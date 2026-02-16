---
title: "[Vulkan]Vulkan_삼각형그리기_Presentation(2/5)"
date: 2025-04-26
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

## **Presentation**

### Window Surface

Vulkan은 플랫폼에 독립적인 API이기 때문에, 자체적으로는 윈도우 시스템과 직접적으로 연결할 수 없습니다.

이를 해결하기 위해서는 Vulkan과 window system을 이어줄 WSI(Window System Interface)가 필요합니다.

이번 챕터에서는 이를 해결해줄 **VK\_KHR\_surface** 확장에 대해 설명할 것입니다.  
이 확장은 렌더링된 이미지를 표시할 수 있는 **abstract surface(추상적인 표면)**을 나타내는 VkSurfaceKHR 객체를 노출시켜줍니다.

우리 프로그램에서 사용하는 surface는 **이미 GLFW로 생성해둔 윈도우를 기반으로** 만들어질 것입니다.  
VK\_KHR\_surface는 **instance-level extension(**인스턴스 레벨 확장**)** 이고,  
우리는 이미 이 확장을 활성화한 상태입니다.(glfwGetRequiredInstanceExtensions 함수가 반환하는 리스트에 포함되어 있습니다)  
이 리스트에는 앞으로 사용할 다른 WSI 확장도 포함되어 있습니다. **window surface는 instance를 만든 직후에 생성**해 줘야합니다.  
그 이유는 **surface가 어떤 GPU(물리 디바이스)를 선택할지에 영향을 줄 수 있기 때문입니다.**

### Window Surface Creation

VkSurfaceKHR 객체 자체는 플랫폼에 독립적이지만, 생성 방식은 플랫폼에 따라 다르기 때문에 의존적인 코드가 필요합니다.

하지만 이 부분은 GLFW가 해결해줍니다.

```
void initVulkan() {
    createInstance();
    setupDebugMessenger();
    createSurface();
    pickPhysicalDevice();
    createLogicalDevice();
}


void createSurface() {
    if (glfwCreateWindowSurface(instance, window, nullptr, &surface) != VK_SUCCESS) {
        throw std::runtime_error("failed to create window surface!");
    }
}
```

### Destory Window

instance를 destory 하기 전에 먼저 surface를 destroy 해줘야 한다.

(GLFW에서는 destroy 함수를 제공하지 않아서, GLFW로 생성했지만 vulkan api로 파괴한다. )

```
void cleanup() {
    ...
    vkDestroySurfaceKHR(instance, surface, nullptr);
    vkDestroyInstance(instance, nullptr);
    ...
}
```

### Querying for presentation supprot (presentation 지원 확인하기)

Vulkan이 윈도우 시스템을 통합을 지원하지만, GPU device가 present 기능을 지원하는 지는 다른 이야기입니다.

그렇기 떄문에 이를 확인할 필요가 있습니다.

우선 presentFamily를 추가하고, isComplete도 확장해줍시다.

```
struct QueueFamilyIndices {
	std::optional<uint32_t> graphicsFamily;
	std::optional<uint32_t> presentFamily;

	bool isComplete()
	{
		return graphicsFamily.has_value() && presentFamily.has_value();
	}
};
```

findQueueFamilies함수에서

graphics 와 present를 지원하는 Queue Family를 찾을 것입니다.

대부분 graphics를 지원하면 present도 지원을 하지만 일관된 구조를 위해서 별도의 Queue로 취급하겠습니다.

(두개의 queue family를 동일하게 보고 성능을 개선시켜도 괜찮습니다.)

```
//queue family
QueueFamilyIndices findQueueFamilies(VkPhysicalDevice device)
{
    QueueFamilyIndices indices;

    //Logic to find graphics queue family indices to populate struct with
    uint32_t queueFamilyCount = 0;
    vkGetPhysicalDeviceQueueFamilyProperties(device, &queueFamilyCount, nullptr);

    std::vector<VkQueueFamilyProperties> queueFamilies(queueFamilyCount);
    vkGetPhysicalDeviceQueueFamilyProperties(device, &queueFamilyCount, queueFamilies.data());

    int i = 0;
    for (const auto& queueFamily : queueFamilies)
    {
        if (queueFamily.queueFlags & VK_QUEUE_GRAPHICS_BIT)
        {
            indices.graphicsFamily = i;

            VkBool32 presentSupport = false;
            vkGetPhysicalDeviceSurfaceSupportKHR(device, i, surface, &presentSupport);

            if (presentSupport)
            {
                indices.presentFamily = i;
            }
        } 

        if (indices.isComplete())
        {
            break;
        }

        i++;
    }

    return indices;
}
```

