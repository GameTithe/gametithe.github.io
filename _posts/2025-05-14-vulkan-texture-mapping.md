---
title: "[Vulkan] Texture Mapping"
date: 2025-05-14
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

{% raw %}

우리가 texture mapping을 하기 위해서 아래와 같은 작업을 수행해야됩니다.

1. **device 메모리를 기반으로 한 image 객체를 생성**한다.
2. **image 파일에서 픽셀 데이터를 읽어와 image에 채운다.**
3. **image sampler를 생성**한다.
4. **shader에서 texture의 색을 샘플링할 수 있도록, combined image sampler descriptor를 추가**한다.

image를 만들고 데이터를 채우는 흐름은 **vertex buffer 생성과 매우 유사합니다.**

먼저 **staging resource**를 만들어 픽셀 데이터를 채운 뒤, 이를 **최종 image 객체로 복사합니다.**

특별히 **staging image**를 만드는 것도 가능하지만,

Vulkan에서는 **VkBuffer에서 VkImage 복사**도 지원하며, **일부 하드웨어에서는 이 방식이 더 빠릅니다.**

우리는 먼저 **buffer를 생성하여 픽셀 값을 채운 후**, 해당 데이터를 최종 rendering에 사용할 image로 복사하겠습니다.

이미지의 layout도 종류가 많기 때문에 상황에 맞게 잘 사용해야됩니다.

|  |  |
| --- | --- |
| VK\_IMAGE\_LAYOUT\_PRESENT\_SRC\_KHR | 화면에 표시할 때 최적 |
| VK\_IMAGE\_LAYOUT\_COLOR\_ATTACHMENT\_OPTIMAL | fragment shader에서 color attachment로 사용할 때 최적 |
| VK\_IMAGE\_LAYOUT\_TRANSFER\_SRC\_OPTIMAL | image를 복사할 때 (source) |
| VK\_IMAGE\_LAYOUT\_TRANSFER\_DST\_OPTIMAL | image를 복사할 때 (destination) |
| VK\_IMAGE\_LAYOUT\_SHADER\_READ\_ONLY\_OPTIMAL | shader에서 texture를 읽을 때 최적 |

layout 전환을 할 때 가장 일반적인 방식은 **pipeline barrier를 사용하는 것입니다.**

**shader 또는 copy 연산 전에 적절한 layout으로 변환**하는 데 필수적입니다.

(barrier는 VK\_SHARING\_MODE\_EXCLUSIVE 모드에서 queue family ownership 전환에도 사용됩니다.)

Image 로드를 위해서 stb\_image.h를 사용하겠습니다.

stb\_image.h가 들어 있는 디렉토리를 Additional Include Directories에 추가하면됩니다.

