---
title: "[Vulkan] Mipmap"
date: 2025-05-16
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

이제 우리의 프로그램은 3D 모델을 불러오고 렌더링할 수 있습니다. 이번 장에서는 **mipmap** 기능을 추가해보겠습니다.

Mipmap은 미리 계산된, 축소된 버전의 이미지입니다. 각 mip 이미지의 너비와 높이는 이전 이미지의 절반이며, Level of Detail(LOD)의 일종으로 사용됩니다.

카메라에서 멀리 떨어진 객체는 더 작은 mip 이미지에서 텍스처를 샘플링합니다. 작은 이미지를 사용하면 렌더링 속도가 빨라지고 아티팩트를 방지할 수 있습니다.

![](https://blog.kakaocdn.net/dna/QGGup/btsNVgO3MDv/AAAAAAAAAAAAAAAAAAAAANpGtZ3qBvJJjW-S-z4lxCs5vSzgelypN1tvej6e7R9O/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=na22KF46UXPVj2FLTuG4C44AYQY%3D)

### Image Creation

Vulkan에서는 각 mip 이미지를 VkImage의 서로 다른 **mip level**에 저장합니다. mip level 0은 원본 이미지이며, 이후 레벨들은 보통 **mip chain**이라 불립니다.

mip level의 개수는 VkImage를 생성할 때 지정합니다. 지금까지는 항상 이 값을 1로 설정했습니다. 이제는 이미지의 크기에서 mip level의 수를 계산해야 합니다.

먼저 이 값을 저장할 class 멤버를 추가합니다.

```
...
uint32_t mipLevels;
VkImage textureImage;
...
```

mipLevels의 값은 createTextureImage 함수에서 텍스처를 불러온 후 계산할 수 있습니다.

```
int texWidth, texHeight, texChannels;
stbi_uc* pixels = stbi_load(TEXTURE_PATH.c_str(), &texWidth, &texHeight, &texChannels, STBI_rgb_alpha);
...
mipLevels = static_cast<uint32_t>(std::floor(std::log2(std::max(texWidth, texHeight)))) + 1;
```

이 수식은 mip chain의 레벨 개수를 계산합니다. max 함수는 더 큰 차원을 선택하고, log2는 해당 차원을 몇 번 2로 나눌 수 있는지를 계산합니다.

이 값을 사용하려면 createImage, createImageView, transitionImageLayout 함수에서 mip level 수를 전달할 수 있도록 변경해야 합니다. 각 함수에 mipLevels 매개변수를 추가합니다:

```
void createImage(uint32_t width, uint32_t height, uint32_t mipLevels, VkFormat format, VkImageTiling tiling, VkImageUsageFlags usage, VkMemoryPropertyFlags properties, VkImage& image, VkDeviceMemory& imageMemory) {
    //...
    imageInfo.mipLevels = mipLevels;
    //...
}

//...

VkImageView createImageView(VkImage image, VkFormat format, VkImageAspectFlags aspectFlags, uint32_t mipLevels) {
    //...
    viewInfo.subresourceRange.levelCount = mipLevels;
    //...
}

//...

void transitionImageLayout(VkImage image, VkFormat format, VkImageLayout oldLayout, VkImageLayout newLayout, uint32_t mipLevels) {
    //...
    barrier.subresourceRange.levelCount = mipLevels;
    //...
}
```

이제 이러한 함수들을 호출하는 부분에서도 적절한 mipLevels 값을 전달해야 합니다.

(depth, swapchain 부분은 1로, mipmap사용하길 원하는 textureimage부분은 mipLevels로 인자를 넘기면 될 것 같습니다.)

```
createImage(swapChainExtent.width, swapChainExtent.height, 1, depthFormat, VK_IMAGE_TILING_OPTIMAL, VK_IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT, VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT, depthImage, depthImageMemory);

createImage(texWidth, texHeight, mipLevels, VK_FORMAT_R8G8B8A8_SRGB, VK_IMAGE_TILING_OPTIMAL, VK_IMAGE_USAGE_TRANSFER_DST_BIT | VK_IMAGE_USAGE_SAMPLED_BIT, VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT, textureImage, textureImageMemory);

//...

swapChainImageViews[i] = createImageView(swapChainImages[i], swapChainImageFormat, VK_IMAGE_ASPECT_COLOR_BIT, 1);

depthImageView = createImageView(depthImage, depthFormat, VK_IMAGE_ASPECT_DEPTH_BIT, 1);

textureImageView = createImageView(textureImage, VK_FORMAT_R8G8B8A8_SRGB, VK_IMAGE_ASPECT_COLOR_BIT, mipLevels);

//...

transitionImageLayout(depthImage, depthFormat, VK_IMAGE_LAYOUT_UNDEFINED, VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL, 1);

transitionImageLayout(textureImage, VK_FORMAT_R8G8B8A8_SRGB, VK_IMAGE_LAYOUT_UNDEFINED, VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL, mipLevels);
```

### Generating Mipmaps

우리의 texture image는 이제 여러 개의 mip level을 가지고 있지만, **staging buffer는 오직 mip level 0만 채울 수 있습니다.**

나머지 mip level들은 아직 정의되지 않았으며, 이 레벨들은 우리가 가진 단 하나의 level에서부터 데이터를 생성해야 합니다.

이를 위해 vkCmdBlitImage 명령을 사용합니다. 이 명령은 이미지 복사, 크기 조정, 필터링 작업을 수행하며, 우리는 이를 여러 번 호출하여 texture image의 각 level에 데이터를 blit하게 됩니다.

vkCmdBlitImage는 **전송(transfer)** 작업으로 간주되기 때문에, texture image가 전송의 **source**이자 **destination**으로 사용될 것임을 Vulkan에 알려야 합니다. 이를 위해 createTextureImage에서 texture image의 usage flag에 VK\_IMAGE\_USAGE\_TRANSFER\_SRC\_BIT를 추가합니다:

```
createImage(texWidth, texHeight, mipLevels, VK_FORMAT_R8G8B8A8_SRGB,
    VK_IMAGE_TILING_OPTIMAL,
    VK_IMAGE_USAGE_TRANSFER_SRC_BIT |
    VK_IMAGE_USAGE_TRANSFER_DST_BIT |
    VK_IMAGE_USAGE_SAMPLED_BIT,
    VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
    textureImage, textureImageMemory);
```

다른 이미지 작업들과 마찬가지로, **vkCmdBlitImage도 이미지의 layout에 의존합니다.** 전체 이미지를 VK\_IMAGE\_LAYOUT\_GENERAL로 전환할 수도 있지만, 이는 성능 저하를 유발할 수 있습니다. 최적의 성능을 위해서는:

* 소스 이미지는 VK\_IMAGE\_LAYOUT\_TRANSFER\_SRC\_OPTIMAL
* 대상 이미지는 VK\_IMAGE\_LAYOUT\_TRANSFER\_DST\_OPTIMAL

로 설정하는 것이 좋습니다. Vulkan은 각 mip level을 독립적으로 전환할 수 있기 때문에, 각 blit 작업 사이에 해당 level만 전환하면 됩니다.

기존의 transitionImageLayout 함수는 전체 image의 layout을 전환하므로, 각 level별로 pipeline barrier를 별도로 작성해야 합니다. 따라서, createTextureImage에서 다음 코드 라인을 제거합니다.

```
// transitionImageLayout to SHADER_READ_ONLY_OPTIMAL 삭제
```

그 대신 mipmap을 생성하는 동안 각 level을 개별적으로 전환합니다. 그럼 mipmap 생성 함수 generateMipmaps를 작성해보겠습니다

```
void generateMipmaps(VkImage image, VkFormat imageFormat,
	int32_t texWidth, int32_t texHeight, uint32_t mipLevels)
{


VkCommandBuffer commandBuffer = beginSingleTimeCommands();

VkImageMemoryBarrier barrier{};
barrier.sType = VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER;
barrier.image = image;
barrier.srcQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
barrier.dstQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
barrier.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
barrier.subresourceRange.baseArrayLayer = 0;
barrier.subresourceRange.layerCount = 1;
barrier.subresourceRange.levelCount = 1;
```

이 VkImageMemoryBarrier 객체는 여러 transition에서 재사용됩니다. 변경되는 부분은 baseMipLevel, oldLayout, newLayout, srcAccessMask, dstAccessMask입니다.

```
int32_t mipWidth = texWidth;
int32_t mipHeight = texHeight;

for (uint32_t i = 1; i < mipLevels; i++) {
barrier.subresourceRange.baseMipLevel = i - 1;
barrier.oldLayout = VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL;
barrier.newLayout = VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL;
barrier.srcAccessMask = VK_ACCESS_TRANSFER_WRITE_BIT;	// 지금까지 권한 (dst였으니, write)
barrier.dstAccessMask = VK_ACCESS_TRANSFER_READ_BIT;	// 앞으로 권한 (src로 사용할 것이니, read)

vkCmdPipelineBarrier(commandBuffer,
    VK_PIPELINE_STAGE_TRANSFER_BIT, VK_PIPELINE_STAGE_TRANSFER_BIT, 0,
    0, nullptr, 0, nullptr, 1, &barrier);
```

```
VkImageBlit blit{};
blit.srcOffsets[0] = { 0, 0, 0 };
blit.srcOffsets[1] = { mipWidth, mipHeight, 1 };
blit.srcSubresource.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
blit.srcSubresource.mipLevel = i - 1;
blit.srcSubresource.baseArrayLayer = 0;
blit.srcSubresource.layerCount = 1;

blit.dstOffsets[0] = { 0, 0, 0 };
blit.dstOffsets[1] = {
	mipWidth > 1 ? mipWidth / 2 : 1,
	mipHeight > 1 ? mipHeight / 2 : 1,
	1
};
blit.dstSubresource.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
blit.dstSubresource.mipLevel = i;
blit.dstSubresource.baseArrayLayer = 0;
blit.dstSubresource.layerCount = 1;
```

소스 mip 레벨은 i - 1, 대상 mip 레벨은 i입니다.

srcOffsets 배열은 데이터를 **어디서 복사해올지**를 결정하는 3D 영역을 지정하고,  
dstOffsets 배열은 데이터를 **어디로 복사할지**를 지정합니다.

( [0,width),[0,height) 느낌)

dstOffsets[1]의 X, Y 크기는 이전 레벨의 절반이므로 **2로 나눈 값**을 사용합니다.  
그리고 2D 이미지의 경우 깊이(Depth)가 1이기 때문에,

srcOffsets[1]과 dstOffsets[1]의 Z 값은 **반드시 1이어야 합니다**.

```
vkCmdBlitImage(commandBuffer,
    image, VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,
    image, VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
    1, &blit,
    VK_FILTER_LINEAR);
```

여기서 textureImage가 srcImage와 dstImage 모두에 사용됩니다.

소스 mip 레벨은 바로 전에 VK\_IMAGE\_LAYOUT\_TRANSFER\_SRC\_OPTIMAL로 전환되었고,  
대상 mip 레벨은 createTextureImage 함수에서  
이미 VK\_IMAGE\_LAYOUT\_TRANSFER\_DST\_OPTIMAL로 설정되어 있습니다.

만약 **전용 transfer 큐**(Vertex Buffer 섹션에서 제안된 것처럼)를 사용 중이라면 주의해야 합니다.

vkCmdBlitImage는 반드시 **graphics 기능을 가진 큐에서 실행**되어야 합니다.

```
        barrier.oldLayout = VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL;
        barrier.newLayout = VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL;
        barrier.srcAccessMask = VK_ACCESS_TRANSFER_READ_BIT;
        barrier.dstAccessMask = VK_ACCESS_SHADER_READ_BIT;

        vkCmdPipelineBarrier(commandBuffer,
            VK_PIPELINE_STAGE_TRANSFER_BIT, VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT, 0,
            0, nullptr, 0, nullptr, 1, &barrier);

        if (mipWidth > 1) mipWidth /= 2;
        if (mipHeight > 1) mipHeight /= 2;
    }
	// 마지막 mip level은 blit 대상이 되지 않으므로 layout 전환만 따로 처리
	barrier.subresourceRange.baseMipLevel = mipLevels - 1;
	barrier.oldLayout = VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL;
	barrier.newLayout = VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL;
	barrier.srcAccessMask = VK_ACCESS_TRANSFER_WRITE_BIT;
	barrier.dstAccessMask = VK_ACCESS_SHADER_READ_BIT;

	vkCmdPipelineBarrier(commandBuffer,
		VK_PIPELINE_STAGE_TRANSFER_BIT, VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT, 0,
		0, nullptr, 0, nullptr, 1, &barrier);

	endSingleTimeCommands(commandBuffer);
}
```

지금까지 mipmap을 만들고 mipmap level에 따라 layout을 따로 따로 변경해주고 있었는데,

마지막 mip level은 blit 대상이 되지 않으므로 layout 전환만 따로 처리해줍시다.

마지막으로 mipmap 생성을 위한 함수를 texture image 초기화 코드에 삽입합니다:

```
transitionImageLayout(textureImage, VK_FORMAT_R8G8B8A8_SRGB,
    VK_IMAGE_LAYOUT_UNDEFINED, VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL, mipLevels);

copyBufferToImage(stagingBuffer, textureImage,
    static_cast<uint32_t>(texWidth), static_cast<uint32_t>(texHeight));

// mipmap을 생성하면서 SHADER_READ_ONLY_OPTIMAL로 전환됨
generateMipmaps(textureImage, texWidth, texHeight, mipLevels);
```

이제 texture image의 모든 mip level이 정상적으로 채워졌습니다.

### Linear filtering support

vkCmdBlitImage 같은 내장 함수를 사용해서 mipmap 레벨들을 자동으로 생성하는 것은 매우 편리하지만,  
**모든 플랫폼에서 이를 지원하는 것은 아닙니다.**

이 기능은 사용하는 텍스처 이미지 포맷이 **linear filtering을 지원해야** 합니다.  
이 지원 여부는 vkGetPhysicalDeviceFormatProperties 함수를 사용해서 확인할 수 있습니다.

우리는 generateMipmaps 함수 안에 이 확인 코드를 추가합시다.

```
void createTextureImage() {
    ...
    generateMipmaps(textureImage, VK_FORMAT_R8G8B8A8_SRGB, texWidth, texHeight, mipLevels);
}


void generateMipmaps(VkImage image, VkFormat imageFormat, int32_t texWidth, int32_t texHeight, uint32_t mipLevels) {
    ...
}
```

vkGetPhysicalDeviceFormatProperties로 지원 여부 확인

```
VkFormatProperties formatProperties;
vkGetPhysicalDeviceFormatProperties(physicalDevice, imageFormat, &formatProperties);
```

VkFormatProperties 구조체는 세 가지 필드를 가집니다:

* linear Tiling Features
* optimal Tiling Features
* buffer Features

우리는 이미지를 **optimal tiling**으로 생성했기 때문에,  
optimal Tiling Features 안에서 해당 포맷이 linear filtering을 지원하는지 확인해야 합니다.

```
if (!(formatProperties.optimalTilingFeatures & VK_FORMAT_FEATURE_SAMPLED_IMAGE_FILTER_LINEAR_BIT)) {
    throw std::runtime_error("texture image format does not support linear blitting!");
}
```

### 

만약 지원하지 않을 경우에는 두 가지 대안이 있습니다:

1. **지원되는 포맷을 찾는 함수**를 구현해서, linear filtering을 지원하는 포맷을 자동 탐색하거나
2. **stb\_image\_resize 같은 라이브러리를 사용해서 소프트웨어로 mipmap 생성**  
   이 경우 각 mip 레벨 이미지를 직접 계산해서 vkCmdCopyBufferToImage 같은 방식으로 업로드하면 됨

대부분의 경우 mipmap은 **런타임에 생성하지 않고**, 미리 생성된 상태로 텍스처 파일에 함께 저장됩니다.  
이렇게 하면 로딩 속도도 빠르고 호환성도 확보할 수 있습니다.

### 

### Sampler

VkImage는 mipmap 데이터를 담고 있고 VkSampler는 그 데이터를 **어떻게 읽을지**를 제어합니다.

**LOD(Level of Detail)** 관련 주요 설정입니다.

* minLod, maxLod: 사용할 mip 레벨의 범위
* mipLodBias: 선택된 LOD에 보정값 추가
* mipmapMode: LOD를 정수로 사용할지, 두 레벨을 보간할지 결정

```
lod = getLodLevelFromScreenSize();           // 객체가 가까울수록 lod는 작음
lod = clamp(lod + mipLodBias, minLod, maxLod);
level = clamp(floor(lod), 0, mipLevels - 1);  // 샘플링할 mip 레벨 결정
```

마무리 설정 예시입니다.

```
samplerInfo.mipmapMode = VK_SAMPLER_MIPMAP_MODE_LINEAR;
samplerInfo.minLod = 0.0f;                             // 사용할 최소 LOD
samplerInfo.maxLod = static_cast<float>(mipLevels);   // 사용할 최대 LOD
samplerInfo.mipLodBias = 0.0f;                         // LOD 오프셋 없음
```

전체 mip 레벨을 사용할 수 있도록 설정했으며, LOD 보정은 적용하지 않음.

이제 프로그램을 실행하면 mipmap이 적용된 텍스처가 화면에 보이게 될 것입니다.

![](https://blog.kakaocdn.net/dna/b3doZW/btsNWfIZ8GO/AAAAAAAAAAAAAAAAAAAAAEXUf74vPuKGcezPtJI_1C1RMg89RyChgNINFbYgJMIX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=s%2FQ5gApwwbM56dF1690MufdJzeo%3D)