### Creating the presetation queue

여기서도 당연히 handle이 필요하니 멤버변수로 선언을 해줍니다.

그리고 점점 많아지는 queue family를 관리하는 우아한 방법은

queue family의 인덱스를 std::set으로 관리해주는 방법입니다.

만약 graphics queue 와 present queue가 동일한 family index를 가지고 있다면

한 번만 전달하게 됩니다.. ( set -> 중복없이 저장)

```
#include <set>

...

//logical device
void createLogicalDevice()
{
    QueueFamilyIndices indices = findQueueFamilies(physicalDevice);

    //queue info
    std::vector<VkDeviceQueueCreateInfo> queueCreateInfos;
    std::set<uint32_t> uniqueQueueFamilies = 
        { indices.graphicsFamily.value(), indices.presentFamily.value() };

    float queuePriority = 1.0f;
    for (uint32_t queueFamily : uniqueQueueFamilies)
    {
        VkDeviceQueueCreateInfo queueCreateInfo{};
        queueCreateInfo.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
        queueCreateInfo.queueFamilyIndex = queueFamily;
        queueCreateInfo.queueCount = 1;
        queueCreateInfo.pQueuePriorities = &queuePriority;

        queueCreateInfos.push_back(queueCreateInfo);
    }

    //features

    //create logical device

    // ......

    vkGetDeviceQueue(device, indices.graphicsFamily.value(), 0, &graphicsQueue);
    vkGetDeviceQueue(device, indices.presentFamily.value(), 0, &graphicsQueue);
}
```

(여기서 graphicsQueue와 present Queue는 같은 handle을 가질 수도 있습니다.)

## Swap chain

Vulkan에는 default framebuffer(기본 프레임 버퍼)라는 개념이 없습니다. ( 또 우리한테 다 시킨다~~!~!~)

그래서 우리가 렌더링할 버퍼를 **직접 소유하고 관리해줄 구조가 필요합니다.**

이 구조가 바로 **스왑 체인(swap chain)** 입니다.

Vulkan에서는 **명시적으로 우리가 ^^ 생성해야 합니다.**

SwapChain은 기본적으로 **화면에 표시되기를 기다리는 이미지들의** **queue** 라고 생각하면 됩니다.

우리 애플리케이션은 이 이미지 중 하나를 **획득(acquire)** 해서 그 위에 그림을 그리고, **작업이 끝난 후 다시 queue에 반환**합니다.

이 Queue가 **어떻게 작동하고,** **언제 이미지를 화면에 표시할 수 있는지**는 swapChain이 어떻게 설정되었느냐에 따라 달라집니다.  
(swapChain의 일반적인 목적은 **화면 주사율(refresh rate)에 맞춰 이미지 출력 타이밍을 동기화하는 것입니다.** )

### Checking for swap chain support

계속 말하지만 모든 그래픽 카드가 화면에 이미지를 직접 출력할 수 있는 것은 아닙니다.

그리고 이미지 프레젠테이션은 **윈도우 시스템 및 윈도우에 연결된 surface와 깊은 연관이 있기 때문에**,

**Vulkan의 코어(core)** 기능에는 포함되어 있지 않습니다.

따라서, swapChain을 사용하려면 반드시 **VK\_KHR\_swapchain 디바이스 확장**을 **지원하는지 확인하고**,  
지원한다면 **명시적으로 활성화(enable)** 해줘야합니다.

이를 위해 먼저 isDeviceSuitable 함수를 확장해서 **swapChain 확장을 지원하는지 확인하도록** 만듭시다.

더보기

