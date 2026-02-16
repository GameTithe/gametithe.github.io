---
title: "[Vulkan] Depth Buffer"
date: 2025-05-15
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

이번 장에서는 Z 좌표를 도입하여 3D mesh를 위한 기반을 마련해봅시다.

3D Geometry

먼저 Vertex position을 vec2 position을 사용중이였는데, 이제 vec3로 변경해봅시다.

```
struct Vertex {
    glm::vec3 pos;
    glm::vec3 color;
    glm::vec2 texCoord;

    static std::array<VkVertexInputAttributeDescription, 3> getAttributeDescriptions() {
        std::array<VkVertexInputAttributeDescription, 3> attributeDescriptions{};

        attributeDescriptions[0].binding = 0;
        attributeDescriptions[0].location = 0;
        attributeDescriptions[0].format = VK_FORMAT_R32G32B32_SFLOAT;
        attributeDescriptions[0].offset = offsetof(Vertex, pos);

        ...
    }
};
```

이제 vertex shader도 수정해줍시다. 수정 후 shader는 반드시 재컴파일해야 합니다!

```
layout(location = 0) in vec3 inPosition;

...

void main() {
    gl_Position = ubo.proj * ubo.view * ubo.model * vec4(inPosition, 1.0);
}
```

기존 vertex position의 z 값은 0.0f으로 초기화합시다.

```
const std::vector<Vertex> vertices = {
    {{-0.5f, -0.5f, 0.0f}, {1.0f, 0.0f, 0.0f}, {0.0f, 0.0f}},
    {{ 0.5f, -0.5f, 0.0f}, {0.0f, 1.0f, 0.0f}, {1.0f, 0.0f}},
    {{ 0.5f,  0.5f, 0.0f}, {0.0f, 0.0f, 1.0f}, {1.0f, 1.0f}},
    {{-0.5f,  0.5f, 0.0f}, {1.0f, 1.0f, 1.0f}, {0.0f, 1.0f}}
};​
```

이렇게 고쳐도 아직 이전과 동일한 결과가 출력될 것입니다.

이제 장면에 새로운 사각형을 추가해봅시다.

기존 사각형 아래쪽에 새로운 사각형을 배치하기 위해 Z 좌표를 -0.5f로 설정합니다:

```
const std::vector<Vertex> vertices = {
    // 위쪽 사각형
    {{-0.5f, -0.5f,  0.0f}, {1.0f, 0.0f, 0.0f}, {0.0f, 0.0f}},
    {{ 0.5f, -0.5f,  0.0f}, {0.0f, 1.0f, 0.0f}, {1.0f, 0.0f}},
    {{ 0.5f,  0.5f,  0.0f}, {0.0f, 0.0f, 1.0f}, {1.0f, 1.0f}},
    {{-0.5f,  0.5f,  0.0f}, {1.0f, 1.0f, 1.0f}, {0.0f, 1.0f}},
    
    // 아래쪽 사각형
    {{-0.5f, -0.5f, -0.5f}, {1.0f, 0.0f, 0.0f}, {0.0f, 0.0f}},
    {{ 0.5f, -0.5f, -0.5f}, {0.0f, 1.0f, 0.0f}, {1.0f, 0.0f}},
    {{ 0.5f,  0.5f, -0.5f}, {0.0f, 0.0f, 1.0f}, {1.0f, 1.0f}},
    {{-0.5f,  0.5f, -0.5f}, {1.0f, 1.0f, 1.0f}, {0.0f, 1.0f}}
};

const std::vector<uint16_t> indices = {
    0, 1, 2, 2, 3, 0,   // 위쪽 정사각형
    4, 5, 6, 6, 7, 4    // 아래쪽 정사각형
};
```

