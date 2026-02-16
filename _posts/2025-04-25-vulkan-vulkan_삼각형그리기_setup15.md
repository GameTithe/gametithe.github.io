---
title: "[Vulkan] Vulkan_삼각형그리기_Setup(1/5)"
date: 2025-04-25
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

~~(적은 포스팅으로 끝내려다보니 너무 길게 적었습니다 ㅋㅋㅋㅋ.... 뒤로 갈 수록 짧아지니 너무 겁먹지마세요)~~

글을 정리하다보니 양이 너무 많아서 나눠야겠습니다.. 원래는 3부작으로 끝내보려고 했는데 오히려 그게 더 학습이 어려울 것 같습니다. ( 스크롤 크기를 보고 포기하실 것 같아서 ... )

그냥 tutorial 처럼 5부작으로 나누겠습니다! 여기서는 Setup을 하겠습니다.

![](https://blog.kakaocdn.net/dna/kWPUH/btsNinapwu0/AAAAAAAAAAAAAAAAAAAAAIaA5EH2aOdM087y11iTRgZSXOQHQvg9uz8qmpNVUZF2/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3GeWd%2Bb1d0X9IrjKLPpNjbwAc28%3D)

Vulkan으로 삼각형을 그리기 위해서는 약 140쪽의 document 분량입니다...

왜 vulkan과 친해지고 싶은게 맞는지 다시 한번 생각을...

세팅을 하면서 느낀 점은 openGL을 공부하고 vulkan 공부를 해야된다는 것입니다.

이 세팅을 왜하는지, 이 param이 무슨 역할인지 알고 쓰는것과 그냥 따라하는 것은 천지차이 같습니다

openGL 공부하고 vulkan하는거면 openGL공부하는거 시간 낭비아닌가요??  
절대아닙니다...!!  
  
그래픽스 이론은 일맥상통 모두 동일합니다. 사람이 사용하는 API만 다를 뿐!!

저도 공부할 때 고민을 많이 했던 부분이였어서 주저리주저리 써봤습니다...

이제 Vulkan 시작해보겠습니다.

~~글이 너무 길어져서 2부작으로 진행될 예정입니다~~

~~3부작으로 나눴습니다. 이어지는 글들은 분량조절 잘 했습니다!~~

네.. 5부작이 되었습니다...

Base Code

```
#include <vulkan/vulkan.h>

#include <iostream>
#include <stdexcept>
#include <cstdlib>

class HelloTringleApplication
{
public:
	void run()
	{
		initVulkan();
		mainLoop();
		cleanup();
	}

private:
	void initVulkan() {

	}

	void mainLoop()
	{
		
	}

	void cleanup()
	{

	}
};

int main()
{
	HelloTringleApplication app;
	

	try
	{
		app.run();
	}

	catch (const std::exception& e)
	{
		std::cerr << e.what() << std::endl;

		return EXIT_FAILURE;
	} 

	return EXIT_SUCCESS;
}
```

### Resource Mangement

C++에서는 <memory> 헤더의 스마트 포인터나 RAII 기법을 통해 자동으로 리소스를 관리할 수 있습니다. 하지만 이 튜토리얼에서는 Vulkan 객체의 생성과 해제를 명시적으로 작성하겠습니다.

Vulkan은 모든 작업을 명확하게 처리하는 것을 목표로 하므로, 객체의 수명을 명확히 관리하는 것이 API를 배우는 데 도움이 됩기 때문입니다

이 튜토리얼을 다 따라간 후에는, Vulkan 객체를 생성자에서 얻고 소멸자에서 해제하는 C++ 클래스를 만들어 자동 리소스 관리를 구현하거나, std::unique\_ptr 또는 std::shared\_ptr에 커스텀 deleter를 제공하는 방법으로도 관리할 수 있습니다. 큰 규모의 Vulkan 프로그램에서는 RAII 방식이 권장되지만, 처음에는 내부에서 어떤 일이 일어나는지를 아는 것이 중요합니다.

```
생성: vkCreateXXX, vkAllocateXXX
해제: vkDestroyXXX, vkFreeXXX
```

Base Code:

```
//#include <vulkan/vulkan.h>

#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>


#include <iostream>
#include <stdexcept>
#include <cstdlib>

class HelloTringleApplication
{
public:
	void run()
	{
		initWindow();
		initVulkan();
		mainLoop();
		cleanup();
	}

private:
	GLFWwindow* window;
	const uint32_t WIDTH = 800;
	const uint32_t HEIGHT = 600;
	void initWindow() {
		glfwInit();
		glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
		glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE);
		
		window = glfwCreateWindow(WIDTH, HEIGHT, "Vulkan", nullptr, nullptr);
	}

	void initVulkan() {

	}

	void mainLoop()
	{
		while (!glfwWindowShouldClose(window))
		{
			glfwPollEvents();
		}
		
	}

	void cleanup()
	{
		glfwDestroyWindow(window);
		glfwTerminate();

	}
};

int main()
{
	HelloTringleApplication app;
	

	try
	{
		app.run();
	}

	catch (const std::exception& e)
	{
		std::cerr << e.what() << std::endl;

		return EXIT_FAILURE;
	} 

	return EXIT_SUCCESS;
}
```

### Instance

Vulkan을 사용하려면 가장 먼저 해야 할 일은 **Instance를** **생성**하여 Vulkan 라이브러리를 초기화하는 것입니다.  
**Instance는 애플리케이션과 Vulkan 라이브러리 사이의 연결을 의미**하며, Instance를 만들기 위해서는 애플리케이션에 대한 몇 가지 정보를 드라이버에 제공해야 합니다.

이건 optional한 세팅이지만 drive가 최적화하는데 필요한 정보이기 때문에 세팅하는 것을 추천합니다.

```
VkApplicationInfo appInfo{};
appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
appInfo.pApplicationName = "Hello Triangle";
appInfo.applicationVersion = VK_MAKE_VERSION(1, 0, 0);
appInfo.pEngineName = "No Engine";
appInfo.engineVersion = VK_MAKE_VERSION(1, 0, 0);
appInfo.apiVersion = VK_API_VERSION_1_0;
```

이건 non-optional한 부분입니다. (반드시 해줘야되는 부분입니다)

```
VkInstanceCreateInfo createInfo{};
createInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
createInfo.pApplicationInfo = &appInfo;
```

### 

### Cleanup

VkInstance는 반드시 프로그램이 끝날 때 없애야합니다. (앞으로 만들 대부분의 object들은 cleanup에 추가될 것 입니다.)

```
	void cleanup()
	{
		vkDestroyInstance(instance, nullptr);
		glfwDestroyWindow(window);
		glfwTerminate(); 
	}
```

### 

### Validation Layers

Vulkan API는 드라이버 오버헤드를 최적화 하는 것을 목표로 설계되어있습니다. 그렇기 때문에 오류 검사 기능이 매우 제한적입니다.

그렇다고 오류 검사를 못하는 것은 아니고, validation layer를 통해서 오류를 검사할 수 있습니다. ( 프로그램을 만들 때 열심히 오류검사를 하고 실전에서는 이를 빼서 최적의 성능을 내겠다는 말입니다. )

Validation Layer가 하는 일들입니다.

* 잘못된 **파라미터 값이 전달되었는지 검사**합니다.
* 리소스 누수를 방지하기 위해 객체의 **생성/소멸 추적**합니다.
* 여러 쓰레드에서 호출되는 함수의 **스레드 안전성(Thread safety)** 검사합니다.
* 모든 Vulkan 함수 호출과 파라미터를 표준 출력으로 로깅합니다.
* **프로파일링하거나 Replay** 하기 위해서 Vulkan 호출을 트레이싱합니다.

LunarG Vulkan SDK가 open source로 제공해줍니다.

### Using Validation Layer

이 섹션에서는 Vulkan SDK에서 제공하는 **표준 validation layer를** 어떻게 활성화하는지 알아보겠습니다.

확장(extension)과 마찬가지로, **validation layer도 이름을 명시해서 활성화해야 됩니다.**

모든 유용한 표준 검증 기능은 SDK에 포함된 "VK\_LAYER\_KHRONOS\_validation"이라는 이름의 레이어에 통합되어 있습니다.

여기서 NDEBUG 매크로는 C++ 표준에서 제공되는 것으로, 디버그 상태 여부를 판단해줍니다. (  = NDEBUG => 디버그 X) 

```
const uint32_t WIDTH = 800;
const uint32_t HEIGHT = 600;


//validation
const std::vector<const char*> validationLayers = {
	"VK_LAYER_KHRONOS_validation"
};

#ifdef NDEBUG
const bool enableValidationLayers = false;
#else 
const bool enableValidationLayers = true;
#endif
```

이제 새로운 함수 checkValidationLayerSupport를  만들어줍니다.

요청한 validation layer들이 시스템에서 사용 가능한지 확인합니다.

vkEnumerateInstanceLayerProperties를 사용해서 사용 가능한 레이어 목록을 가져오고, 이 목록 안에 원하는 validation layer가 있는지 확인합니다.  ( beakpoint를 둬서 직접 확인하면서 해보세요 :) )