참고로 Vulkan 헤더에는  
**VK\_KHR\_SWAPCHAIN\_EXTENSION\_NAME** 이라는 **매크로를 사용하면** 오타 걱정 없이 VK\_KHR\_swapchain 확장을 표현(?)할 수 있습니다. ( 내부적으로 문자열로 되어있습니다)

먼저, 필요한 디바이스 확장 목록을 다음과 같이 선언하자 (마치 밸리데이션 레이어처럼):

그리고

우리가 필요한 확장자들이 모두 존재하는 지 확인합시다.

```
//swap chain
const std::vector<const char*> deviceExtensions = 
{
	VK_KHR_SWAPCHAIN_EXTENSION_NAME
}

//.....

bool isDeviceSuitable(VkPhysicalDevice device)
{
    QueueFamilyIndices indices = findQueueFamilies(device);

    bool extensionSupported = checkDeviceExtensionSupport(device);

    return indices.isComplete();
}

bool checkDeviceExtensionSupport(VkPhysicalDevice device)
{
    return true;
}
```

checkDeviceExtensionSupport 함수를 아래와 같이 구현하면

requiredExtenstion이 Empty는 모든게 support되어진다는 의미입니다.

```
	bool checkDeviceExtensionSupport(VkPhysicalDevice device)
	{
		uint32_t extensionCount;
		vkEnumerateDeviceExtensionProperties(device, nullptr, &extensionCount, nullptr);

		std::vector<VkExtensionProperties> availableExtensions(extensionCount);
		vkEnumerateDeviceExtensionProperties(device, nullptr, &extensionCount, availableExtensions.data());

		std::set<std::string> requiredExtenstion(deviceExtensions.begin(), deviceExtensions.end());

		for (const auto& extension : availableExtensions)
		{
			requiredExtenstion.erase(extension.extensionName);
		}


		return requiredExtenstion.empty();
	}
```

swapchain이 지원된다는 것을 확인할 수 있습니다.