![](https://blog.kakaocdn.net/dna/bbtMDM/btsNKfozfAw/AAAAAAAAAAAAAAAAAAAAAMelxdUTJ6SbTHEoy8WCAtKgD4YUS2FtBejx1AG6iU2M/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=zV4I3HozPjv8w9dsgj%2BeA2J13sA%3D)

(저는 vcpkg로 설치해서 사용했습니다.)

### Loading an Image

stb\_image 라이브러리를 다음과 같이 include합시다.

```
#define STB_IMAGE_IMPLEMENTATION
#include <stb_image.h>
```

기본적으로 stb\_image.h는 함수의 선언부(prototype)만 정의되어 있습니다.

실제 함수의 정의(body)를 포함하려면 STB\_IMAGE\_IMPLEMENTATION을 define한 후 include 해야됩니다.

```
void initVulkan() {
    ...
    createCommandPool();      // 커맨드 풀 생성 이후에
    createTextureImage();     // 텍스처 이미지를 생성
    createVertexBuffer();     // 이후 버텍스 버퍼 생성
    ...
}
```

image를 load하고, vulkan imagme object에 업로드 할 때

command buffer를 사용할 예정이므로, 반드시 **createCommandPool 호출 이후에 실행되어야 합니다.**

shaders 디렉토리 옆에 textures라는 새로운 디렉토리를 만들어, 여기에 텍스처 이미지를 저장합시다.

textures/texture.jpg로 저장하고 불러와봅시다.

```
void createTextureImage() {
    int texWidth, texHeight, texChannels;

    stbi_uc* pixels = stbi_load("textures/texture.jpg", &texWidth, &texHeight, &texChannels, STBI_rgb_alpha);
    VkDeviceSize imageSize = texWidth * texHeight * 4;

    if (!pixels) {
        throw std::runtime_error("failed to load texture image!");
    }
 
}
```

### Staging Buffer

이제 우리는 vkMapMemory를 이용해 픽셀 데이터를 복사할 수 있도록 **host-visible 메모리에 staging buffer**를 만들 것입니다.

createTextureImage 함수 안에 이 임시 버퍼용 변수를 추가합시다.

```
VkBuffer stagingBuffer;
VkDeviceMemory stagingBufferMemory;
```

이 버퍼는

**host-visible 메모리**에 존재하고 ( vkMapMemory로 접근 가능하기 위해서)

**transfer source**로 사용될 수 있수 있어야합니다. (image로 복사하기 위해서)

```
createBuffer(
    imageSize,
    VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
    VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
    stagingBuffer,
    stagingBufferMemory
);​
```

그다음 image에서 가져온 픽셀 값을 버퍼에 복사합니다.

```
void* data;
vkMapMemory(device, stagingBufferMemory, 0, imageSize, 0, &data);
memcpy(data, pixels, static_cast<size_t>(imageSize));
vkUnmapMemory(device, stagingBufferMemory);
```

마지막으로, 원래의 pixels 배열을 해제합니다.

```
stbi_image_free(pixels);
```

### Texture Image

픽셀 값을 직접 shader에서 접근하도록 버퍼를 구성할 수도 있지만, **Vulkan에서는 image object를 사용하는 것이 더 낫습니다.**

image object를 사용하면 **2D 좌표 기반으로 색을 불러올 수 있고, 속도와 사용성 면에서도 훨씬 유리**합니다.  
**image 내부의 픽셀은** **texel( texture pixel이라는 의미)**이라고 불리며, 이제부터는 이 용어를 사용하겠습니다.

멤버 변수를 추가합시다.

```
VkImage textureImage;
VkDeviceMemory textureImageMemory;
```

image를 만들기 위해 VkImageCreateInfo 구조체를 설정합시다

```
VkImageCreateInfo imageInfo{};
imageInfo.sType = VK_STRUCTURE_TYPE_IMAGE_CREATE_INFO;
imageInfo.imageType = VK_IMAGE_TYPE_2D;
imageInfo.extent.width = static_cast<uint32_t>(texWidth);
imageInfo.extent.height = static_cast<uint32_t>(texHeight);
imageInfo.extent.depth = 1;
imageInfo.mipLevels = 1;
imageInfo.arrayLayers = 1;
```

Vulkan에게 **image의 좌표계 종류**를 알려줘야합니다.

VK\_IMAGE\_TYPE\_1D: 데이터 배열, gradient

VK\_IMAGE\_TYPE\_2D: 일반적인 텍스처 (**우리가 사용하는 것**)

VK\_IMAGE\_TYPE\_3D: voxel( volume  pixel ,  3D 텍스처)

depth는 **항상 1 이상**이어야 하며, 0은 허용되지 않습니다.

mipmap을 사용하지 않고, texture array도 사용하지 않으므로 각각 1로 설정했습니다.

```
imageInfo.format = VK_FORMAT_R8G8B8A8_SRGB;
```

Vulkan은 다양한 image format을 지원하지만, 복사 대상인 buffer와 **같은 포맷**이어야 합니다.

```
imageInfo.tiling = VK_IMAGE_TILING_OPTIMAL;
```

VK\_IMAGE\_TILING\_LINEAR: texel이 row-major 형식으로 나열됨 (버퍼처럼 접근 가능)

VK\_IMAGE\_TILING\_OPTIMAL: 하드웨어에 맞춰 최적화된 레이아웃으로 정렬됨 (**shader 샘플링 시 권장**)

**(image의 **layout과는 달리**, tiling은 생성 후 바꿀 수 없습니다.)**

```
imageInfo.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
```

초기 layout 값으로 가능한 2개

VK\_IMAGE\_LAYOUT\_UNDEFINED: GPU에서 사용 불가능, **첫 layout 전환 시 texel이 삭제됨**VK\_IMAGE\_LAYOUT\_PREINITIALIZED: GPU에서 사용 불가능, **첫** **layout** **전환 시 texel 유지됨**

우리는 **이미지를 shader로 복사해서 샘플링**해서 사용할 예정이니, texel을 유지할 필요가 없습니다.

그러니 UNDEFINED 사용하겠습니다.

```
imageInfo.usage = VK_IMAGE_USAGE_TRANSFER_DST_BIT | VK_IMAGE_USAGE_SAMPLED_BIT;
```

이 image는 staging buffer로부터 복사받는 **destination**이므로 TRANSFER\_DST\_BIT를 포함시키고

이후 shader에서 샘플링해야 하므로 SAMPLED\_BIT도 포함시키겠습니다.

```
imageInfo.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
imageInfo.samples = VK_SAMPLE_COUNT_1_BIT;
imageInfo.flags = 0; // Optional
```

VK\_SHARING\_MODE\_EXCLUSIVE: 하나의 queue family에서만 사용하겠습니다.

samples = 1: multisampling 안함

```
if (vkCreateImage(device, &imageInfo, nullptr, &textureImage) != VK_SUCCESS) {
    throw std::runtime_error("failed to create image!");
}
```

항상 하던대로 vkCreateImage를 사용해서 이미지를 생성해줍니다.

```
VkMemoryRequirements memRequirements;
vkGetImageMemoryRequirements(device, textureImage, &memRequirements);
```

이미지의 메모리를 할당하는 방식은 버퍼와 동일합니다.

```
VkMemoryAllocateInfo allocInfo{};
allocInfo.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;
allocInfo.allocationSize = memRequirements.size;
allocInfo.memoryTypeIndex = findMemoryType(memRequirements.memoryTypeBits, VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT);

if (vkAllocateMemory(device, &allocInfo, nullptr, &textureImageMemory) != VK_SUCCESS) {
    throw std::runtime_error("이미지 메모리 할당에 실패했습니다!");
}

vkBindImageMemory(device, textureImage, textureImageMemory, 0);
```

이렇게 이미지를 생성하고 메모리를 할당하면 되는데, 볼륨이 너무 커졌으니

createImage라는 함수로 따로 뺍시다.

```
void createImage(uint32_t width, uint32_t height, VkFormat format,
VkImageTiling tiling, VkImageUsageFlags usage,
VkMemoryPropertyFlags properties, VkImage& image,
VkDeviceMemory& imageMemory) {

	VkImageCreateInfo imageInfo{};
	imageInfo.sType = VK_STRUCTURE_TYPE_IMAGE_CREATE_INFO;
	imageInfo.imageType = VK_IMAGE_TYPE_2D;
	imageInfo.extent.width = width;
	imageInfo.extent.height = height;
	imageInfo.extent.depth = 1;
	imageInfo.mipLevels = 1;
	imageInfo.arrayLayers = 1;

	imageInfo.format = VK_FORMAT_R8G8B8A8_SRGB;
	imageInfo.tiling = VK_IMAGE_TILING_OPTIMAL;
	imageInfo.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
	imageInfo.usage = VK_IMAGE_USAGE_TRANSFER_DST_BIT |
		VK_IMAGE_USAGE_SAMPLED_BIT;
	imageInfo.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
	imageInfo.samples = VK_SAMPLE_COUNT_1_BIT;
	imageInfo.flags = 0;

	if (vkCreateImage(device, &imageInfo, nullptr, &textureImage) != VK_SUCCESS)
	{
		throw std::runtime_error("failed to create image");
	}

	VkMemoryRequirements memRequirements;
	vkGetImageMemoryRequirements(device, textureImage, &memRequirements);

	VkMemoryAllocateInfo allocInfo{};
	allocInfo.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;
	allocInfo.allocationSize = memRequirements.size;
	allocInfo.memoryTypeIndex =
		findMemoryType(memRequirements.memoryTypeBits,
			VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT);

	if (vkAllocateMemory(device, &allocInfo, nullptr, &textureImageMemory) != VK_SUCCESS)
	{
		throw std::runtime_error("failed to allocate Image Memory");
	}

	vkBindImageMemory(device, textureImage, textureImageMemory, 0);

}
```

width, height, format, tiling mode, usage, memory property 등은 이미지마다 달라질 수 있으므로 함수 파라미터로 만듭시다.

이제 createTextureImage 함수는 다음과 같이 간단하게 작성할 수 있습니다.

```
void createTextureImage()
{
	int texWidth, texHeight, texChannels;

	stbi_uc* pixels = stbi_load("textures/texture.jpg", &texWidth, &texHeight, &texChannels, STBI_rgb_alpha);

	VkDeviceSize imageSize = texWidth * texHeight & 4;

	if (!pixels)
	{
		throw std::runtime_error("failed to load texture image!");

	}

	VkBuffer stagingBuffer;
	VkDeviceMemory stagingBufferMemory;

	createBuffer(imageSize, VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
		VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT |
		VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
		stagingBuffer,
		stagingBufferMemory);

	void* data;
	vkMapMemory(device, stagingBufferMemory, 0, imageSize, 0, &data);
	memcpy(data, pixels, static_cast<size_t>(imageSize));
	vkUnmapMemory(device, stagingBufferMemory);

	stbi_image_free(pixels);

	createImage(texWidth, texHeight,
		VK_FORMAT_R8G8B8_SRGB,
		VK_IMAGE_TILING_OPTIMAL,
		VK_IMAGE_USAGE_TRANSFER_DST_BIT | VK_IMAGE_USAGE_SAMPLED_BIT,
		VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
		textureImage, textureImageMemory);

	transitionImageLayout(textureImage, VK_FORMAT_R8G8B8A8_SRGB,
		VK_IMAGE_LAYOUT_UNDEFINED, VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL);
	
	copyBufferToImage(stagingBuffer, textureImage, static_cast<uint32_t>(texWidth), static_cast<uint32_t>(texHeight));

	// for shader 
	transitionImageLayout(textureImage, VK_FORMAT_R8G8B8A8_SRGB,
		VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
		VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL);
}
```

layer transition에 대해서 정리하면, 처음 초기에는 유효한 데이터가 없기 때문에 VK\_IMAGE\_LAYOUT\_UNDEFINED로 초기화를 하고,

Staging buffer에서 데이터를 가져오기 위해서 복사를 위한 layer:VK\_IMAGE\_LAYOUT\_TRANSFER\_DST\_OPTIMAL로 변경 했다가,

shader가 사용하기 위한 layer: VK\_IMAGE\_LAYOUT\_SHADER\_READ\_ONLY\_OPTIMAL로 변경하는 흐름입니다.

### Layout Transitions

이제 command buffer에 다시 record하고 실행하는 작업을 해야 됩니다.

해당 로직을 **helper 함수로 분리해봅시다.**

```
VkCommandBuffer beginSingleTimeCommands() {
    VkCommandBufferAllocateInfo allocInfo{};
    allocInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;
    allocInfo.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
    allocInfo.commandPool = commandPool;
    allocInfo.commandBufferCount = 1;

    VkCommandBuffer commandBuffer;
    vkAllocateCommandBuffers(device, &allocInfo, &commandBuffer);

    VkCommandBufferBeginInfo beginInfo{};
    beginInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
    beginInfo.flags = VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT;

    vkBeginCommandBuffer(commandBuffer, &beginInfo);
    return commandBuffer;
}
```

**일회성 command buffer**를 생성하고 record하는 역할을 합니다.

VK\_COMMAND\_BUFFER\_USAGE\_ONE\_TIME\_SUBMIT\_BIT는 이 command buffer가 단 한 번만 제출될 것이라는 의미입니다.

```
void endSingleTimeCommands(VkCommandBuffer commandBuffer) {
    vkEndCommandBuffer(commandBuffer);

    VkSubmitInfo submitInfo{};
    submitInfo.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO;
    submitInfo.commandBufferCount = 1;
    submitInfo.pCommandBuffers = &commandBuffer;

    vkQueueSubmit(graphicsQueue, 1, &submitInfo, VK_NULL_HANDLE);
    vkQueueWaitIdle(graphicsQueue);

    vkFreeCommandBuffers(device, commandPool, 1, &commandBuffer);
}
```

이 함수는 **command buffer를 종료**하고, **graphic queue에 제출**한 뒤 **queue가 작업을 마칠 때까지 기다립니다**.

마지막에는 사용한 **command buffer를** **command pool로 반환합니다.**

위 helper 함수들을 활용하면 copyBuffer는 다음처럼 간단해집니다.

```
void copyBuffer(VkBuffer srcBuffer, VkBuffer dstBuffer, VkDeviceSize size) {
    VkCommandBuffer commandBuffer = beginSingleTimeCommands();

    VkBufferCopy copyRegion{};
    copyRegion.size = size;
    vkCmdCopyBuffer(commandBuffer, srcBuffer, dstBuffer, 1, &copyRegion);

    endSingleTimeCommands(commandBuffer);
}
```

vkCmdCopyBufferToImage 명령을 사용하려면 image가 적절한 layout 상태여야 하므로, **layout 전환을 처리하는 함수**를 만들어야 합니다.

```
void transitionImageLayout(VkImage image, VkFormat format,
                           VkImageLayout oldLayout, VkImageLayout newLayout) {
    VkCommandBuffer commandBuffer = beginSingleTimeCommands();

    // TODO: barrier 설정 필요

    endSingleTimeCommands(commandBuffer);
}
```

## 

layout 전환을 수행할 때는 일반적으로 VkImageMemoryBarrier를 사용합니다.

이 구조체는 리소스 접근을 **synchronization**하고, **image layout을 전환**하거나 **queue family 소유권을 이전**하는 데도 쓰입니다.

```
VkImageMemoryBarrier barrier{};
barrier.sType = VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER;
barrier.oldLayout = oldLayout;
barrier.newLayout = newLayout;
```

oldLayout을 VK\_IMAGE\_LAYOUT\_UNDEFINED로 설정하면 기존 내용은 무시되며, 초기화 용도로 적합합니다.

```
barrier.srcQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
barrier.dstQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
```

queue family를 변경 하지 않을 경우 반드시 VK\_QUEUE\_FAMILY\_IGNORED로 명시해야 합니다.

```
barrier.image = image;
barrier.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
barrier.subresourceRange.baseMipLevel = 0;
barrier.subresourceRange.levelCount = 1;
barrier.subresourceRange.baseArrayLayer = 0;
barrier.subresourceRange.layerCount = 1;
```

어떤 image의 어떤 부분이 영향을 받을지를 지정합니다.  
여기선 일반적인 2D image로, mipmap이나 array layer가 없기 때문에 각각 1개만 설하겠습니다.

```
barrier.srcAccessMask = 0; // TODO
barrier.dstAccessMask = 0; // TODO
```

이 barrier를 통해 어떤 연산이 먼저 완료되어야 하고, 어떤 연산이 이 barrier 이후에 시작되어야 하는지를 정의합니다.  
layout 전환 종류에 따라 적절한 mask를 설정해야 합니다.

```
vkCmdPipelineBarrier(
    commandBuffer,
    /* srcStageMask */ 0,         // TODO
    /* dstStageMask */ 0,         // TODO
    0,                            // 보통 0 또는 VK_DEPENDENCY_BY_REGION_BIT
    0, nullptr,                   // memory barrier 없음
    0, nullptr,                   // buffer memory barrier 없음
    1, &barrier                   // image memory barrier 1개
);
```

srcStageMask: **barrier 이전에** 끝나야 할 pipeline stage

dstStageMask: **barrier 이후에** 실행될 pipeline stage

VK\_DEPENDENCY\_BY\_REGION\_BIT: region 단위로 barrier를 제한할 수 있는 옵션

(어떤 pipeline stage를 선택할 수 있는지는 image가 사용되는 방식에 따라 달라지며, validation layer는 잘못된 stage를 지정하면 경고를 출력해줍니다.)

( shader에서 읽는 용도라면 VK\_ACCESS\_SHADER\_READ\_BIT,  
해당 stage는 VK\_PIPELINE\_STAGE\_FRAGMENT\_SHADER\_BIT로 지정해야됩니다.)

### Copying buffer to image

createTextureImage로 다시 돌아가기 전에, 먼저 하나의 헬퍼 함수를 더 작성하겠습니다.

```
void copyBufferToImage(VkBuffer buffer, VkImage image, uint32_t width, uint32_t height) {
    VkCommandBuffer commandBuffer = beginSingleTimeCommands();

    // TODo

    endSingleTimeCommands(commandBuffer);
}
```

buffer에서 image로 데이터를 복사할 때도 마찬가지로, **buffer의 어느 부분이 image의 어느 부분으로 복사되는지** 명시해야 합니다.

```
VkBufferImageCopy region{};
region.bufferOffset = 0;
region.bufferRowLength = 0;
region.bufferImageHeight = 0;

region.imageSubresource.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
region.imageSubresource.mipLevel = 0;
region.imageSubresource.baseArrayLayer = 0;
region.imageSubresource.layerCount = 1;

region.imageOffset = {0, 0, 0};
region.imageExtent = {
    width,
    height,
    1
};
```

**bufferOffset**: buffer 내에서 pixel 값이 시작되는 byte 오프셋

**bufferRowLength, bufferImageHeight:** 메모리에서 픽셀들이 어떻게 배치되어 있는지를 정의함

여기선 둘 다 0으로 설정되어 있고, 이는 **픽셀이 메모리에서 간격 없이 꽉 차게(tightly packed)** 배치되어 있다는 의미다.

**imageSubresource:** image의 어느 서브 리소스를 복사 대상으로 할지 지정함

색상 채널만 복사하기 때문에 VK\_IMAGE\_ASPECT\_COLOR\_BIT 사용

**imageOffset, imageExtent:** image의 어느 위치로 얼마만큼의 데이터를 복사할지 정의

실제 복사 작업은 vkCmdCopyBufferToImage로 큐에 등록됩니다.

```
vkCmdCopyBufferToImage(
    commandBuffer,
    buffer,
    image,
    VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
    1,
    &region
);
```

**buffer:** 원본 buffer

**image:** 대상 image

**VK\_IMAGE\_LAYOUT\_TRANSFER\_DST\_OPTIMAL:** 현재 image가 복사 작업에 적합한 layout으로 설정

(복사 전에 layout 전환을 완료해둔 상태여야 함)

**1:** 복사 영역 개수 (여기선 한 번만 복사)

**&region**: 복사할 상세 영역 정보

### Preparing the texture image

이제 texture image를 완전히 준비하기 위한 모든 도구를 갖췄으니, 다시 createTextureImage 함수로 돌아가봅시다.

다음 단계는 **staging buffer의 데이터를 texture image로 복사하는 것입니다.**

이를 위해 다음 두 단계가 필요합니다.

1. texture image의 layout을 VK\_IMAGE\_LAYOUT\_TRANSFER\_DST\_OPTIMAL로 전환
2. buffer => image 복사 명령 실행

방금 전에 만든 함수들 덕분에 이 작업은 간단히 처리할 수 있습니다.

layout 설정하고, staging Buffer 데이터를 textureImage로 복사하는 작업입니다.

```
transitionImageLayout(textureImage, VK_FORMAT_R8G8B8A8_SRGB,
                      VK_IMAGE_LAYOUT_UNDEFINED, VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL);

copyBufferToImage(stagingBuffer, textureImage,
                  static_cast<uint32_t>(texWidth),
                  static_cast<uint32_t>(texHeight));
```

### 

이제 **shader에서 texture image를 샘플링**할 수 있도록 하려면, 마지막으로 **shader 접근이 가능한 layout**으로 한 번 더 전환해야합니다..!

```
transitionImageLayout(textureImage, VK_FORMAT_R8G8B8A8_SRGB,
                      VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
                      VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL);
```

이 layout은 shader가 read-only로 접근할 수 있도록 설정해주며,  
실제 rendering 파이프라인에서 **fragment shader 등에서 texture를 사용할 수 있게 만드는 마무리 단계입니다.**

### Transition Barrier Masks

Vulkan에서 이미지를 사용할 때는 **그 이미지가 어떤 layout에 있는지가 매우 중요**합니다.

예를 들어, 이미지가 처음 생성되었을 때는 VK\_IMAGE\_LAYOUT\_UNDEFINED 상태일 수 있지만, 이후에 shader에서 사용하곻 싶다면 layout을 VK\_IMAGE\_LAYOUT\_SHADER\_READ\_ONLY\_OPTIMAL로 변경해야합니다.

하지만 단순히 **layout만 바꾸는 것으로 끝나는 것이 아니라, GPU 내부에서 그 transition이 언제 일어나야 하는지, 그리고 어떤 access mask가 필요한지를 명확하게 지정**해야합니다.

이러한 설정이 잘못되면 validation layer에서 경고 메시지를 띄우고, 프로그램이 올바르게 작동하지 않을 수 있습니다.

이번에 처리해야될 transition은 두 가지가 있습니다.

1. VK\_IMAGE\_LAYOUT\_UNDEFINED => VK\_IMAGE\_LAYOUT\_TRANSFER\_DST\_OPTIMAL

이 transition은 이미지가 생성된 직후, 즉 아직 어떤 데이터도 쓰이지 않은 상태에서 시작됩니다. (undifined 상태)

이 경우에는 기다릴 작업이 아무것도 없기 때문에, **transfer write** **작업을 바로 진행해도 괜찮습니다.**

2. VK\_IMAGE\_LAYOUT\_TRANSFER\_DST\_OPTIMAL => VK\_IMAGE\_LAYOUT\_SHADER\_READ\_ONLY\_OPTIMAL

이 transition은 이미지를 shader에서 사용할 준비를 하는 과정입니다.

**shader read 작업이 반드시 transfer write 작업이 모두 완료된 이후**에 수행되어야 합니다.

특히 **fragment shader에서 읽기 작업이 발생하므로, 해당 pipeline stage에 맞추어 설정해 주셔야 합니다.**

(fragment에서 texture를 sampling해서 사용하니까)

아래는 두 가지 transition 상황에 맞춘 access mask와 pipeline stage 설정 예시입니다:

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
```

그리고 이 설정을 실제 command buffer에 적용할 때는 다음과 같은 방식으로 pipeline barrier를 기록하시면 됩니다:

```
vkCmdPipelineBarrier(
    commandBuffer,
    sourceStage, destinationStage,
    0,
    0, nullptr,
    0, nullptr,
    1, &barrier
);
```

### 

VK\_PIPELINE\_STAGE\_TRANSFER\_BIT는 일반적인 graphics pipeline 단계가 아니라, transfer 작업만을 위한 **가상의 pseudo-stage**입니다.

첫 번째 transition에서는 아무것도 기다릴 필요가 없기 때문에 VK\_PIPELINE\_STAGE\_TOP\_OF\_PIPE\_BIT에서 시작해도 괜찮습니다.

두 번째 transition에서는 반드시 transfer 작업이 끝난 후에 shader가 image를 읽도록 VK\_ACCESS\_SHADER\_READ\_BIT(shader에서 접근 권한을 얻길 원한다)와 VK\_PIPELINE\_STAGE\_FRAGMENT\_SHADER\_BIT(fragments stage 전까지) 를 사용해야 합니다.

command buffer를 제출하면, VK\_ACCESS\_HOST\_WRITE\_BIT에 대한 **암시적 동기화**가 자동으로 적용됩니다.  
즉, srcAccessMask를 0으로 설정해도 특정 조건에서는 문제가 되지 않을 수 있습니다.  
하지만 OpenGL처럼 내부적으로 숨겨진 동작에 의존하는 것보다는, **명시적으로 필요한 권한과 시점을 지정하시는 것이 더 안전한 방법**입니다.

특별한 경우에는 모든 작업에 사용할 수 있는 VK\_IMAGE\_LAYOUT\_GENERAL layout을 사용할 수 있습니다.  
하지만 이 layout은 성능 최적화가 되어 있지 않아서 일반적인 경우에는 사용을 권장하지 않습니다.  
(이미지가 input과 output으로 동시에 사용되거나, preinitialized layout 이후에 다시 접근해야 할 경우 등에서 사용됩니다.)

현재까지 사용하신 helper 함수들은 각 명령을 기록하고, 실행이 끝날 때까지 GPU queue를 기다리는 방식으로 구성되어 있습니다.  
하지만 실전에서는 여러 transition과 copy 작업을 **하나의 command buffer에 기록한 후**, 이를 **비동기적으로 실행**하는 것이 성능상 훨씬 유리합니다.

예를 들어 createTextureImage() 함수 안의 transition과 copy 작업을 한데 모아 setupCommandBuffer에 기록하시고,  
필요 시 flushSetupCommands로 실행하면 됩니다.

### Cleanup

마지막으로 transition이 끝난 후에는 staging buffer와 관련 메모리를 다음과 같이 정리해주시면 됩니다.

```
transitionImageLayout(textureImage, VK_FORMAT_R8G8B8A8_SRGB,
    VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
    VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL);

vkDestroyBuffer(device, stagingBuffer, nullptr);
vkFreeMemory(device, stagingBufferMemory, nullptr);
```

그리고 프로그램이 종료될 때 texture image를 해제합시다.

```
void cleanup() {
    cleanupSwapChain();

    vkDestroyImage(device, textureImage, nullptr);
    vkFreeMemory(device, textureImageMemory, nullptr);
}
```

### Image view and Sampler

**그래픽 파이프라인에 Texture를 샘플링하기 위해서 필요한 두 가지 리소스**를 생성합니다.

1. swapchain 이미지 작업에서 이미 본 적 있는 image view이고,
2. shader가 이미지로부터 texel(텍스처 픽셀)을 읽을 때 사용되 sampler입니다.

### Texture ImageView 만들기

우리는 swapchain 이미지나 framebuffer를 사용할 때, 이미지를 직접 사용하는 것이 아니라 **image view를 통해 접근했습니다.**  
texture image 역시 동일하게, 사용할 수 있도록 하려면 **image view를 따로 생성**해야 합니다.

먼저 텍스처 이미지를 위한 VkImageView 멤버를 클래스에 추가해줍니다

```
VkImageView textureImageView;
```

초기화 루틴에서 다음 순서로 호출되도록 합니다:

```
void initVulkan() {
    ...
    createTextureImage();
    createTextureImageView(); // 여기에 추가
    createVertexBuffer();
    ...
}
```

### 

이 함수의 코드는 이전에 작성했던 createImageViews 함수에서 대부분 재활용할 수 있습니다.  
차이점은 **이미지와 포맷만 다르다**는 것입니다.

```
void createTextureImageView() {
    VkImageViewCreateIn viewInfo{};
    viewInfo.sType = VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO;
    viewInfo.image = textureImage;
    viewInfo.viewType = VK_IMAGE_VIEW_TYPE_2D;
    viewInfo.format = VK_FORMAT_R8G8B8A8_SRGB;
    viewInfo.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
    viewInfo.subresourceRange.baseMipLevel = 0;
    viewInfo.subresourceRange.levelCount = 1;
    viewInfo.subresourceRange.baseArrayLayer = 0;
    viewInfo.subresourceRange.layerCount = 1;

    // viewInfo.components 초기화 안해도 괜찮, swizzle 가능이 기본 

    if (vkCreateImageView(device, &viewInfo, nullptr, &textureImageView) != VK_SUCCESS) {
        throw std::runtime_error("failed to create texture image view!");
    }
}
```

createImageView()라는 공통 함수를 만들어 두면 여러 곳에서 재사용할 수 있습니다:

```
VkImageView createImageView(VkImage image, VkFormat format) {
    VkImageViewCreateInfo viewInfo{};
    viewInfo.sType = VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO;
    viewInfo.image = image;
    viewInfo.viewType = VK_IMAGE_VIEW_TYPE_2D;
    viewInfo.format = format;
    viewInfo.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
    viewInfo.subresourceRange.baseMipLevel = 0;
    viewInfo.subresourceRange.levelCount = 1;
    viewInfo.subresourceRange.baseArrayLayer = 0;
    viewInfo.subresourceRange.layerCount = 1;

    VkImageView imageView;
    if (vkCreateImageView(device, &viewInfo, nullptr, &imageView) != VK_SUCCESS) {
        throw std::runtime_error("failed to create texture image view!");
    }

    return imageView;
}
```

이제 createTextureImageView() 함수는 아주 간단하게 줄일 수 있습니다.

```
void createTextureImageView() {
    textureImageView = createImageView(textureImage, VK_FORMAT_R8G8B8A8_SRGB);
}
```

마찬가지로, swapchain 이미지들을 위한 createImageViews()도 다음처럼 단순화할 수 있습니다.

```
void createImageViews() {
    swapChainImageViews.resize(swapChainImages.size());

    for (uint32_t i = 0; i < swapChaiImages.size(); i++) {
        swapChainImageViews[i] = createImageView(swapChainImages[i], swapChainImageFormat);
    }
}
```

프로그램이 종료될 때, **image view를 image보다** **먼저 destroy** 해야 합니다.  
cleanup() 함수 안에 다음 코드를 추가하세요

```
void cleanup() {
    cleanupSwapChain();

    vkDestroyImageView(device, textureImageView, nullptr);
    vkDestroyImage(device, textureImage, nullptr);
    vkFreeMemory(device, textureImageMemory, nullptr);
    ...
}
```

이제 이미지에 대한 view가 생성되었습니다. 이제 sampler를 만들어봅시다. 

## Sampler

shader가 이미지를 읽는 방식은 두 가지가 있습니다

* texel을 **직접 읽는 방법** (많이 안씀)
* **sampler를 통해 읽는 방법** (텍스처로 사용할 때 일반적입니다)

**Sampler는 단순히 texel 값을 가져오는 것이 아니라, 필터링과 변환을** **적용하여 최종 색상을 계산해주는 역할을 합니다.**  
oversampling 또는 undersampling 문제가 발생했을 때, sampler는 이를 자동으로 보정해줄 수 있습니다.

![](https://blog.kakaocdn.net/dna/buOQ4Y/btsNNeP07cY/AAAAAAAAAAAAAAAAAAAAABfzhWpe3JU6t_zjlZ22PHQmeTanStUl_CxGpe_Qnggl/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=XyJhQ9CKq8PKAi1PZSQMtJMuTRE%3D)

**oversampling:** texel 수 < fragment 수 인 경우이다. 단순히 가장 가까운 texel을 가져오면 다음과 같은 **거친 결과**가 나타납니다.

하지만 주변 4개의 texel을 선형 보간(linear interpolation)하여 가져오면 훨씬 **부드러운 결과**를 얻을 수 있습니다. sampler는 이러한 **필터링을 자동으로 수행**해줍니다. (왼쪽은 Minecraft 스타일, 오른쪽은 일반적인 그래픽 스타일)

![](https://blog.kakaocdn.net/dna/bD6vik/btsNK1x1fiE/AAAAAAAAAAAAAAAAAAAAAHutut3cw9Bj9KeQsIdqoVa8D5I0y2T7BYdibpos7_bt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9R8s%2F7jiguWL9DBkCVDvJc4QLrE%3D)

**undersampling:**  texel 수 > fragment 수 인 경우이다.  특히 체크무늬 같은 **고주파 텍스처**를 비스듬히 보면 흐릿하게 보이거나 왜곡됩니다.  
이때는 **anisotropic filtering**이 필요하며, sampler를 통해 자동으로 적용할 수 있습니다.

 **Addressing Mode:** 텍스처 좌표가 이미지 범위를 벗어났을 때 처리하는 방법들  

![](https://blog.kakaocdn.net/dna/cX1w5v/btsNNg1pOqZ/AAAAAAAAAAAAAAAAAAAAAJQ-uVdkbyHFYASULAw-BnI7yzE109UmwYf7ksV_uhkg/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=2%2B%2BxRDp1yQXT0%2Bq1mYE4X3DBc7E%3D)

* VK\_SAMPLER\_ADDRESS\_MODE\_REPEAT: 이미지 경계를 넘어가면 텍스처를 반복시킵니다 (타일링 효과).
* VK\_SAMPLER\_ADDRESS\_MODE\_MIRRORED\_REPEAT: 반복하면서 반전된 좌표로 텍스처를 뒤집습니다.
* VK\_SAMPLER\_ADDRESS\_MODE\_CLAMP\_TO\_EDGE: 경계를 벗어나면 가장자리 색상을 계속 사용합니다.
* VK\_SAMPLER\_ADDRESS\_MODE\_CLAMP\_TO\_BORDER: 경계를 벗어나면 지정된 고정 색상으로 채웁니다.

```
void initVulkan()
{
    createTextureImage();
    createTextureImageView();
    createSampler();
}
void createTextureSampler() {
    VkSamplerCreateInfo samplerInfo{};
    samplerInfo.sType = VK_STRUCTURE_TYPE_SAMPLER_CREATE_INFO;

    // 보간 필터 (선형 보간 사용)
    samplerInfo.magFilter = VK_FILTER_LINEAR;
    samplerInfo.minFilter = VK_FILTER_LINEAR;

    // address mode (U, V, W는 텍스처 좌표축 명칭입니다)
    samplerInfo.addressModeU = VK_SAMPLER_ADDRESS_MODE_REPEAT;
    samplerInfo.addressModeV = VK_SAMPLER_ADDRESS_MODE_REPEAT;
    samplerInfo.addressModeW = VK_SAMPLER_ADDRESS_MODE_REPEAT;

    // Anisotropic filtering 사용 설정
    samplerInfo.anisotropyEnable = VK_TRUE;

    // physical device 에서 지원하는 최대 Anisotropy 값 조회
    VkPhysicalDeviceProperties properties{};
    vkGetPhysicalDeviceProperties(physicalDevice, &properties);
    samplerInfo.maxAnisotropy = properties.limits.maxSamplerAnisotropy;

    // 이미지 범위 밖에서 샘플링할 때 사용할 색상
    samplerInfo.borderColor = VK_BORDER_COLOR_INT_OPAQUE_BLACK;

    // 정규화된 텍스처 좌표 사용 ([0,width), [0, height): TRUE // [0, 1): False)
    samplerInfo.unnormalizedCoordinates = VK_FALSE;

    // Shadow map에 사용하는 depth 비교 기능은 사용 안 함
    samplerInfo.compareEnable = VK_FALSE;
    samplerInfo.compareOp = VK_COMPARE_OP_ALWAYS;

    // Mipmapping 관련 설정 (지금은 사용 안 함)
    samplerInfo.mipmapMode = VK_SAMPLER_MIPMAP_MODE_LINEAR;
    samplerInfo.mipLodBias = 0.0f;
    samplerInfo.minLod = 0.0f;
    samplerInfo.maxLod = 0.0f;

    // sampler 생성
    if (vkCreateSampler(device, &samplerInfo, nullptr, &textureSampler) != VK_SUCCESS) {
        throw std::runtime_error("failed to create texture sampler!");
    }
}
```

## 

anisotropy의 count는 성능과 quality 간 trade off관계이다. 일단은 max를 채워서 사용합시다.

**중요한 점은, sampler 객체는 VkImage를 직접 참조하지 않는다는 것입니다.**  
sampler는 **샘플링 방식을 정의하는 독립 객체**이며, 1D, 2D, 3D 어떤 이미지든 사용 가능합니다.

이는 OpenGL 등의 구형 API에서 텍스처 이미지와 필터 설정이 결합된 방식과는 다릅니다.

(openGL은 texture param으로 filter를 설정했었다.)

### Cleanup

이미지에 대해서 더 이상 접근하지 않을 때 Sampler를 파괴해주면 된다.

```
void cleanup() {
    cleanupSwapChain();

    vkDestroySampler(device, textureSampler, nullptr);
    vkDestroyImageView(device, textureImageView, nullptr);
    vkDestroyImage(device, textureImage, nullptr);
    vkFreeMemory(device, textureImageMemory, nullptr);
    ...
}
```

이상태로 실행을 시키면 validation layer에서 경고를 줄 수 있다.

anisotropic filtering은 device의 선택적 옵션 기능이기 때문이다. 알맞는 device를 찾아서 사용하자

```
bool isDeviceSuitable(VkPhysicalDevice device)
{
    // ... 

    VkPhysicalDeviceFeatures supportedFeatures;
    vkGetPhysicalDeviceFeatures(device, &supportedFeatures);

    return indices.isComplete() && extensionSupported
        && swapChainAdequate && supportedFeatures.samplerAnisotropy;
}
```

지원안하는 하드웨어는 아래처럼 그냥 끄면 됩니다.

```
samplerInfo.anisotropyEnable = VK_FALSE;
samplerInfo.maxAnisotropy = 1;
```

### 

### Combined Image Sampler

이전에 uniform buffer를 다루며 **descriptor**의 개념을 처음 배웠습니다.  
이번에는 **새로운 타입의 descriptor: combined image sampler**에 대해 배워봅시다.

이 descriptor는 **shader에서 image 리소스를 sampler 객체를 통해 접근할 수 있게 해주는 구조**입니다.  
우리가 지난 챕터에서 만든 VkSampler 객체와 연결하여 사용됩니다.

## Update the descriptors

combined image sampler를 사용하기 위해 다음 세 가지를 수정해야 합니다.

1. **Descriptor Layout**
2. **Descriptor Pool**
3. **Descriptor Set**

그리고 마지막으로, **Vertex 구조체에 texture coordinate를 추가하고**, **Fragment Shader에서 이를 통해 텍스처 색상을 샘플링**하게 됩니다.

createDescriptorSetLayout() 함수에서 다음과 같이 VkDescriptorSetLayoutBinding을 하나 더 추가합니다.

```
VkDescriptorSetLayoutBinding samplerLayoutBinding{};
samplerLayoutBinding.binding = 1;
samplerLayoutBinding.descriptorCount = 1;
samplerLayoutBinding.descriptorType = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
samplerLayoutBinding.pImmutableSamplers = nullptr;
samplerLayoutBinding.stageFlags = VK_SHADER_STAGE_FRAGMENT_BIT;
```

binding = 1: 기존 uniform buffer가 0번 binding이었다면, sampler는 1번에 위치시킵니다.

stageFlags: sampler는 **fragment shader에서만 사용되므로** FRAGMENT\_BIT로 지정합니다.

uboLayoutBinding과 함께 배열로 묶어 layout을 생성합니다:

```
std::array<VkDescriptorSetLayoutBinding, 2> bindings = {
    uboLayoutBinding,
    samplerLayoutBinding
};
```

createDescriptorPool() 함수에서 pool이 combined image sampler를 위한 공간을 가지도록 수정해야 합니다.

```
std::array<VkDescriptorPoolSize, 2> poolSizes{};
poolSizes[0].type = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
poolSizes[0].descriptorCount = static_cast<uint32_t>(MAX_FRAMES_IN_FLIGHT);
poolSizes[1].type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
poolSizes[1].descriptorCount = static_cast<uint32_t>(MAX_FRAMES_IN_FLIGHT);

VkDescriptorPoolCreateInfo poolInfo{};
poolInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO;
poolInfo.poolSizeCount = static_cast<uint32_t>(poolSizes.size());
poolInfo.pPoolSizes = poolSizes.data();
poolInfo.maxSets = static_cast<uint32_t>(MAX_FRAMES_IN_FLIGHT);

if (vkCreateDescriptorPool(device, &poolInfo, nullptr, &descriptorPool) != VK_SUCCESS) {
	throw std::runtime_error("failed to create descriptor pool!");
}
```

Descriptor pool이 충분히 크지 않으면, Vulkan 1.1 이후에는 vkAllocateDescriptorSets()에서 VK\_ERROR\_POOL\_OUT\_OF\_MEMORY가 발생할 수 있습니다.

( GPU 드라이버가 자동으로 이 문제를 해결할 수도 있지만, **기기마다 결과가 달라질 수 있으므로** 명시적으로 descriptor 개수를 충분히 할당하는 것이 **안전하고 권장되는 방법**입니다.)

=> 이 문제는 validation layer가 잡아주지 않기 때문에 Best Practice Validation을 활성화하지 않았다면 디버깅이 어려울 수 있습니다.

createDescriptorSets() 함수에서 image 리소스도 바인딩되도록 추가합니다:

```
for (size_t i = 0; i < MAX_FRAMES_IN_FLIGHT; i++) {
    VkDescriptorBufferInfo bufferInfo{};
    bufferInfo.buffer = uniformBuffers[i];
    bufferInfo.offset = 0;
    bufferInfo.range = sizeof(UniformBufferObject);

    VkDescriptorImageInfo imageInfo{};
    imageInfo.imageLayout = VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL;
    imageInfo.imageView = textureImageView;
    imageInfo.sampler = textureSampler;

    std::array<VkWriteDescriptorSet, 2> descriptorWrites{};

    // UBO
    descriptorWrites[0].sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
    descriptorWrites[0].dstSet = descriptorSets[i];
    descriptorWrites[0].dstBinding = 0;
    descriptorWrites[0].dstArrayElement = 0;
    descriptorWrites[0].descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
    descriptorWrites[0].descriptorCount = 1;
    descriptorWrites[0].pBufferInfo = &bufferInfo;

    // Combined Image Sampler
    descriptorWrites[1].sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
    descriptorWrites[1].dstSet = descriptorSets[i];
    descriptorWrites[1].dstBinding = 1;
    descriptorWrites[1].dstArrayElement = 0;
    descriptorWrites[1].descriptorType = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
    descriptorWrites[1].descriptorCount = 1;
    descriptorWrites[1].pImageInfo = &imageInfo;

    vkUpdateDescriptorSets(
        device,
        static_cast<uint32_t>(descriptorWrites.size()),
        descriptorWrites.data(),
        0,
        nullptr
    );
}
```

여기서 VkDescriptorImageInfo는 sampler와 image view, 그리고 layout 정보를 동시에 담습니다.  
이는 uniform buffer에서 VkDescriptorBufferInfo를 사용했던 방식과 매우 유사합니다

textureImageView => 어떤 이미지인가?

textureSampler => 어떻게 샘플링할 것인가?

이 둘을 합쳐서 shader에서 사용 가능한 형태로 descriptor에 등록한 것입니다

### Texture Coordinate

texture를 맵핑하기 위해서는 텍스처에서의 좌표가 필요합니다.

이 좌표들이 실제 object( geometry)에 어떻게 텍스쳐가 맵핑될 지 정해줍니다.

```
struct Vertex {
    glm::vec2 pos;         // 위치 좌표
    glm::vec3 color;       // 색상
    glm::vec2 texCoord;    // 텍스처 좌표

    static VkVertexInputBindingDescription getBindingDescription() {
        VkVertexInputBindingDescription bindingDescription{};
        bindingDescription.binding = 0;
        bindingDescription.stride = sizeof(Vertex);
        bindingDescription.inputRate = VK_VERTEX_INPUT_RATE_VERTEX;

        return bindingDescription;
    }

    static std::array<VkVertexInputAttributeDescription, 3> getAttributeDescriptions() {
        std::array<VkVertexInputAttributeDescription, 3> attributeDescriptions{};

        attributeDescriptions[0].binding = 0;
        attributeDescriptions[0].location = 0;
        attributeDescriptions[0].format = VK_FORMAT_R32G32_SFLOAT;
        attributeDescriptions[0].offset = offsetof(Vertex, pos);

        attributeDescriptions[1].binding = 0;
        attributeDescriptions[1].location = 1;
        attributeDescriptions[1].format = VK_FORMAT_R32G32B32_SFLOAT;
        attributeDescriptions[1].offset = offsetof(Vertex, color);

        attributeDescriptions[2].binding = 0;
        attributeDescriptions[2].location = 2;
        attributeDescriptions[2].format = VK_FORMAT_R32G32_SFLOAT;
        attributeDescriptions[2].offset = offsetof(Vertex, texCoord);

        return attributeDescriptions;
    }
};
```

```
const std::vector<Vertex> vertices = {
    {{-0.5f, -0.5f}, {1.0f, 0.0f, 0.0f}, {1.0f, 0.0f}},  // 왼쪽 아래
    {{ 0.5f, -0.5f}, {0.0f, 1.0f, 0.0f}, {0.0f, 0.0f}},  // 오른쪽 아래
    {{ 0.5f,  0.5f}, {0.0f, 0.0f, 1.0f}, {0.0f, 1.0f}},  // 오른쪽 위
    {{-0.5f,  0.5f}, {1.0f, 1.0f, 1.0f}, {1.0f, 1.0f}}   // 왼쪽 위
};
```

이 튜토리얼에서는 정사각형의 각 면을 채우기 위해 (0, 0)에서 (1, 1)까지의 텍스처 좌표를 사용할 것입니다.  
이 좌표계에서 (0, 0)은 텍스처의 **왼쪽 위**, (1, 1)은 **오른쪽 아래**를 나타냅니다.

( 좌표를 0보다 작게 또는 1보다 크게 설정하면 위에서 배운 Addressing Mode가 동작되는 것을 확인할 수 있습니다. )

### Shader

마지막 단계는 shader를 수정하여 텍스처에서 색상을 샘플링하도록 만드는 것입니다.  
**우선, vertex shader 에서 텍스처 좌표를 fragment shader로 전달하도록 수정해야 합니다.**

```
layout(location = 0) in vec2 inPosition;
layout(location = 1) in vec3 inColor;
layout(location = 2) in vec2 inTexCoord;

layout(location = 0) out vec3 fragColor;
layout(location = 1) out vec2 fragTexCoord;

void main() {
    gl_Position = ubo.proj * ubo.view * ubo.model * vec4(inPosition, 0.0, 1.0);
    fragColor = inColor;
    fragTexCoord = inTexCoord;
}
```

fragTexCoord는 fragColor와 마찬가지로 **정사각형의 표면 전체에서 Raterizer의해 보간(interpolation)** 됩니다.

=> 우리가 4개의 좌표를 주고도 texture가 잘 입혀지는 이유입니다.

```
#version 450

layout(location = 0) in vec3 fragColor;
layout(location = 1) in vec2 fragTexCoord;

layout(location = 0) out vec4 outColor;

void main() {
    outColor = vec4(fragTexCoord, 0.0, 1.0);
}
```

위 셰이더를 실행하면 텍스처 좌표가 색상으로 표현된 정사각형을 보게 될 것입니다.

**셰이더를 수정한 후에는 반드시 다시 컴파일해야 합니다!**

GLSL에서 **텍스처를 샘플링**하기 위해선, sampler2D로 정의된 **sampler uniform**을 사용해야 합니다

```
layout(binding = 1) uniform sampler2D texSampler;
```

(1D나 3D 텍스처의 경우에는 sampler1D, sampler3D 등을 사용합니다.)

바인딩 번호(binding = 1)는 Vulkan의 디스크립터 설정과 일치해야 합니다.

```
void main() {
    outColor = texture(texSampler, fragTexCoord);
}
```

texture 함수는 내장 함수로, **sampler와 텍스처 좌표를 인자로 받아** 필터링 및 좌표 변환 등을 자동으로 처리해줍니다.

이제 프로그램을 실행하면, 정사각형에 **텍스처가 표시되는 것을 확인할 수 있습니다.**

![](https://blog.kakaocdn.net/dna/mB1Uw/btsNU4UcRQx/AAAAAAAAAAAAAAAAAAAAAK8zQ47YcoJ6DB5knJd7omLd7fQiWcEITI9JMS-22nFJ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ymPwfHCKN52sae04K6z2tORnoAo%3D)

텍스처 좌표를 1.0보다 큰 값으로 확장하면, 어드레싱 모드(addressing mode)의 작동 방식도 확인할 수 있습니다.  
예를 들어 다음과 같은 셰이더 코드는

```
void main() {
    outColor = texture(texSampler, fragTexCoord * 2.0);
}
```

텍스처 좌표를 **2배로 확장**하여, Vulkan의 VK\_SAMPLER\_ADDRESS\_MODE\_REPEAT 설정이 적용된 경우 텍스처가 반복되어 나타나는 것을 볼 수 있습니다.

![](https://blog.kakaocdn.net/dna/Q9hrH/btsNVb0c6p7/AAAAAAAAAAAAAAAAAAAAAEDpqSGkVxc72S9SkpPIsvvnxWV-ll8hIhzW5GhjOdWZ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2F%2FW36yrzmagkWjcn2z%2FZWGQU5Ig%3D)

텍스처 색상과 정점 색상을 **곱해서 결합**하는 방법도 있습니다

```
void main() {
    outColor = vec4(fragColor * texture(texSampler, fragTexCoord).rgb, 1.0);
}
```

여기서는 RGB 값만 곱하고, 알파(alpha)는 1.0으로 고정했습니다.

![](https://blog.kakaocdn.net/dna/bnH5Be/btsNVCppYQa/AAAAAAAAAAAAAAAAAAAAAPPxylFQpuDgowFlNnIqIZ1k14WuHqwVD1rEsbyAycNa/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=eb5sijPecH3Z%2B7Mzd0PPV6MIN3w%3D)

이제 셰이더에서 이미지를 **텍스처로 접근하고 샘플링하는 방법**을 배웠습니다!!!

**이후에 프레임버퍼에 쓰인 이미지**를 다시 읽어서 사용하면:

* **후처리(Post-processing)**,
* **3D 월드 내의 카메라 디스플레이**

등과 같은 **다양한 효과**를 구현할 수 있습니다.
{% endraw %}