```
bool checkValidationLayerSupport()
{
    uint32_t layerCount;
    vkEnumerateInstanceLayerProperties(&layerCount, nullptr);

    std::vector<VkLayerProperties> availableLayers(layerCount);

    vkEnumerateInstanceLayerProperties(&layerCount, availableLayers.data());

    for (const char* layerName : validationLayers)
    {
        bool layerFound = false;

        for (const auto& layerProperties : availableLayers)
        {
            if (strcmp(layerProperties.layerName, layerName) == 0)
            {
                layerFound = true;
                break;
            }
        }
        if (!layerFound)
            return false;
    }

    return true;
}
```

이제 createInstance() 함수에서 validation layer가 필요한데 시스템에서 지원하지 않는 경우 예외를 발생시킵시다.

```
void createInstance() {
    if (enableValidationLayers && !checkValidationLayerSupport()) {
        throw std::runtime_error("validation layers requested, but not available!");
    }

    //...
}
```

마지막으로 **VkInstanceCreateInfo 구조체를 채울 때 validation layer를 포함**시킨다

```
if (enableValidationLayers)
{
    createInfo.enabledLayerCount = static_cast<uint32_t>(validationLayers.size());
    createInfo.ppEnabledLayerNames = validationLayers.data();
}
else
{
    createInfo.enabledLayerCount = 0;
}
```