![](https://blog.kakaocdn.net/dna/IvXwp/btsNcqSuZPM/AAAAAAAAAAAAAAAAAAAAAApdiS_b-ZcN9FhixhIOyBMx1lxb1gL4QdmXLIDwTY5v/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=FTgvt8nHYOBADAMs4dnYYJTTGzE%3D)![](https://blog.kakaocdn.net/dna/bNwDUP/btsNdAs4fGh/AAAAAAAAAAAAAAAAAAAAAO9BasP9NlwW2uwPspjbINmgV1HUXBXYxSWuNOGj8O4h/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=72KzXtPN%2BYSGKReaAHhWee3jpMM%3D)

### Enabling device extensions ( device 확장 활성화 )

지원되는 것까지 했으니, 이제 활성화를 해봅시다.

logical device를 생성할 때 createinfo를 수정합시다.

```
createInfo.enabledExtensionCount = static_cast<uint32_t>(deviceExtensions.size());
createInfo.ppEnabledExtensionNames = deviceExtensions.data();
```

### 

### Querying details of swap chain support (스왑 체인 지원 세부 정보 조회 )

swap chain이 가능한지 체크한걸로는 부족합니다...

해당 swap chain과 우리가 만든 윈도우 surface와 호환이 되는 지 확인해봐야합니다.

swapChain 생성을 위해선 instance, device 생성보다 훨씬 **더 많은 설정 정보**가 필요하기 때문에,

미리 자세한 정보를 쿼리해야합니다.

확인해야 할 세 가지 주요 속성입니다.

1. **기본 surface 기능(capabilities)**
   * 스왑 체인 이미지의 최소/최대 개수
   * 이미지의 최소/최대 너비 및 높이
2. **지원되는 surface format**
   * 픽셀 포맷, 색상 공간 등
3. **지원되는 프레젠테이션 모드**
   * vsync 여부 등

이 정보들을 한 번에 전달하기 위해서 구조체로 묶어서 관리하겠습니다.

```
struct SwapChainSupportDetails
{
	VkSurfaceCapabilitiesKHR capabilities;
	std::vector<VkSurfaceFormatKHR> formats;
	std::vector<VkPresentModeKHR> presentModes;
};

SwapChainSupportDetails querySwapChainSupport(VkPhysicalDevice device)
{
    SwapChainSupportDetails details;

    return details;
}
```

이 형식에서 위에서 말한 3가지 detail을 추가합시다.

```
//swap chain
SwapChainSupportDetails querySwapChainSupport(VkPhysicalDevice device)
{
    SwapChainSupportDetails details;

    //capabilities
    vkGetPhysicalDeviceSurfaceCapabilitiesKHR(device, surface, &details.capabilities);

    //format
    uint32_t formatCount;
    vkGetPhysicalDeviceSurfaceFormatsKHR(device, surface, &formatCount, nullptr);

    if (formatCount != 0)
    {
        details.formats.resize(formatCount);
        vkGetPhysicalDeviceSurfaceFormatsKHR(device, surface, &formatCount, details.formats.data());
    }

    //presentMode
    uint32_t presentModeCount;
    vkGetPhysicalDeviceSurfacePresentModesKHR(device, surface, &presentModeCount, nullptr);

    if (presentModeCount != 0)
    {
        details.presentModes.resize(presentModeCount);
        vkGetPhysicalDeviceSurfacePresentModesKHR(device, surface, &presentModeCount, details.presentModes.data());
    }

    return details;
}
```

이렇게 체크하는 코드를 추가했으면

isDeviceSuitable함수를 다시 확장해서 swapchain 지원이 적절한지 확인하는 것도 추가합시다.

**swapchain지원이 적절하다는 의미는 suface format이 1개 이상 있고 & present mode가 1개 이상 존재한다는 의미입니다.**

```
bool isDeviceSuitable(VkPhysicalDevice device)
{
    QueueFamilyIndices indices = findQueueFamilies(device);

    bool extensionSupported = checkDeviceExtensionSupport(device);

    //swapchain
    bool swapChainAdequate = false;
    if (extensionSupported)
    {
        SwapChainSupportDetails swapChainSupport = querySwapChainSupport(device);
        swapChainAdequate = !swapChainSupport.formats.empty() &&
            !swapChainSupport.presentModes.empty();
    }

    return indices.isComplete() && extensionSupported && swapChainAdequate;
}
```

### 

### **Choosing the right settings for the swap chain (스왑 체인에 적합한 설정 선택하기)**

swapChainAdequate 조건이 충족되었다면, 기본적인 support는 충분하지만 아직도 여러가지 옵션들이 존재합니다.

최적의 설정을 선택하기 위해서 3가지 주요 설정을 고르는 함수를 만듭시다.

* **Surface Format** (색 깊이, 픽셀 포맷)
* **Presentation Mode** (이미지를 화면에 스왑하는 조건)
* **Swap Extent** (이미지의 해상도)

각 항목마다 **이상적인 설정값(ideal value)** 을 먼저 선택하고,  
만약 사용할 수 없다면 **차선의 옵션을 선택하는 로직**을 작성할 거야.

여기서는 위에서 골라놓은 foramt에서

우리가 원하는 format, colorSpace를 선택하고, 만약 그게 없다면 0번째 인덱스에 저장된 형식을 사용해도 큰 무리가 없다.

```
VkSurfaceFormatKHR chooseSwapSurfaceFormat(const std::vector<VkSurfaceFormatKHR>& availableFormats)
{
    for (const auto& availableFormat : availableFormats)
    {
        if (availableFormat.format == VK_FORMAT_B8G8R8A8_SRGB &&
            availableFormat.colorSpace == VK_COLOR_SPACE_SRGB_NONLINEAR_KHR)
        {
            return availableFormat;
        }
    }

    return availableFormats[0];
}
```

### Presentation mode

**VK\_PRESENT\_MODE\_IMMEDIATE\_KHR**

애플리케이션이 제출한 이미지를 바로 화면에 표시하는 방식이다.  
디스플레이의 새로 고침 시점을 기다리지 않기 때문에 반응 속도가 빠르지만,  
그만큼 **화면 찢김(tearing) 현상이 발생할 수 있다.**

**VK\_PRESENT\_MODE\_FIFO\_KHR**

스왑체인을 **큐(queue)로 생각하면 된다.**  
디스플레이가 새로 고쳐질 때 큐의 앞에서 이미지 하나가 꺼내지고,  
애플리케이션은 새 이미지를 큐의 뒤에 삽입한다.  
**큐가 가득 찼을 경우, 애플리케이션은 다음 VBlank(수직 동기화 시점)까지 대기해야 한다.**  
**이 방식은 VSync와 동일하며, 모든 Vulkan 구현에서 반드시 지원된다.**

**VK\_PRESENT\_MODE\_FIFO\_RELAXED\_KHR**

**기본 동작은 FIFO와 동일하다**.  
하지만 애플리케이션이 너무 늦게 이미지를 제출해서 **큐가 비어 있는 상태에서 VBlank가 발생하면,**  
**그 시점에 바로 이미지를 표시한다.**  
**이 경우 화면 찢김이 발생할 수 있다.**

**VK\_PRESENT\_MODE\_MAILBOX\_KHR**

FIFO 방식의 변형이다.  
**큐가 가득 찼을 때 애플리케이션이 대기하지 않고,**  
**큐에 들어 있는 오래된 이미지를 새로운 이미지로 교체한다.**  
화면 찢김 없이 가능한 한 최신 프레임을 표시할 수 있어 지연(latency)을 줄이고  
**부드러운 애니메이션을 구현할 수 있다.**  
트리플 버퍼링과 비슷한 방식이지만, 단순히 버퍼가 3개라는 이유만으로 프레임 제한이 사라지는 건 아니다.

energy 사용 문제가 없다면 VK\_PRESENT\_MODE\_MAILBOX\_KHR이 굉장히 좋아보입니다.

하지만 모바일에서는 energy 사용이 가장 중요하기 때문에 VK\_PRESENT\_MODE\_FIFO\_KHR 를 사용을 권장합니다.

여기서는 mailbox방법을 우선 사용하고, 지원하지 않으면 fifo를 사용하는 방법으로 구현했습니다.

```
VkPresentModeKHR chooseSwapPresentMode(const std::vector<VkPresentModeKHR>& availablePresentModes)
{
    for (const auto& availablePresentMode : availablePresentModes)
    {
        if (availablePresentMode == VK_PRESENT_MODE_MAILBOX_KHR)
        {
            return availablePresentMode;
        }
    }

    return VK_PRESENT_MODE_FIFO_KHR;
}
```

### Swap Extent

스왑 체인에서 사용되는 이미지의 **해상도 (픽셀 단위 크기)** 를 의미합니다.

대부분의 경우 이 해상도는 **우리가 렌더링할 창의 해상도와 정확히 일치해야합니다.**

이 값의 허용 범위는 VkSurfaceCapabilitiesKHR 구조체 안에 정의되어 있고,

currentExtent 멤버가 **기본적으로** **창의 해상도와 일치하도록 설정**되어 있습니다.

( **하지만 일부 플랫폼/윈도우 매니저에서는 Vulkan이 이 값을 직접 설정하지 않을 수도 있습니다.** currentExtent.width와 height가 uint32\_t의 최대값으로 설정되어 있습니다.

이런 경우에는, **우리가 직접 창 크기에 맞춰 적절한 해상도를 설정해야합니다.**  )

GLFW는 **두 가지 단위를 사용**해:

* **스크린 좌표**: glfwCreateWindow에서 지정한 WIDTH, HEIGHT
* **픽셀 단위**: 실제 렌더링이 이루어지는 단위 (Vulkan에서 요구)

예를 들어 DPI가 높은 모니터에서는 **스크린 좌표보다 픽셀 수가 더 많을 수 있어.**

(단순히 800x600이라고 800x600공간에 800x600개의 픽셀만 있는 것은 아니다 )

그래서 단순히 {WIDTH, HEIGHT}를 사용할 수는 없고,

**GLFW의 glfwGetFramebufferSize를 사용해서 픽셀 해상도를 가져와야한다.**

```
VkExtent2D chooseSwapExtent(const VkSurfaceCapabilitiesKHR& capabilities)
{
	if (capabilities.currentExtent.width != std::numeric_limits<uint32_t>::max())
	{
		return capabilities.currentExtent;
	}

	else
	{
		int width, height;

		glfwGetFramebufferSize(window, &width, &height);

		VkExtent2D actualExtent = {
			static_cast<uint32_t> (width),
			static_cast<uint32_t> (height),
		};

		actualExtent.width = std::clamp(actualExtent.width,
			capabilities.minImageExtent.width,
			capabilities.maxImageExtent.width);

		actualExtent.height = std::clamp(actualExtent.height,
			capabilities.minImageExtent.height,
			capabilities.maxImageExtent.height);
		
		return actualExtent;
	}
}
```

### **Create the Swap Chain**

이제 logical device생성 하고 swapchain을 생성합시다.

```
void initVulkan() {
    createInstance();
    setupDebugMessenger();
    createSurface();
    pickPhysicalDevice();
    createLogicalDevice();
    
    // 여기서 호출
    createSwapChain();  
}

// 지금까지 세팅을 위해 만들었던 함수들 사용
void createSwapChain() {
    SwapChainSupportDetails swapChainSupport = querySwapChainSupport(physicalDevice);

    VkSurfaceFormatKHR surfaceFormat = chooseSwapSurfaceFormat(swapChainSupport.formats);
    VkPresentModeKHR presentMode = chooseSwapPresentMode(swapChainSupport.presentModes);
    VkExtent2D extent = chooseSwapExtent(swapChainSupport.capabilities);
}
```

이제 swapchain에 사용할 이미지의 수를 설정해야되는데

구현체가 요구하는 최소한의 이미지 개수에서 1개 더 요청하는 것이 일반적입니다.

(max를 넘지 않는 선에서)

```
void createSwapChain()
{
    SwapChainSupportDetails swapChainSupport = querySwapChainSupport(physicalDevice);

    VkSurfaceFormatKHR surfaceFormat = chooseSwapSurfaceFormat(swapChainSupport.formats);
    VkPresentModeKHR presentMode = chooseSwapPresentMode(swapChainSupport.presentModes);
    VkExtent2D extent = chooseSwapExtent(swapChainSupport.capabilities);

    uint32_t imageCount = swapChainSupport.capabilities.minImageCount + 1;
    if (swapChainSupport.capabilities.maxImageCount > 0 && 
        imageCount > swapChainSupport.capabilities.maxImageCount)
    {
        imageCount = swapChainSupport.capabilities.maxImageCount;
    } 

}
```

이렇게 세팅할 준비를 마쳤으면, SwapChainCreateInfo에 값을 채워 넣고.

입체 3D app을 개발하는게 아니면 imageArrayLayer는 항상 1입니다..

현재 튜토리얼에서 사용하고 있는 (아래 코드) imageUsage는 swapchain 이미지에 직접 렌더링 한다는 의미입니다.

post processing을 하고 싶다면 ATTACHMENT\_BIT가 아니라 TRANSFER\_DST\_BIT 등으로 바꿔서 작업할 수 있습니다.

```
void createSwapChain()
{
    SwapChainSupportDetails swapChainSupport = querySwapChainSupport(physicalDevice);

    VkSurfaceFormatKHR surfaceFormat = chooseSwapSurfaceFormat(swapChainSupport.formats);
    VkPresentModeKHR presentMode = chooseSwapPresentMode(swapChainSupport.presentModes);
    VkExtent2D extent = chooseSwapExtent(swapChainSupport.capabilities);

    uint32_t imageCount = swapChainSupport.capabilities.minImageCount + 1;
    if (swapChainSupport.capabilities.maxImageCount > 0 && 
        imageCount > swapChainSupport.capabilities.maxImageCount)
    {
        imageCount = swapChainSupport.capabilities.maxImageCount;
    }

    VkSwapchainCreateInfoKHR createInfo{};
    createInfo.sType = VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR;
    createInfo.surface = surface;

    createInfo.minImageCount = imageCount;
    createInfo.imageFormat = surfaceFormat.format;
    createInfo.imageColorSpace = surfaceFormat.colorSpace;
    createInfo.imageExtent = extent;
    createInfo.imageArrayLayers = 1;
    createInfo.imageUsage = VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT;

}
```

### 

### Queue Family Sharing Mode( 스왑 체인 공유 방식 설정 )

```
QueueFamilyIndices indices = findQueueFamilies(physicalDevice);
uint32_t queueFamilyIndices[] =
	{ indices.graphicsFamily.value(), indices.presentFamily.value() };

if (indices.graphicsFamily != indices.presentFamily)
{
	createInfo.imageSharingMode = VK_SHARING_MODE_CONCURRENT;
	createInfo.queueFamilyIndexCount = 2;
	createInfo.pQueueFamilyIndices = queueFamilyIndices;
}
else
{
	createInfo.imageSharingMode = VK_SHARING_MODE_EXCLUSIVE;
	createInfo.queueFamilyIndexCount = 0;
	createInfo.pQueueFamilyIndices = nullptr;
}
```

VK\_SHARING\_MODE\_EXCULSIVE (최고 성능)

이미지가 한 개의 queue family에만 소속 가능, 다른 queue에서 쓸 때는 명시적으로 소유권을 이전해야 됩니다.

VK\_SHARING\_MODE\_CONCURRENT ( 간편 but 조금 느림 )

여러 queue family에서 동시에 사용할 수 있습니다.

**만약 graphics와 presentation queue family가 동일하다면 exclusive를 사용해야됩니다.**

**왜냐하면 concurrent mode는 최소 2개 이상의 queue family가 필요하기 때문입니다.**

### 이미지 변환 설정

```
createInfo.preTransform = swapChainSupport.capabilities.currentTransform;
```

스왑 체인 이미지에 **회전, 반전 등 변환을 적용할 수 있습니다.**

여기선 **변환 없이 그대로** 쓰겠다는 의미로 현재 설정값을 그대로 사용하겠습니다.

### 알파 블렌딩 설정

```
createInfo.compositeAlpha = VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR;​
```

다른 윈도우와의 **알파 블렌딩** 설정을 할 수 있습니다.

거의 항상 알파 채널을 무시하기 때문에 **불투명 모드**(OPAQUE)를 사용하겠습니다.

### 

### 프레젠트 모드 설정

```
createInfo.presentMode = presentMode;​
```

앞에서 선택한 VK\_PRESENT\_MODE\_FIFO\_KHR 또는 MAILBOX\_KHR을 그래도 사용하겠습니다.

### 

### 픽셀 클리핑 설정

```
createInfo.clipped = VK_TRUE;​
```

다른 창에 **가려진 픽셀은 무시**해도 된다는 의미입니다.

**성능 최적화를 위해 사용합시다.**

### 

### 스왑 체인 재생성 대비

```
createInfo.oldSwapchain = VK_NULL_HANDLE;
```

Vulkan에서는 **윈도우 크기 변경 등의 이유로 스왑 체인을 다시 생성해야 할 때가 있습니다.**

그때 기존 스왑 체인을 oldSwapchain에 넘겨서 **리소스 재활용**이 가능합니다.

현재는 단일 생성만 고려하므로 NULL 처리하겠습니다.

이제 셋팅이 끝났으니 create해주면 됩니다!

```
if (vkCreateSwapchainKHR(device, &createInfo, nullptr, &swapChain) != VK_SUCCESS)
{
	throw std::runtime_error("failed to create swap chain!");
}
```

그리고 우리가 계속하던대로 destroy도 합시다.

### Retrieving the swap chain images

이제 swapchain을 생성했으니, handle을 가져옵시다. 나중에 렌더링할 때 사용할 것입니다.

swapChain을 멤버 변수로 저장합시다.

```
std::vector<VkImage> swapChainImages;
```

**vkCreateSwapchainKHR() 이후에 handle을 가져오는 코드를 추가한다.**

createSwapChain()에서 최소 이미지 개수만 지정했기 때문에, 실제 vulkan이 그보다 많은 이미지를 생성할 수도 있습니다. 그래서 아래 코드처럼 개수를 먼저 확인한다.

```
vkGetSwapchainImagesKHR(device, swapChain, &imageCount, nullptr);
swapChainImages.resize(imageCount);

vkGetSwapchainImagesKHR(device, swapChain, &imageCount, swapChainImages.data());
```

우리가 선택한 이미지 format과 extent를 나중에 사용하기 위해 저장합시다.

멤버변수로 아래에 변수 4개를 만들어서 저장합시다.

```
VkSwapchainKHR swapChain;
std::vector<VkImage> swapChainImages;
VkFormat swapChainImageFormat;
VkExtent2D swapChainExtent;
```

createSwapChain() 끝에서 다음과 같이 format을 저장하면됩니다.

```
swapChainImageFormat = surfaceFormat.format;
swapChainExtent = extent;
```

### Image View

어떤 VkImage이든, 스왑체인에 포함된 이미지들도 포함해서, 렌더 파이프라인에서 사용하려면 VkImageView 객체를 생성해야 합니다.

**이미지 뷰(Image View)는 말 그대로 이미지에 대한 뷰(view)입니다.**  
이미지를 어떻게 접근할지, 이미지의 어떤 부분을 접근할지 설명합니다.

예를 들어, 해당 이미지가 2D 텍스처인지, 깊이 텍스처인지, mipmap 레벨을 사용할 것인지 등을 지정합니다.

이 장에서는 스왑체인에 있는 모든 이미지에 대해 **기본적인 이미지 뷰를 생성하는 createImageViews 함수를 작성할 것입니다.** 이렇게 하면 나중에 해당 이미지들을 컬러 타겟으로 사용할 수 있습니다

클래스 멤버 변수로 imageView를 저장합시다.

```
std::vector<VkImageView> swapChainImageViews;
```

SwapChain생성 직후에 호출합니다.

```
void initVulkan() {
    createInstance();
    setupDebugMessenger();
    createSurface();
    pickPhysicalDevice();
    createLogicalDevice();
    createSwapChain();
    
    
    // 여기에 추가
    createImageViews(); 
}
```

이미지를 설정하고 생성합니다.

mipmap없이 일단 가장 basic하게 만듭시다..!

```
void createImageView()
{
	swapChainImageViews.resize(swapChainImages.size());

	for (size_t i = 0; i < swapChainImages.size(); i++)
	{
		VkImageViewCreateInfo createInfo{};

		createInfo.sType = VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO;
		createInfo.image = swapChainImages[i];
		createInfo.viewType = VK_IMAGE_VIEW_TYPE_2D;
		createInfo.format = swapChainImageFormat;

		createInfo.components.r = VK_COMPONENT_SWIZZLE_IDENTITY;
		createInfo.components.g = VK_COMPONENT_SWIZZLE_IDENTITY;
		createInfo.components.b = VK_COMPONENT_SWIZZLE_IDENTITY;
		createInfo.components.a = VK_COMPONENT_SWIZZLE_IDENTITY;

		createInfo.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
		createInfo.subresourceRange.baseMipLevel = 0;
		createInfo.subresourceRange.levelCount = 1;
		createInfo.subresourceRange.baseArrayLayer = 0;
		createInfo.subresourceRange.layerCount = 1;

		if (vkCreateImageView(device, &createInfo, nullptr, &swapChainImageViews[i]) != VK_SUCCESS)
		{
			throw std::runtime_error("failed to create image views!");
		} 
	}
}
```

만약 입체(3D) 애플리케이션을 만들고 있다면, 여러 레이어를 가진 swapChain을 만들어야합니다.  
이 경우, 각 레이어를 왼쪽/오른쪽 눈용으로 접근할 수 있도록 여러 개의 이미지 뷰를 만들 수 있습니다.

생성 뒤에는 항상 그랬듯이 cleanup을 채웁시다.

```
void cleanup() {
    for (auto imageView : swapChainImageViews) {
        vkDestroyImageView(device, imageView, nullptr);
    }
 //...
}
```

이미지 뷰를 생성하면 이미지를 **텍스처**로 사용하는 데에는 충분하지만,  
**렌더 타겟(Render Target)** 으로 사용하려면 **프레임버퍼(FrameBuffer)** 를 생성하는 한 단계가 더 필요합니다.

이 작업은 그래픽스 파이프라인을 설정할 때 추가합시다.