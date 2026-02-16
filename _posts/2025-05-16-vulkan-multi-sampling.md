---
title: "[Vulkan] Multi Sampling"
date: 2025-05-16
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

## Multisampling

우리 프로그램은 이제 텍스처에 대해 여러 수준의 디테일(Level of Detail)을 로드할 수 있게 되었고, 이는 먼 거리에서 객체를 렌더링하건, 해상도가 낮은 상황에서 발생하는 아티팩트를 개선해 줍니다.

결과적으로 이미지는 훨씬 더 부드러워졌지만, 자세히 들여다보면 기하학 도형의 가장자리에 톱니 모양의 들쭉날쭉한 패턴이 여전히 나타나는 것을 확인할 수 있습니다.

아래 이미지로 보면 이해가 잘될겁니다.

![](https://blog.kakaocdn.net/dna/HNfTN/btsNX0R3mJC/AAAAAAAAAAAAAAAAAAAAAC5_PTejNVDT0VfdBM8s0FCcsnNg_JB7G1lBd6jjv6w7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=I3w%2FqmbmggYbBvKhs36lkU5%2BcXo%3D)

이러한 원치 않는 효과는 Aliasing이라고 하며, 이는 화면에 렌더링할 수 있는 픽셀 수가 제한되어 있기 때문에 발생합니다.

이를 해결하기 위한 여러 방법들이 있으며, 이번 장에서는 그 중 하나인 **Multi Sample Anti Aliasing(MSAA)을 알아볼 것입니다.**

일반적인 렌더링에서는 픽셀의 색상을 단일 샘플 지점(보통은 픽셀 중심)을 기준으로 결정합니다. 만약 그리는 선이 특정 픽셀을 통과하더라도 그 샘플 지점을 포함하지 않으면, 해당 픽셀은 공백으로 남게 되어 **계단현상**이 발생합니다.

**MSAA는 픽셀당 여러 개의 샘플 포인트를 사용하여 최종 색상을 결정합니다. 당연히 샘플 수가 많을수록 결과는 더 부드럽지만, 계산 비용도 더 커집니다.**

![](https://blog.kakaocdn.net/dna/bujGWl/btsNYjwVBfr/AAAAAAAAAAAAAAAAAAAAAHXDxvlx5RDml46UqnOH4--rBPxHRoMRgoVP8C6Li0IP/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Y%2F1DBN7AwLlEsEiJdnUMOHB1pz4%3D)![](https://blog.kakaocdn.net/dna/ch6Ph4/btsNYpKJZlw/AAAAAAAAAAAAAAAAAAAAAFAkI7xp2A7Lil-MOA2h9eOfEzf9Ce6DIotCTEE-y7kY/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=YlHV1izwddjFIkHgwEx5g7GooKs%3D)

이번 구현에서는 **사용 가능한 최대 샘플 수**를 사용하는 것에 초점을 맞출 예정입니다. 하지만 실제 응용 프로그램에서는 품질 요구를 충족할 수 있다면 더 적은 샘플 수를 선택하여 성능을 높이는 것이 더 나을 수도 있습니다.

### Getting available sample count

먼저, 하드웨어가 지원하는 최대 샘플 수를 알아봐야 합니다. 대부분의 최신 GPU는 최소 8개의 샘플을 지원하지만, 이 수치는 하드웨어에 따라 달라질 수 있으므로 확인이 필요합니다. 이를 추적하기 위해 클래스 멤버 변수를 하나 추가해줍니다:

```
VkSampleCountFlagBits msaaSamples = VK_SAMPLE_COUNT_1_BIT;
```

**기본적으로는 픽셀당 하나의 샘플만 사용하며, 이는 멀티샘플링이 적용되지 않은 상태와 동일합니다.**

사용 가능한 최대 샘플 수는 선택된 VkPhysicalDevice에 연결된 VkPhysicalDeviceProperties로부터 얻을 수 있습니다.

우리는 색상 버퍼와 깊이 버퍼를 모두 사용하고 있기 때문에, **두 버퍼 모두에서 지원되는 샘플 수를 고려**해야 하며, 둘 중 **공통으로 지원되는 가장 높은 샘플 수**를 선택해야 합니다.

```
VkSampleCountFlagBits getMaxUsableSampleCount() {
    VkPhysicalDeviceProperties physicalDeviceProperties;
    vkGetPhysicalDeviceProperties(physicalDevice, &physicalDeviceProperties);

    VkSampleCountFlags counts =
        physicalDeviceProperties.limits.framebufferColorSampleCounts &
        physicalDeviceProperties.limits.framebufferDepthSampleCounts;

    if (counts & VK_SAMPLE_COUNT_64_BIT) { return VK_SAMPLE_COUNT_64_BIT; }
    if (counts & VK_SAMPLE_COUNT_32_BIT) { return VK_SAMPLE_COUNT_32_BIT; }
    if (counts & VK_SAMPLE_COUNT_16_BIT) { return VK_SAMPLE_COUNT_16_BIT; }
    if (counts & VK_SAMPLE_COUNT_8_BIT)  { return VK_SAMPLE_COUNT_8_BIT;  }
    if (counts & VK_SAMPLE_COUNT_4_BIT)  { return VK_SAMPLE_COUNT_4_BIT;  }
    if (counts & VK_SAMPLE_COUNT_2_BIT)  { return VK_SAMPLE_COUNT_2_BIT;  }

    return VK_SAMPLE_COUNT_1_BIT;
}
```

이제 위 함수를 활용하여 pickPhysicalDevice 함수에서 physical device를 선택할 때 msaaSamples 값을 설정합니다.

```
void pickPhysicalDevice() {
    ...
    for (const auto& device : devices) {
        if (isDeviceSuitable(device)) {
            physicalDevice = device;
            msaaSamples = getMaxUsableSampleCount();
            break;
        }
    }
}
```

### Setting up a render target

MSAA에서는 각 픽셀이 offscreen buffer에서 샘플링되고, 그 결과가 최종적으로 화면에 렌더링됩니다.

**offscreen buffer는 각 픽셀마다 여러 개의 샘플을 저장할 수 있어야 하기 때문에** **지금까지 사용했던 일반 이미지와는 조금 다릅니다.** 

**멀티샘플 버퍼가 생성된 후에는, 이를 단일 샘플만 저장할 수 있는 기본 프레임버퍼(default framebuffer)로 리졸브(resolve) 해야 합니다.**

그렇기 때문에 기존의 렌더링 과정을 다음과 같이 변경해야됩니다.

* 하나의 추가 렌더 타겟을 생성해야 합니다.
* 그에 따른 드로우 작업 과정도 수정해야 합니다.

깊이 버퍼(depth buffer)처럼, 우리는 한 번에 하나의 드로잉 작업만 활성화되므로 **렌더 타겟은 하나만** 필요합니다.

```
VkImage colorImage;
VkDeviceMemory colorImageMemory;
VkImageView colorImageView;
```

이 새 이미지 객체는 **픽셀당 여러 샘플을 저장해야 하므로**, VkImageCreateInfo 구조체를 생성할 때 샘플 수를 지정해줘야 합니다. 이를 위해 createImage 함수에 **numSamples 매개변수를 추가**합시다.

```
void createImage(uint32_t width, uint32_t height, uint32_t mipLevels,
                 VkSampleCountFlagBits numSamples, VkFormat format,
                 VkImageTiling tiling, VkImageUsageFlags usage,
                 VkMemoryPropertyFlags properties, VkImage& image,
                 VkDeviceMemory& imageMemory)
{
    ...
    imageInfo.samples = numSamples;
    ...
}
```

당장은 함수를 호출하는 모든 부분에서 샘플 수를 VK\_SAMPLE\_COUNT\_1\_BIT로 설정해 두고, 이후 구현이 완료되면 적절한 값으로 대체합시다.

```
createImage(swapChainExtent.width, swapChainExtent.height, 1,
            VK_SAMPLE_COUNT_1_BIT, depthFormat, VK_IMAGE_TILING_OPTIMAL,
            VK_IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT,
            VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT, depthImage,
            depthImageMemory);

createImage(texWidth, texHeight, mipLevels, VK_SAMPLE_COUNT_1_BIT,
            VK_FORMAT_R8G8B8A8_SRGB, VK_IMAGE_TILING_OPTIMAL,
            VK_IMAGE_USAGE_TRANSFER_SRC_BIT |
            VK_IMAGE_USAGE_TRANSFER_DST_BIT |
            VK_IMAGE_USAGE_SAMPLED_BIT,
            VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT, textureImage,
            textureImageMemory);
```

다음으로는 multi sample buffer를 생성합니다. createColorResources 함수를 작성하며, 여기서 msaaSamples 값을 createImage에 전달합니다. 그리고 Vulkan specification( 요구사항(?)  )에 따라 멀티샘플 이미지는 mip level을 1로 고정해야됩니다. ( 어차피 텍스처로 사용되지 않기 때문에 mipmap은 필요 없습니다.)

```
void createColorResources() {
    VkFormat colorFormat = swapChainImageFormat;

    createImage(swapChainExtent.width, swapChainExtent.height, 1,
                msaaSamples, colorFormat, VK_IMAGE_TILING_OPTIMAL,
                VK_IMAGE_USAGE_TRANSIENT_ATTACHMENT_BIT |
                VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT,
                VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT, colorImage,
                colorImageMemory);

    colorImageView = createImageView(colorImage, colorFormat,
                                     VK_IMAGE_ASPECT_COLOR_BIT, 1);
}
```

이제 깊이 버퍼도 멀티샘플을 사용할 수 있도록 createDepthResources 함수의 샘플 수를 수정합니다:

```
void createDepthResources() {
    ...
    createImage(swapChainExtent.width, swapChainExtent.height, 1,
                msaaSamples, depthFormat, VK_IMAGE_TILING_OPTIMAL,
                VK_IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT,
                VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT, depthImage,
                depthImageMemory);
    ...
}
```

이 함수를 createDepthResources 함수 호출 직전에 추가합니다.

```
void initVulkan() {
    ...
    createColorResources();
    createDepthResources();
    ...
}
```

새로 생성한 Vulkan 리소스를 메모리 누수 없이 정리할 수 있도록 cleanupSwapChain 함수에 다음 내용을 추가합니다.

```
void cleanupSwapChain() {
    vkDestroyImageView(device, colorImageView, nullptr);
    vkDestroyImage(device, colorImage, nullptr);
    vkFreeMemory(device, colorImageMemory, nullptr);
    ...
}​
```

또한, 창 크기 변경 시 새 컬러 이미지를 새 크기에 맞게 다시 생성할 수 있도록 recreateSwapChain에 다음 호출을 추가합니다.

```
void recreateSwapChain() {
    ...
    createImageViews();
    createColorResources();
    createDepthResources();
    ...
}
```

### Adding new attachments

먼저 Render Pass부터 수정하겠습니다.

createRenderPass 함수에서  
colorAttachment의 sample수와, finalLayout을 변경해줍니다.   
depthAttachment의 sample수도 변경합니다.

```
colorAttachment.samples = msaaSamples;
colorAttachment.finalLayout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;

depthAttachment.samples = msaaSamples;
```

 finalLayout을 VK\_IMAGE\_LAYOUT\_PRESENT\_SRC\_KHR에서  
VK\_IMAGE\_LAYOUT\_COLOR\_ATTACHMENT\_OPTIMAL로 바꿨습니다.  
**멀티샘플링된 이미지는 직접 스왑체인으로 화면에 띄울 수 없기 때문에** 반드시 일반 단일 샘플 이미지로 **resolve(해결)** 해야만 화면에 표시가 가능합니다.

(깊이 버퍼는 화면에 표시되지 않으므로 이 제한이 적용되지 않습니다.)

그렇기 때문에 **resolve attachment라는** 컬러 버퍼용 새로운 attachment를 하나 추가해야 합니다.

```
VkAttachmentDescription colorAttachmentResolve{};
colorAttachmentResolve.format = swapChainImageFormat;
colorAttachmentResolve.samples = VK_SAMPLE_COUNT_1_BIT;
colorAttachmentResolve.loadOp = VK_ATTACHMENT_LOAD_OP_DONT_CARE;
colorAttachmentResolve.storeOp = VK_ATTACHMENT_STORE_OP_STORE;
colorAttachmentResolve.stencilLoadOp = VK_ATTACHMENT_LOAD_OP_DONT_CARE;
colorAttachmentResolve.stencilStoreOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;
colorAttachmentResolve.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
colorAttachmentResolve.finalLayout = VK_IMAGE_LAYOUT_PRESENT_SRC_KHR;
```

### 

렌더 패스가 멀티샘플링된 컬러 이미지를 단일 샘플 버퍼로 resolve 하도록 지시하려면  
해당 resolve 타겟을 가리키는 **Attachment Reference**를 생성해야 합니다:

```
VkAttachmentReference colorAttachmentResolveRef{};
colorAttachmentResolveRef.attachment = 2; // resolve attachment index
colorAttachmentResolveRef.layout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;​
```

그리고 이를 서브패스(Subpass)에 연결합니다:

```
subpass.pResolveAttachments = &colorAttachmentResolveRef;
```

이렇게 하면 이 서브패스는 **렌더링 시 자동으로 멀티샘플링 이미지를 일반 이미지로 resolve** 하게 됩니다.

이제 VkRenderPassCreateInfo에 전달할 attachment 목록도 새롭게 구성해야 합니다:

```
std::array<VkAttachmentDescription, 3> attachments = {
    colorAttachment,
    depthAttachment,
    colorAttachmentResolve
};
```

createFramebuffers 함수도 수정하여 새로운 컬러 이미지 뷰를 프레임버퍼에 포함시켜야 합니다.

```
std::array<VkImageView, 3> attachments = {
    colorImageView,        // 멀티샘플 컬러 이미지
    depthImageView,        // 깊이 이미지
    swapChainImageViews[i] // resolve 타겟 이미지
};
```

```
multisampling.rasterizationSamples = msaaSamples;
```

이제 파이프라인에도 멀티샘플링을 적용하도록 createGraphicsPipeline 함수를 수정합니다:

```
void createGraphicsPipeline() {
//...
	multisampling.rasterizationSamples = msaaSamples;
//...
}
```

이제 프로그램을 실행하면, **이전보다 가장자리의 톱니 현상이 줄어든** 것을 확인할 수 있습니다.

![](https://blog.kakaocdn.net/dna/brDuc5/btsNXCYm7Jc/AAAAAAAAAAAAAAAAAAAAAA3CanEVCZidRjMhso9OoVtYiHwcYXIXOXsSVNCr4x7r/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=pe4QRnvvI6OufVNsdjZJ%2BWgTnZg%3D)![](https://blog.kakaocdn.net/dna/HNfTN/btsNX0R3mJC/AAAAAAAAAAAAAAAAAAAAAC5_PTejNVDT0VfdBM8s0FCcsnNg_JB7G1lBd6jjv6w7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=I3w%2FqmbmggYbBvKhs36lkU5%2BcXo%3D)

## Quality Improvements

현재 우리가 구현한 MSAA는 일부 **제한점**이 있으며, 복잡한 장면에서 출력 이미지의 품질에 영향을 줄 수 있습니다. 예를 들어, **셰이더 앨리어싱(Shader Aliasing)** 문제는 아직 해결되지 않았습니다.

MSAA는 **기하학적인 가장자리를 부드럽게 만들어주는 역할**만 수행하고, **오브젝트 내부의 픽셀**에는 영향을 주지 않습니다.  
이로 인해, 예를 들어 다각형의 외곽선은 부드럽게 렌더링되지만,  
**대비가 큰 텍스처**가 적용되면 여전히 거칠고 들쭉날쭉하게 보일 수 있습니다..

이 문제를 해결할 수 있는 방법 중 하나는 **Sample Shading** 기능을 활성화하는 것입니다.  
이는 각 샘플별로 **프래그먼트 셰이더를 평가**하게 하여 이미지 품질을 더욱 개선할 수 있지만,**비용**이 증가합니다

```
void createLogicalDevice() {
    ...
    deviceFeatures.sampleRateShading = VK_TRUE; // 장치에 샘플 셰이딩 기능 활성화
    ...
}

void createGraphicsPipeline() {
    ...
    multisampling.sampleShadingEnable = VK_TRUE; // 파이프라인에서 샘플 셰이딩 활성화
    multisampling.minSampleShading = 0.2f;       // 샘플 셰이딩이 적용될 최소 비율 (1에 가까울수록 부드러움)
    ...
}
```

이 예제에서는 성능상 이유로 Sample Shading을 **비활성화** 상태로 둘 예정이지만,  
**특정 상황에서는 이미지 품질이 눈에 띄게 향상**될 수 있습니다.

여기까지 오는 데 많은 작업이 필요했지만, 이제 우리는 **Vulkan 기반 프로그램의 견고한 베이스**를 갖추었습니다!!

Vulkan은 매우 **명시적인(explicit)** API이긴 하지만, 많은 렌더링 개념들은 다른 그래픽 API들과 **본질적으로 동일**합니다.  
따라서 OpenGL이나 DirectX 기반의 튜토리얼을 참고하여도 충분히 이해하고 확장할 수 있을 것입니다.

라고 합니다... 막막하지만,,,, 계속 공부하고 글 올리겠습니다! 저도 헤딩해야되서 주기가 늦어질 수 있습니다.

(다음 파트는 compute shader인데, 지금 당장 사용할 일은 없을 것 같아서,

openGL, DX로 구현했던 다른 graphic 이론들을 Vulkan에서 해보겠습니닷)