### Message callback

디버그 메세지를 처리하기 위해서는

VK\_EXT\_debug\_utils 확장을 사용해서 debug messenger를 설정해야 됩니다.

```
std::vector<const char*> getRequiredExtensions() {
    uint32_t glfwExtensionCount = 0;
    const char** glfwExtensions;
    glfwExtensions = glfwGetRequiredInstanceExtensions(&glfwExtensionCount);

    std::vector<const char*> extensions(glfwExtensions, glfwExtensions + glfwExtensionCount);

    if (enableValidationLayers) {
        extensions.push_back(VK_EXT_DEBUG_UTILS_EXTENSION_NAME);
    }

    return extensions;
}
```

만든 getRequiredExtension을 CreateInstance에서 사용하면 됩니다. (변수 이름이 중복되면 알아서 잘 고쳐보자..!)

```
auto extensions = getRequiredExtensions();
createInfo.enabledExtensionCount = static_cast<uint32_t>(extensions.size());
createInfo.ppEnabledExtensionNames = extensions.data();
```

아래는 디버그 메시지를 받을 때 Vulkan이 호출하게 될 함수이고, 아래의 signature를 갖습니다.

```
static VKAPI_ATTR VkBool32 VKAPI_CALL debugCallback(
    VkDebugUtilsMessageSeverityFlagBitsEXT messageSeverity,
    VkDebugUtilsMessageTypeFlagsEXT messageType,
    const VkDebugUtilsMessengerCallbackDataEXT* pCallbackData,
    void* pUserData
) {
    std::cerr << "validation layer: " << pCallbackData->pMessage << std::endl;

    return VK_FALSE;
}
```

첫 번째 Param: messageSeverity

Debug Message는 아래와 같은 내용을 갖고 있다.

**VK\_DEBUG\_UTILS\_MESSAGE\_SEVERITY\_VERBOSE\_BIT\_EXT:** 진단(diagnostic)용 메시지

**VK\_DEBUG\_UTILS\_MESSAGE\_SEVERITY\_INFO\_BIT\_EXT:** 리소스 생성 등과 같은 정보 제공 메시지

**VK\_DEBUG\_UTILS\_MESSAGE\_SEVERITY\_WARNING\_BIT\_EXT:** 오류는 아니지만, 버그일 가능성이 높은 동작에 대한 경고

**VK\_DEBUG\_UTILS\_MESSAGE\_SEVERITY\_ERROR\_BIT\_EXT:** 명백한 잘못된 동작으로, 충돌이 발생할 수 있는 심각한 오류 메시지

아래로 내려 갈 수록 심각한 메세지이니 이렇게 처리할 수 있습니다.

```
if (messageSeverity >= VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT) {
    // 이 메시지는 중요하므로 출력해도 됨
}
```

두 번째 Param: messageType

**VK\_DEBUG\_UTILS\_MESSAGE\_TYPE\_GENERAL\_BIT\_EXT:** 스펙이나 성능과는 관계없는 일반적인 이벤트 발생

**VK\_DEBUG\_UTILS\_MESSAGE\_TYPE\_VALIDATION\_BIT\_EXT:** 스펙 위반 또는 실수 가능성이 있는 상황

**VK\_DEBUG\_UTILS\_MESSAGE\_TYPE\_PERFORMANCE\_BIT\_EXT:** 성능상 비효율적인 Vulkan 사용 가능성