![](https://blog.kakaocdn.net/dna/RE8TH/btsNU50V6xL/AAAAAAAAAAAAAAAAAAAAAPjYPU4b5gmY2NEcNMbo603wYdaqjyORHLJK6C366nGH/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2B8KuP7ZN1eZM6fEXZCeGeoMxflw%3D)

프로그램을 실행하면 아래쪽 사각형이 위쪽 사각형에 덮어씌어집니다. (더 뒷 쪽에 있음에도 불구하고)

그 이유는 인덱스 배열에서 나중에 그려지는 geometry가 먼저 그려진 geometry의 fragment 값을 덮기 때문입니다.

이 문제를 해결하는 방법은 다음 두 가지가 있습니다

1. **모든 draw call을 depth(깊이) 순으로 정렬하는 방법** (Back-to-Front)
   * 주로 **투명 객체** 렌더링 시 사용 됨
2. **Depth buffer와 depth test를 사용하는 방법**
   * 일반적인 opaque(불투명) 객체 렌더링에 적합

Depth buffer는 color attachment처럼 각 픽셀에 대해 **깊이 값**을 저장하는 추가 버퍼입니다.  
Rasterizer가 fragment를 생성할 때마다 depth test가 수행되며,  
해당 fragment가 이전에 할당된 값보다 더 가까울 경우에만 픽셀이 업데이트됩니다.

테스트에 통과하면 현재 fragment의 깊이 값이 depth buffer에 기록됩니다.

이 depth 값은 **fragment shader에서 수동으로 조작**하는 것도 가능합니다.

기본적으로 GLM에서 생성하는 perspective projection matrix는 OpenGL의 깊이 범위인 -1.0 ~ 1.0을 따릅니다.  
하지만 Vulkan은 0.0 ~ 1.0 범위를 사용하므로 다음과 같이 정의를 추가해야 합니다:

```
#define GLM_FORCE_RADIANS
#define GLM_FORCE_DEPTH_ZERO_TO_ONE
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
```

### Depth image and view

Depth attachment는 color attachment처럼 **image를 기반**으로 합니다.  
하지만 color attachment와 달리, **swap chain은 depth image를 자동으로 생성해주지 않습니다.**

렌더링은 한 번에 하나의 draw 작업만 실행되므로, **depth image는 하나만 있으면 충분**합니다.  
이 depth image도 다음의 세 가지 리소스를 요구합니다:

```
VkImage depthImage;
VkDeviceMemory depthImageMemory;
VkImageView depthImageView;
```

새로운 함수 createDepthResources를 만들어 이 리소스들을 설정합니다

```
void initVulkan() {
    ...
    createCommandPool();
    createDepthResources();  //여기서 호출합니다
    createTextureImage();
    ...
}​
```

### Create Depth Image

Depth image를 생성하는 절차는 비교적 간단합니다.

* **해상도**는 color attachment와 동일합니다.( swap chain extent로 지정합니다. )
* depth attachment에 적합한 **image usage**를 설정해야 합니다.
* tiling은 **VK\_IMAGE\_TILING\_OPTIMAL**, **메모리는 device local로 지정**합니다.

Texture image와는 달리, texel에 직접 접근할 필요가 없으므로 **정확한 format이 고정되어 있을 필요는 없습니다**.  
하지만 **24비트 이상의 깊이 정밀도**를 사용하는 것이 일반적입니다. 다음의 포맷들이 자주 사용됩니다

![](https://blog.kakaocdn.net/dna/cjXCtk/btsNVt8gtZR/AAAAAAAAAAAAAAAAAAAAAK91M0D2C7ZQP1lsJiFyEK5TylO9qtgXVOHHrfPQuSZO/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=6cui4yZYrFKC92xFgOLB2r6Sws4%3D)

VK\_FORMAT\_D32\_SFLOAT는 대부분의 하드웨어에서 지원되므로 기본 선택지로 적합합니다.  
그러나 우리는 좀 더 유연한 코드를 위해 **우선순위별로 후보 format을 입력받고, 지원 여부를 확인하는** 함수를 만들겠습니다.

```
VkFormat findSupportedFormat(
    const std::vector<VkFormat>& candidates,
    VkImageTiling tiling,
    VkFormatFeatureFlags features
) {
    for (VkFormat format : candidates) {
        VkFormatProperties props;
        vkGetPhysicalDeviceFormatProperties(physicalDevice, format, &props);

        if (tiling == VK_IMAGE_TILING_LINEAR &&
            (props.linearTilingFeatures & features) == features) {
            return format;
        } else if (tiling == VK_IMAGE_TILING_OPTIMAL &&
                   (props.optimalTilingFeatures & features) == features) {
            return format;
        }
    }

    throw std::runtime_error("failed to find supported format!");
}
```

이 함수에서 vkGetPhysicalDeviceFormatProperties를 사용해 각 format의 지원 여부를 확인합니다.

* linearTilingFeatures: linear tiling일 때 지원되는 기능
* optimalTilingFeatures: optimal tiling일 때 지원되는 기능
* bufferFeatures: buffer에서 지원되는 기능 (이번에는 사용하지 않습니다)

위에서 만든 findSupportedFormat을 활용해 **depth attachment에 적합한 포맷을 선택하는 헬퍼 함수를 작성**합니다

```
VkFormat findDepthFormat() {
    return findSupportedFormat(
        {
            VK_FORMAT_D32_SFLOAT,
            VK_FORMAT_D32_SFLOAT_S8_UINT,
            VK_FORMAT_D24_UNORM_S8_UINT
        },
        VK_IMAGE_TILING_OPTIMAL,
        VK_FORMAT_FEATURE_DEPTH_STENCIL_ATTACHMENT_BIT
    );
}
```

이때 VK\_IMAGE\_USAGE\_XXX가 아니라 VK\_FORMAT\_FEATURE\_XXX 플래그를 사용해야 합니다.

선택한 depth format이 stencil component를 포함하는지 확인하는 간단한 함수도 작성합니다

stencil은 이후 챕터에서 다룰 예정입니다.

```
bool hasStencilComponent(VkFormat format) {
    return format == VK_FORMAT_D32_SFLOAT_S8_UINT ||
           format == VK_FORMAT_D24_UNORM_S8_UINT;
}
```

이제 createDepthResources 함수에서 포맷을 찾고 image를 생성합니다

```
VkFormat depthFormat = findDepthFormat();

createImage(
    swapChainExtent.width,
    swapChainExtent.height,
    depthFormat,
    VK_IMAGE_TILING_OPTIMAL,
    VK_IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT,
    VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
    depthImage,
    depthImageMemory
);

depthImageView = createImageView(depthImage, depthFormat, VK_IMAGE_ASPECT_DEPTH_BIT);
```

기존 createImageView 함수는 항상 color image로 간주하고 있었기 때문에,  
**aspectMask를 매개변수로 받을 수 있도록 수정해야 합시다.**

```
VkImageView createImageView(VkImage image, VkFormat format, VkImageAspectFlags aspectFlags) {
    ...
    viewInfo.subresourceRange.aspectMask = aspectFlags;
    ...
}
```

이후 이 함수를 사용하는 모든 위치에서 올바른 aspectMask를 전달해야 합니다:

```
swapChainImageViews[i] = createImageView(
    swapChainImages[i],
    swapChainImageFormat,
    VK_IMAGE_ASPECT_COLOR_BIT
);

depthImageView = createImageView(
    depthImage,
    depthFormat,
    VK_IMAGE_ASPECT_DEPTH_BIT
);

textureImageView = createImageView(
    textureImage,
    VK_FORMAT_R8G8B8A8_SRGB,
    VK_IMAGE_ASPECT_COLOR_BIT
);
```

이제 depth image의 생성을 완료했습니다.  
이 image는 프로그램에서 직접 접근하거나 다른 image에서 복사할 필요가 없습니다.  
렌더 패스의 시작에서 color attachment처럼 **clear** 처리만 하면 됩니다.

### 

### Explicitly transitioning the depth image

뛰어넘어도 되는 부분입니다

더보기

이 내용은 보통 **render pass에서 자동 처리되지만**, 완전성을 위해 수동 전환 방식도 설명하는 절입니다.

**render pass내부에서 자동으로 처리되기 때문에 depth image의 layout을 명시적으로 전환할 필요는 없습니다.**  
하지만 학습 목적 또는 디버깅 목적을 위해 이 과정을 이해하는 것은 유익합니다.  
(나중에 봐도 괜찮습니다)

createDepthResources 함수의 마지막에 transitionImageLayout 함수를 호출하여 layout을 전환합니다

```
transitionImageLayout(
    depthImage,
    depthFormat,
    VK_IMAGE_LAYOUT_UNDEFINED,
    VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL
);
```

더보기

### 

transitionImageLayout 함수 안에서 **subresource aspect**를 올바르게 설정해주어야 합니다:

```
if (newLayout == VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL) {
    barrier.subresourceRange.aspectMask = VK_IMAGE_ASPECT_DEPTH_BIT;

    if (hasStencilComponent(format)) {
        barrier.subresourceRange.aspectMask |= VK_IMAGE_ASPECT_STENCIL_BIT;
    }
} else {
    barrier.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
}
```

**stencil을 사용하지 않더라도**,  
stencil component가 포함된 format(D24\_UNORM\_S8\_UINT, D32\_SFLOAT\_S8\_UINT)의 경우에  
layout 전환 시 **VK\_IMAGE\_ASPECT\_STENCIL\_BIT를 포함**시켜야 합니다.

다음으로 layout 전환을 위한 **access mask**와 **pipeline stage**를 정확히 설정해야 합니다.  
아래는 전형적인 layout 전환의 세 가지 경우를 다룹니다:

```
if (oldLayout == VK_IMAGE_LAYOUT_UNDEFINED && newLayout == VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL) {
    barrier.srcAccessMask = 0;
    barrier.dstAccessMask = VK_ACCESS_TRANSFER_WRITE_BIT;

    sourceStage = VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT;
    destinationStage = VK_PIPELINE_STAGE_TRANSFER_BIT;
}
else if (oldLayout == VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL && newLayout == VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL) {
    barrier.srcAccessMask = VK_ACCESS_TRANSFER_WRITE_BIT;
    barrier.dstAccessMask = VK_ACCESS_SHADER_READ_BIT;

    sourceStage = VK_PIPELINE_STAGE_TRANSFER_BIT;
    destinationStage = VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT;
}
else if (oldLayout == VK_IMAGE_LAYOUT_UNDEFINED && newLayout == VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL) {
    barrier.srcAccessMask = 0;
    barrier.dstAccessMask = 
        VK_ACCESS_DEPTH_STENCIL_ATTACHMENT_READ_BIT |
        VK_ACCESS_DEPTH_STENCIL_ATTACHMENT_WRITE_BIT;

    sourceStage = VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT;
    destinationStage = VK_PIPELINE_STAGE_EARLY_FRAGMENT_TESTS_BIT;
}
else {
    throw std::invalid_argument("unsupported layout transition!");
}
```

### 

* srcAccessMask는 **이전 layout에서의 접근 권한**을 나타냅니다.  
  0이면 아무것도 접근하지 않았음을 의미합니다.
* dstAccessMask는 **새로운 layout에서 필요한 접근 권한**입니다.  
  예: depth attachment는 읽기/쓰기 둘 다 필요합니다.
* sourceStage는 **이전 작업이 완료된 시점**,  
  destinationStage는 **다음 작업이 시작될 시점**을 의미합니다.

Depth buffer는 fragment에 대해 **depth 테스트를 수행**하는 데 사용되며,  
이는 **VK\_PIPELINE\_STAGE\_EARLY\_FRAGMENT\_TESTS\_BIT** 단계에서 발생합니다.

* 읽기: depth test
* 쓰기: depth 값 갱신 (일부는 LATE\_FRAGMENT\_TESTS\_BIT에서 수행됨)

### Render Pass

기존 color attachment에 더해 depth 테스트를 위한 설정을 추가하는 작업입니다.

이제 createRenderPass 함수를 수정하여 **depth attachment**를 포함하도록 합니다.

1. VkAttachmentDescription에 Depth Attachment 정의

```
VkAttachmentDescription depthAttachment{};
depthAttachment.format = findDepthFormat();  // depth image와 동일한 포맷 사용
depthAttachment.samples = VK_SAMPLE_COUNT_1_BIT;
depthAttachment.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR;
depthAttachment.storeOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;
depthAttachment.stencilLoadOp = VK_ATTACHMENT_LOAD_OP_DONT_CARE;
depthAttachment.stencilStoreOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;
depthAttachment.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
depthAttachment.finalLayout = VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL;
```

* format: depth image와 **동일한 포맷**을 사용해야 합니다.
* loadOp: 렌더링 시작 시 깊이 값을 **clear** 합니다.
* storeOp: 이후 depth 값을 사용하지 않으므로 **저장하지 않음(DONT\_CARE)** 으로 설정합니다.
* initialLayout: **이전 내용 layout이 뭐였던 신경안쓰니**  UNDEFINED로 설정합니다.
* finalLayout: **depth 테스트에 사용할 수 있는 DEPTH\_STENCIL\_ATTACHMENT\_OPTIMAL**로 설정합니다.

2. Subpass 내 Depth Attachment 참조 추가

```
VkAttachmentReference depthAttachmentRef{};
depthAttachmentRef.attachment = 1; // attachments 배열의 인덱스 1
depthAttachmentRef.layout = VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL;
```

3. Subpass에 Depth Attachment 연결

```
VkSubpassDescription subpass{};
subpass.pipelineBindPoint = VK_PIPELINE_BIND_POINT_GRAPHICS;
subpass.colorAttachmentCount = 1;
subpass.pColorAttachments = &colorAttachmentRef;
subpass.pDepthStencilAttachment = &depthAttachmentRef;
```

* Subpass에서는 **하나의 depth (+ stencil) attachment만 사용**할 수 있습니다. (여러 개의 depth buffer에서 테스트하는 것은 의미가 없다. )

4. Attachment 배열에 depthAttachment 포함

```
std::array<VkAttachmentDescription, 2> attachments = {
    colorAttachment, depthAttachment
};
```

5. Render Pass 생성 구조체에 반영

```
VkRenderPassCreateInfo renderPassInfo{};
renderPassInfo.sType = VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO;
renderPassInfo.attachmentCount = static_cast<uint32_t>(attachments.size());
renderPassInfo.pAttachments = attachments.data();
renderPassInfo.subpassCount = 1;
renderPassInfo.pSubpasses = &subpass;
renderPassInfo.dependencyCount = 1;
renderPassInfo.pDependencies = &dependency;
```

6. Subpass Dependency 업데이트 (Color + Depth 대응)

```
//이전 작업이 끝나는 시점
dependency.srcStageMask =
VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT |
VK_PIPELINE_STAGE_EARLY_FRAGMENT_TESTS_BIT;

//우리가 작업을 시작할 수 있는 가장빠른 stage
dependency.dstStageMask =
VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT |
VK_PIPELINE_STAGE_EARLY_FRAGMENT_TESTS_BIT;


//접근할 리소스
dependency.dstAccessMask = VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT |
VK_ACCESS_DEPTH_STENCIL_ATTACHMENT_WRITE_BIT;
```

* 이 설정은 **depth image의 layout 전환**과 **loadOp를 통한 clear 작업**이 충돌하지 않도록 하기 위함입니다.
* Depth image는 **early fragment test 단계에서 처음 사용되며**,  
  **loadOp가 clear일 경우 해당 시점에 쓰기 접근이 발생**합니다.
* 따라서 dstAccessMask에 DEPTH\_STENCIL\_ATTACHMENT\_WRITE\_BIT를 추가해줘야 합니다.

### FrameBuffer

다음 단계는 **depth image를 framebuffer의 depth attachment로 바인딩**하는 것입니다.  
createFramebuffers 함수로 이동하여 **depth image view를 두 번째 attachment로 명시**합니다:

```
std::array<VkImageView, 2> attachments = {
    swapChainImageViews[i],  // color attachment
    depthImageView           // depth attachment
};
```

그리고 VkFramebufferCreateInfo 구조체를 다음과 같이 설정합니다

```
VkFramebufferCreateInfo framebufferInfo{};
framebufferInfo.sType = VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO;
framebufferInfo.renderPass = renderPass;
framebufferInfo.attachmentCount = static_cast<uint32_t>(attachments.size());
framebufferInfo.pAttachments = attachments.data();
framebufferInfo.width = swapChainExtent.width;
framebufferInfo.height = swapChainExtent.height;
framebufferInfo.layers = 1;
```

각 swap chain image는 별도의 **color attachment**를 가지지만, **모든 color image는 동일한 depth image를 공유**할 수 있습니다.

이는 **동시에 하나의 subpass만 실행되도록 동기화(semaphore) 되어 있기 때문**입니다.

따라서 depth image는 공유 가능하며, 여러 framebuffers에 재사용 가능합니다

**depthImageView가 먼저 생성되어야 framebuffer에 사용할 수 있으므로,**  
initVulkan() 함수에서 **createFramebuffers()를 createDepthResources() 이후에 호출**해야 합니다

```
createDepthResources();
createFramebuffers();
```

### Clear Values

depth attachment도 VK\_ATTACHMENT\_LOAD\_OP\_CLEAR를 사용하므로,  
이제는 **color + depth용 clear 값을 모두 명시**해야 합니다.

recordCommandBuffer 함수에서 VkClearValue 배열을 설정합니다:

```
std::array<VkClearValue, 2> clearValues{};
clearValues[0].color = {{0.0f, 0.0f, 0.0f, 1.0f}};  // color clear
clearValues[1].depthStencil = {1.0f, 0};            // depth clear
```

Vulkan에서 depth 값의 범위는 **0.0 (near) ~ 1.0 (far)** 입니다.

초기 상태에서는 모든 픽셀이 **가장 먼 거리(1.0f)** 로 초기화되어야, 이후에 가까운 depth의 fragment가 통과할 수 있습니다.

렌더 패스에 clear 값을 적용하려면 다음을 설정합니다

```
renderPassInfo.clearValueCount = static_cast<uint32_t>(clearValues.size());
renderPassInfo.pClearValues = clearValues.data();
```

clearValues의 순서는 attachment 순서와 반드시 일치해야 합니다.

## Depth  and Stencil State

depth attachment는 이제 framebuffer에 포함되었지만,  
**depth test를 사용하려면 graphics pipeline에도 활성화**해줘야 합니다.

```
VkPipelineDepthStencilStateCreateInfo depthStencil{};
depthStencil.sType = VK_STRUCTURE_TYPE_PIPELINE_DEPTH_STENCIL_STATE_CREATE_INFO;
depthStencil.depthTestEnable = VK_TRUE;
depthStencil.depthWriteEnable = VK_TRUE;
depthStencil.depthCompareOp = VK_COMPARE_OP_LESS;
```

Depth Bound Test는 사용하지 않음

```
depthStencil.depthBoundsTestEnable = VK_FALSE;
depthStencil.minDepthBounds = 0.0f;
depthStencil.maxDepthBounds = 1.0f;
```

depth bound test는 **depth 값이 지정된 범위 안에 들어올 때만 유효**한 fragment로 간주합니다.

Stencil Test도 사용하지 않음

```
depthStencil.stencilTestEnable = VK_FALSE;
depthStencil.front = {};
depthStencil.back = {};
```

만약 stencil test를 사용하려면 **depth format에 stencil component가 포함되어야 합니다**  
(예: VK\_FORMAT\_D24\_UNORM\_S8\_UINT)

작성한 depthStencil 구조체를 pipeline에 등록합니다: 

```
pipelineInfo.pDepthStencilState = &depthStencil;​
```

depth/stencil attachment가 render pass에 있다면, 해당 pipeline state도 반드시 설정해야 합니다.

## 결과

![](https://blog.kakaocdn.net/dna/b0aaFO/btsNV473Pkl/AAAAAAAAAAAAAAAAAAAAAJtHmBe9mPW7Fd9kxNJaA6pwmQOIP5xgxPKJlbdyJ-Eh/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ewIFrLHq%2BVXMm2Ru%2FirGHDPoc18%3D)

진짜 마지막 부분입니다..하하

### Handling Window Resize

창 크기가 변경되면 color attachment의 해상도뿐 아니라 **depth buffer의 해상도도 함께 변경**되어야 합니다.

recreateSwapChain() 함수에 **depth resource 재생성 코드**를 추가해야 합니다

```
void recreateSwapChain() {
    int width = 0, height = 0;
    while (width == 0 || height == 0) {
        glfwGetFramebufferSize(window, &width, &height);
        glfwWaitEvents();  // 창이 최소화되었을 경우 대기
    }

    vkDeviceWaitIdle(device);  // GPU 작업이 모두 끝날 때까지 대기

    cleanupSwapChain();        // 이전 리소스 정리

    createSwapChain();         // swap chain 재생성
    createImageViews();        // image view 재생성
    createDepthResources();    // depth image/view 다시 생성
    createFramebuffers();      // framebuffer 다시 생성
}
```

depth image 관련 리소스는 기존 swap chain 리소스들과 함께 해제해야 합니다

```
void cleanupSwapChain() {
    vkDestroyImageView(device, depthImageView, nullptr);
    vkDestroyImage(device, depthImage, nullptr);
    vkFreeMemory(device, depthImageMemory, nullptr);

    ...
}
```

 

드디어 3D geometry를 올바르게 렌더링할 수 있게 되었습니다!! 하하하...!  
다음 장에서는 모델을 불러봐봅시다~