세 번째 Param: pCallbackData

VkDebugUtilsMessengerCallbackDataEXT 구초체를 가리키며, 메세지의 세부적인 정보를 가지고 있습니다.

아래 3개가 중요한 데이터입니다.

**pMessage:**  
디버그 메시지를 담은 null-terminate 문자열 (const char\*)

**pObjects:**  
이 메시지와 관련된 Vulkan 객체 핸들들의 배열

**objectCount:**  
pObjects 배열에 포함된 객체 수

네 번째 Param: pUserData

콜백을 등록할 때 지정한 사용자 정의 데이터로, 콜백 내에서 사용할 수있는 포인터입니다.

특별한 용도가 없으면 nullptr로 두면됩니다.

**반환값의 의미**

(true, false 실수로 바꿔서 적은거 아닙니다)

VK\_TRUE -> 호출을 중단시키고,  VK\_ERROR\_VALIDATION\_FAILED\_EXT 오류 발생 ( validation layer 자체를 테스트할 때 사용)

VK\_FALSE -> 호출은 계속되고 로깅하는 방식. (일반적으로 사용하는 방식 )

### 콜백 등록하기

디버그 콜백은 **핸들(handle)** 로 관리되며, 명시적으로 **생성 및 제거**를 해줘야 합니다.  
원한다면 여러 개를 동시에 등록할 수도 있습니다.

```
void initVulkan()
{
    createInstance();
    setupDebugMessenger();
}

void setupDebugMessenger()
{
	if (!enableValidationLayers) return;

	VkDebugUtilsMessengerCreateInfoEXT createInfo{};

	createInfo.sType = VK_STRUCTURE_TYPE_DEBUG_UTILS_MESSENGER_CREATE_INFO_EXT;
	createInfo.messageSeverity = 
		VK_DEBUG_UTILS_MESSAGE_SEVERITY_VERBOSE_BIT_EXT | 
		VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT |
		VK_DEBUG_UTILS_MESSAGE_SEVERITY_ERROR_BIT_EXT;

	createInfo.messageType = 
		VK_DEBUG_UTILS_MESSAGE_TYPE_GENERAL_BIT_EXT |
		VK_DEBUG_UTILS_MESSAGE_TYPE_VALIDATION_BIT_EXT |
		VK_DEBUG_UTILS_MESSAGE_TYPE_PERFORMANCE_BIT_EXT;

	createInfo.pfnUserCallback = debugCallback;
	createInfo.pUserData = nullptr; //Optional 

}
```

**messageSeverity:** information에 관한 message만 제외하고 모두 확인할 수 있도록 했습니다.

**messageType:** 콜백 받을 메세지 타입을 조정할 수 있습니다.

**pfnUserCallback:** 실제로 등록할 콜백 함수의 포인터를 지정하고,

**pUserData 필드:** 선택적으로 콜백 함수에 전달할 상용자 정의 데이터를 넘길 수 있습니다.

(예를 들어 HelloTriangleApplication 클래스의 포인터를 넘겨주는 용도로 사용할 수 있다.)

VkDebugUtilsMessengerEXT(디버그 메신저)를 만들기 위해서 PFN\_vkCreateDebugUtilsMessengerEXT 함수를 호출해야합니다.

하지만 PFN\_vkCreateDebugUtilsMessengerEXT이 확장함수 이기 때문에 vkGetInstanceProcAddr를 사용해서 함수의 주소를 얻어와서 사용해야 됩니다.

```
VkResult CreateDebugUtilsMessengerEXT(
    VkInstance instance,
    const VkDebugUtilsMessengerCreateInfoEXT* pCreateInfo,
    const VkAllocationCallbacks* pAllocator,
    VkDebugUtilsMessengerEXT* pDebugMessenger
) {
    auto func = (PFN_vkCreateDebugUtilsMessengerEXT)
        vkGetInstanceProcAddr(instance, "vkCreateDebugUtilsMessengerEXT");

    if (func != nullptr) {
        return func(instance, pCreateInfo, pAllocator, pDebugMessenger);
    } else {
        return VK_ERROR_EXTENSION_NOT_PRESENT;
    }
}
```

디버그 메신저는 **특정 인스턴스에 종속되므로**, 인스턴스를 첫 번째 인자로 명시해줘야합니다.

### Destroy Debugmessenger

생성한 VkDebugUtilsMessengerEXT 객체는 프로그램 종료 시 **명시적으로 제거해야 합니다.**

```
	void DestroyDebugUtilsMessengerEXT(VkInstance instance,
		VkDebugUtilsMessengerEXT debugMessenger,
		const VkAllocationCallbacks* pAllocator)
	{
		auto func = (PFN_vkDestroyDebugUtilsMessengerEXT)vkGetInstanceProcAddr(instance, "vkDestroyDebugUtilsMessengerEXT");

		if (func != nullptr)
		{
			func(instance, debugMessenger, pAllocator);
		}
	}
```

### Debugging instance creation and destruction

지금까지 validation layers를 통해 디버깅 기능을 추가했지만, 모든 상황을 커버한 것은 아닙니다.

vkCreateDebugUtilsMessengerEXT는 instance 생성 이후에 호출 가능하고,

vkCreateDebugUtilsMessengerEXT는 instance 소멸 이전에 먼저 소멸되야합니다.

**vkCreateInstance** 또는 **vkDestroyInstance** 자체에 문제가 생기면 디버깅할 방법이 없습니다..!

VkInstanceCreateInfo 구조체의 pNext 필드에  
VkDebugUtilsMessengerCreateInfoEXT 구조체의 포인터를 전달하는 방법으로 해결가능합니다.

```
void createInstance()
{
//...
    VkDebugUtilsMessengerCreateInfoEXT debugCreateInfo{}; 
    if (enableValidationLayers) {
        createInfo.enabledLayerCount = static_cast<uint32_t>(validationLayers.size());
        createInfo.ppEnabledLayerNames = validationLayers.data();

        populateDebugMessengerCreateInfo(debugCreateInfo);
        createInfo.pNext = (VkDebugUtilsMessengerCreateInfoEXT*)&debugCreateInfo;
    }
    else {
        createInfo.enabledLayerCount = 0;
        createInfo.pNext = nullptr;
    } 
    VkResult result = vkCreateInstance(&createInfo, nullptr, &instance); 
    if (vkCreateInstance(&createInfo, nullptr, &instance) != VK_SUCCESS) {
        throw std::runtime_error("failed to create instance!");
    }
    
//...
}
```

이제

Validation layer가 잘 작동하는 지 테스트 하기 위해서

debug messenger를 destroy하는 함수를 주석처리해 줬습니다.

우리는 mainloop가 무한 루프니까 그부분은 주석처리하고 테스트하면 됩니다.

```
void cleanup()
{
	if (enableValidationLayers)
	{
		//DestroyDebugUtilsMessengerEXT(instance, debugMessenger, nullptr);
	}

	vkDestroyInstance(instance, nullptr);
	
	glfwDestroyWindow(window);
	glfwTerminate(); 
}
```

아래와 같이 destroy안했어!! 라고 알려주는 모습입니다!

![](https://blog.kakaocdn.net/dna/cIUbf2/btsNensNHsV/AAAAAAAAAAAAAAAAAAAAAC50-_x5twPWb6kUVNG1P928jIElga4fIJzHffkH_J98/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=mA%2B6Rnh9eRYn2Nd4Q2AciEao4HM%3D)

### Physical Device & Queue Families

위에서 만들어준 instance를 통해 Vulkan 라이브러리를 초기화한 후에 필요한 기능을 지원하는 device( GPU )를 찾아서 select해야 됩니다.

여러 개의 GPU를 동시에 선택하고 사용할 수도 있지만, 여기서는 첫 번째 그래픽 카드만 사용할 것입니다.

클래스 안에서 GPU를 저장할 VkPhysicalDevice를 선언하고,

이전에 했던 것과 동일하게 GPU를 찾아서 저장해줍니다.

```
//physical device
VkPhysicalDevice physicalDevice = VK_NULL_HANDLE;


void pickPhysicalDevice()
{
    uint32_t deviceCount = 0;
    vkEnumeratePhysicalDevices(instance, &deviceCount, nullptr);

    if (deviceCount == 0)
    {
        throw std::runtime_error("failed to find GPUs with Vulkan support!");
    }

    std::vector<VkPhysicalDevice> devices(deviceCount);
    vkEnumeratePhysicalDevices(instance, &deviceCount, devices.data());

}
```

GPU가 모두 동일한 것이 아니기 때문에 우리의 조건에 맞는 것을 찾아야합니다.

순회하면서 isDeviceSuitable로 원하는 GPU를 찾는 코드이다.

```
void pickPhysicalDevice()
{
    uint32_t deviceCount = 0;
    vkEnumeratePhysicalDevices(instance, &deviceCount, nullptr);

    if (deviceCount == 0)
    {
        throw std::runtime_error("failed to find GPUs with Vulkan support!");
    }

    std::vector<VkPhysicalDevice> devices(deviceCount);
    vkEnumeratePhysicalDevices(instance, &deviceCount, devices.data());

    for (const auto& device : devices)
    {
        if (isDeviceSuitable(device))
        {
            physicalDevice = device;
            break;
        }
    }

    if (physicalDevice == VK_NULL_HANDLE)
    {
        throw std::runtime_error("failed to find a suitable GPU!");
    }
}

bool isDeviceSuitable(VkPhysicalDevice device)
{
    return true;
}
```

isDeviceSuitable을 채워봅시다.

예를 들어, 우리 애플리케이션이 **전용(Discrete) 그래픽 카드이면서 지오메트리 셰이더를 지원하는 GPU만 사용**한다고 가정해서 코드를 작성했습니다.

```
bool isDeviceSuitable(VkPhysicalDevice device)
{
    VkPhysicalDeviceProperties deviceProperties;
    VkPhysicalDeviceFeatures deviceFeatures;
    vkGetPhysicalDeviceProperties(device, &deviceProperties);
    vkGetPhysicalDeviceFeatures(device, &deviceFeatures);

	// Descrete && gemoetry shader
    return deviceProperties.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU &&
        deviceFeatures.geometryShader;

}
```

위의 코드와 같이 필요한 것을 가지고 있는 지만 체크할 수 있고, **각 GPU에 점수를 매긴 뒤 가장 높은 점수를 가진 GPU를 선택**할 수도 있습니다.

아래의 방식은 원하는 조건의 GPU에 점수를 주면서, 가장 높은 점수를 받은 GPU를 최종적으로 선택하는 방법입니다.

```
void pickPhysicalDevice()
{
    uint32_t deviceCount = 0;
    vkEnumeratePhysicalDevices(instance, &deviceCount, nullptr);

    if (deviceCount == 0)
    {
        throw std::runtime_error("failed to find GPUs with Vulkan support!");
    }

    std::vector<VkPhysicalDevice> devices(deviceCount);

    //	vkEnumeratePhysicalDevices(instance, &deviceCount, devices.data());
    std::multimap<int, VkPhysicalDevice> candidates;

    for (const auto& device : devices)
    {
        int score = rateDeviceSuitability(device);
        candidates.insert(std::make_pair(score, device));
    }

    if (candidates.rbegin()->first > 0)
    {
        physicalDevice = candidates.rbegin()->second;
    }
    else
    {
        throw std::runtime_error("failed to find a suitable GPU!!");
    }
}

int rateDeviceSuitability(VkPhysicalDevice device)
{
    VkPhysicalDeviceProperties deviceProperties;
    VkPhysicalDeviceFeatures deviceFeatures;

    vkGetPhysicalDeviceProperties(device, &deviceProperties);
    vkGetPhysicalDeviceFeatures(device, &deviceFeatures);

    int score = 0;

    // 전용 GPU이면 보너스 점수
    if (deviceProperties.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU) {
        score += 1000;
    }

    // 최대 텍스처 크기에 따라 점수 추가
    score += deviceProperties.limits.maxImageDimension2D;

    // 지오메트리 셰이더를 지원하지 않으면 0점 처리
    if (!deviceFeatures.geometryShader) {
        return 0;
    }

    return score;


}
```

일단 여기서는 return true로 하고, 뒤에서 조건을 추가해봅시다.

```
bool isDeviceSuitable(VkPhysicalDevice device) {
    return true;
}
```

### Queue Family

Vulkan에서는 그림을 그리던 텍스처를 업로드하던 대부분의 작업을 Queue를 통해서 이루어집니다.

서로 다른 type의 Queue들은 서로 다른 Queue Family에서 파생되며, 각 Queue family에 맞는 특정 명령들만 허용합니다.

예를 들어 어떤 queue family는  계산 작업만 처리하고, 다른 queue family는 memory transfer 작업만 처리할 수 있습니다.

그렇기 때문에 우리가 원하는 명령을 처리할 수 있는 Queue family가 있는지 확인해야 됩니다.  
이를 위해 findQueueFamilies라는 함수를 만들어서 필요한 큐 패밀리를 검색합시다.

지금 필요한 것은 graphics Queue Family이지만, 나중에 여러 종류가 필요할 수 있으니 구조체로 빼서 정의합시다.

```
struct QueueFamilyIndices {
	uint32_t graphicsFamily;
};

// .... . . 

uint32_t graphicsFamily
```

여기서 uint32\_t에 어떤 값이 저장되든 graphicsFamily가 index 0까지 사용한다고 하면 queue를 못찾았을 경우를 판별할 때 헷갈릴 수 있습니다.

그래서 C++17에서 등장한 std::optional 문법을 사용해줍시다. 값의 존재여부를 has\_value()로 알 수 있습니다.

아래는 문법 예시입니다.

```
#include <optional>

std::optional<uint32_t> graphicsFamily;

std::cout << std::boolalpha << graphicsFamily.has_value() << std::endl; // false

graphicsFamily = 0;

std::cout << std::boolalpha << graphicsFamily.has_value() << std::endl; // true
```

QueueFamily의 구조체도 아래와 같이 바꿔줍시다.

```
struct QueueFamilyIndices {
    std::optional<uint32_t> graphicsFamily;
};

QueueFamilyIndices findQueueFamilies(VkPhysicalDevice device) {
    QueueFamilyIndices indices;
    // 찾은 큐 패밀리 인덱스를 여기에 할당
    return indices;
}
```

우리가 지금까지 계속 사용했던 방법으로 Queue Family를 찾아줍니다.

```
uint32_t queueFamilyCount = 0;
vkGetPhysicalDeviceQueueFamilyProperties(device, &queueFamilyCount, nullptr);

std::vector<VkQueueFamilyProperties> queueFamily(queueFamilyCount);
vkGetPhysicalDeviceQueueFamilyProperties(device, &queueFamilyCount, queueFamily.data());
```

VkQueueFamilyProperties에는 queue family의 type을 나타내는 정보가 있습니다.

이를 확인해서 graphics Family를 찾을 것입니다.

(VK\_QUEUE\_GRAPHICS\_BIT가 Graphics Queue를 의미합니다.)

아래와 같이 flag를 체크해서 원하는 queue family를 찾을 수 있습니다.

```
QueueFamilyIndices findQueueFamilies(VkPhysicalDevice device)
{
	QueueFamilyIndices indices;
	  
    //...
	
    int i = 0;
	for (const auto& queueFamily : queueFamilies)
	{
		if (queueFamily.queueFlags & VK_QUEUE_GRAPHICS_BIT)
		{
			indices.graphicsFamily = i;
		}  
		i++;
	}


	return indices;
}
```

이제 유효성 검사까지 추가해주면 됩니다.

```
struct QueueFamilyIndices {
	std::optional<uint32_t> graphicsFamily;

	bool isComplete()
	{
		return graphicsFamily.has_value();
	}
};

// ....
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
		} 

		if (indices.isComplete())
		{
			break;
		}

		i++;
	}


	return indices;
}

bool isDeviceSuitable(VkPhysicalDevice device)
{
	QueueFamilyIndices indices = findQueueFamilies(device);

	return indices.isComplete();
}
```

아까 return true;로 하고 넘어간 isDeviceSuitable에 QueueFamily를 찾는 함수를 추가해줍니다.

선택한 device에 graphics queue family를 지원하는지 확인하고 선택하는 느낌입니다.

## Logical Device and Queue

physical device를 선택한 후에는 그 device와 상호작용할 logical device를 설정해야됩니다.

logical device를 생성할 때는 사용하고자 하는 features들을 명시해야됩니다.

그리고 원하는 Queue Family를 지정했으니, 특정 queue도 지정해야됩니다.

(원하는 것 하나하나 골라서 선택하는게,,, vulkan입니다. 하하하)

하나의 physical device에 여러개의 logical device를 생성할 수 있습니다.

logical device를 저장할 멤버 변수를 클래스에 추가하고,

생성할 함수를 추가해줍시다.

```
VkDevice device;

void initVulkan() {
    createInstance();
    setupDebugMessenger();
    pickPhysicalDevice();
    createLogicalDevice();
}

void createLogicalDevice() {
    // 구현 내용은 아래에서 다룸
}
```

QueueFamily에서 원하는 Queue를 가져오 위해서 설정할 것이 많습니다.

첫 번째로 설정할 것은 VkDeviceQueueCreateInfo입니다.

한개의 QueueFamily에서 몇개의 Queue를 가져올 지 설정하는 것입니다.

아래는 graphics Queue를 1개 가져온다는 코드입니다.

```
void createLogicalDevice()
{
    QueueFamilyIndices indices = findQueueFamilies(physicalDevice);

    VkDeviceQueueCreateInfo queueCreateInfo{};
    queueCreateInfo.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
    queueCreateInfo.queueFamilyIndex = indices.graphicsFamily.value();
    queueCreateInfo.queueCount = 1;

}
```

최신 드라이버는 하나의 Queue Family에서 적은 수의 queue 가져가도록 만들어져있습니다.

실제로 작업할 때에도 1개의 queue로도 충분합니다.

왜냐하면 command buffer들을 여러 쓰레드를 생성하고, 메인 쓰레드에 queue를 통해 한 번에 submit합니다.

이런 구조 때문에 queue를 여러개 만든다면  queue마다의 동기화를 신경써야됩니다.

그렇기 때문에 queue를 적게 사용하는 것을  권장합니다.

### Queue의 priority(우선순위) 설정

Vulkan에서는 **Queue의 우선순위를 부동소수점 값(0.0 ~ 1.0)** 으로 설정할 수 있습니다. Queue가 1개일 때도 설정해줘야됩니다.

```
float queuePriority = 1.0f;
queueCreateInfo.pQueuePriorities = &queuePriority;
```

### Deivce Feature 정하기

vkGetPhysicalDeviceFeatures를 통해 GPU가 지원하는지 확인했던 것들로, 예를 들어 **지오메트리 셰이더(geometry shaders)** 같은 기능들이 여기에 해당됩니다.

현재 단계에서는 특별히 필요한 기능이 없기 때문에,  
다음과 같이 모든 값을 VK\_FALSE로 초기화하면 됩니다.

나중에 Vulkan에서 더 재밌는 작업을 하게 될 때 이 구조체를 다시 다루겠습니다.

```
VkPhysicalDeviceFeatures deviceFeatures{};
```

### Create Logical Device

위에서 설정한 VkDeviceQueueCreateInfo, VkPhysicalDeviceFeatures를 바탕으로 Logical Device를 만드는 코드입니다.

```
VkDeviceCreateInfo createInfo{};
createInfo.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;

createInfo.pQueueCreateInfos = &queueCreateInfo;
createInfo.queueCreateInfoCount = 1;

createInfo.pEnabledFeatures = &deviceFeatures;
```

### Extension & Validation Layer

이후 설정들은 Instance를 만들 때와 비슷하지만,

device전용으로 extesion(확장), validation layer를 지정해야됩니다.

**Extension**

예를 들어 VK\_KHR\_swapchain은 렌더링한 이미지를 윈도우에 띄우는 Device extension이다.

어떤 device는 이 extension을 지원하지 않을 수 있습니다.

예를 들면 compute only GPU는 화면 출력 기능이 없습니다. 그렇기 때문에 직접 extension을 지정해줘야합니다.

**Validation layer**

Vulkan 초반에는 instance와 device 각각에 대해서 validation layer를 개별적으로 지정했지만, 최신 버전에서는 구분하지 않습니다.

즉, VkDeviceCreateInfo의 enabledLayerCount와 ppEnabledLayerNames는  
최신 구현에서는 무시되지만, 구형 시스템과의 **호환성을 위해 여전히 설정해 두는 것이 좋습니다.**

```
createInfo.enabledExtensionCount = 0;

if (enableValidationLayers)
{
    createInfo.enabledLayerCount = static_cast<uint32_t>(validationLayers.size());
    createInfo.ppEnabledLayerNames = validationLayers.data();
}

else
{
    createInfo.enabledLayerCount = 0;
}
```

이제 vkCreateDevice를 사용해서 logical device를 만들어주면 된다.

```
if (vkCreateDevice(physicalDevice, &createInfo, nullptr, &device) != VK_SUCCESS)
{
    throw std::runtime_error("failed to create logical device!");
}
```

이 함수도 인스턴스 생성과 마찬가지로,  
**존재하지 않는 확장**을 활성화하려 하거나  
**지원하지 않는 기능**을 지정하면 실패할 수 있습니다.

### Retrieving Queue Handles( Queue Handles 얻어오기)

**queue 자체는 logical device를 만들 때 함께 생성**됩니다. 하지만 queue와 상호작용할 수 있는 **handle은 따로 만들어줘야합니다.**

우선 handle를 저장할 변수를 클래스 멤버 변수로 추가합시다.

```
VkQueue graphicsQueue;
```

**handle은 queue가 destroy될 때, implicitly(암묵적으로)하게 같이 destroy**됩니다.

vkGetDeviceQueue를 사용해서 handle을 가져온다.

우리는 queue를 1개만 사용하니까 index를 0으로해서 queue handle을 만들어주었다.

```
vkGetDeviceQueue(device, indices.graphicsFamily.value(), 0, &graphicsQueue);
```

### 

### Destroy Logical Device

logical device 역시 프로그램이 끝날 때 destroy해줘야됩니다.

```
void cleanup() {
    vkDestroyDevice(device, nullptr);
}
```

Logical Device는 Instance와 **직접적으로 연결되지는 않습니다.**  
따라서 vkCreateDevice() 호출 시 intance를 별도로 전달할 필요가 없다.

이제 logical device & queue handle까지 설정했습니다.

드디어 GPU를 사용해 **실제 작업을 수행할 수 있는 준비가 완료된 것입니다.**