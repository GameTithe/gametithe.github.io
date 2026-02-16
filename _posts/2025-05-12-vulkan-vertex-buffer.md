---
title: "[Vulkan] Vertex Buffer"
date: 2025-05-12
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

Vertex Buffer ~ find memory type 날라감

버퍼까지는 잘 만들었지만, 아직 메모리는 할당되지 않았습니다.

vkGetBufferMemoryRequirements함수는 메모리 요구사항을 query(질의)하는 함수입니다.

(createVertexBuffer에 작성하면 됩니다. )

```
VkMemoryRequirements memRequirements;
vkGetBufferMemoryRequirements(device, vertexBuffer, &memRequirements);
```

VkMemoryRequirements는

size, aligment, memoryTypeBits 3가지 필드를 가지고 있습니다.

버퍼의 요구사항, application의 요구사항을 조합해서 올바른 memory type을 선택해야됩니다. 이를 위해서 findMemoryType이라는 함수를 생성해봅시다.

```
uint32_t findMemoryType(uint32_t typeFilter, VkMemoryPropertyFlags properties) {
    //...
}
```

첫 번째로

메모리 type에 대한 정보를 가져옵시다. (여기서 부터는 다시 findMemoryType에 )

```
VkPhysicalDeviceMemoryProperties memProperties;
vkGetPhysicalDeviceMemoryProperties(physicalDevice, &memProperties);
```

VkPhysicalDeviceMemoryProperties

* memoryHeaps: VRAM or RAM(VRAM이 부족할 경우) 과 같은 물리적으로 구분된 메모리 자원을 의미합니다.
* memoryTypes : Heap 안에 존재하는 메모리 type을 나타냅니다.

Buffer에 적합한 메모리 타입을 찾아봅시다.

```
for (uint32_t i = 0; i < memProperties.memoryTypeCount; i++) {
    if (typeFilter & (1 << i)) {
        return i;
    }
}
throw std::runtime_error("failed to find suitable memory type!");
```

typeFilter에 되어있는 bit mask를 통해서 올바른 메모리 type을 찾을 수 있습니다.

하지만 buffer에만 맞는 메모리 type이 아니라 CPU에서도 해당 메모리에 접근할 수 있어야합니다.

![](https://blog.kakaocdn.net/dna/nA4Km/btsNGr9dyBk/AAAAAAAAAAAAAAAAAAAAAPkHzXXji-Q1biTNE63VYjr7mwFGiiWx8XPrYW1dACvn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=E0pb5HUJ9JxD5DxrGd9i7SX7qL0%3D)

그렇기때문에

VK\_MEMORY\_PROPERTY\_HOST\_VISIBLE\_BIT

VK\_MEMORY\_PROPERTY\_HOST\_COHERENT\_BIT 속성을 포함하는 것도 추가해야됩니다.

```
for (uint32_t i = 0; i < memProperties.memoryTypeCount; i++) {
    if ((typeFilter & (1 << i)) &&
        (memProperties.memoryTypes[i].propertyFlags & properties) == properties) {
        return i;
    }
}
throw std::runtime_error("failed to find suitable memory type!");
```

### Memory Allocation

이제 메모리 type을 찾을 수 있으니, 메모리를 실제로 할당해봅시다.

```
VkMemoryAllocateInfo allocInfo{};
allocInfo.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;
allocInfo.allocationSize = memRequirements.size;
allocInfo.memoryTypeIndex = findMemoryType(
    memRequirements.memoryTypeBits,
    VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
);
```

**메모리 할당은 크기와 타입만 지정**해주면 되므로 간단합니다.

이 두 값은 위에서 만들어준 finMemoryType과 memoryRequirement에서 유도됩니다.

이제 handle을 만들고, 메모리를 할당해봅시다.

```
VkBuffer vertexBuffer;
VkDeviceMemory vertexBufferMemory;

...

if (vkAllocateMemory(device, &allocInfo, nullptr, &vertexBufferMemory) != VK_SUCCESS) {
    throw std::runtime_error("failed to allocate vertex buffer memory!");
}
```

메모리 할당이 성공했다면, 이제 이 메모리를 buffer에 연결(bind)할 수 있습니다.

```
vkBindBufferMemory(device, vertexBuffer, vertexBufferMemory, 0);
```

네 번째 파라미터는 메모리 영역 내의 오프셋입니다.

이 메모리는 vertex buffer 전용으로 할당된 것이므로, **오프셋은 0**입니다.  
(만약 오프셋이 0이 아니라면, memRequirements.alignment의 배수여야 합니다.)

이 handle 또한 cleanup에 추가해줘야합니다.

```
void cleanup() {
    cleanupSwapChain();

    vkDestroyBuffer(device, vertexBuffer, nullptr);
    vkFreeMemory(device, vertexBufferMemory, nullptr);
}
```

### Filling the Vertex Buffer

buffer를 만들어주고 binding까지 해줬으니, vertex data를 buffer에 복사해봅시다.

vkMapMemory를 통해서 buffer메모리에 cpu가 접근 가능한 영역으로 맵핑합니다.

```
void* data;
vkMapMemory(device, vertexBufferMemory, 0, bufferInfo.size, 0, &data);
```

이제 memcpy를 사용해 vertex data를 매핑된 메모리로 복사하고, vkUnmapMemory로 매핑을 해제하면 됩니다.

```
void* data;
vkMapMemory(device, vertexBufferMemory, 0, bufferInfo.size, 0, &data);
memcpy(data, vertices.data(), (size_t)bufferInfo.size);
vkUnmapMemory(device, vertexBufferMemory);
```

드라이버는 데이터를 즉시 실제 buffer 메모리에 복사하지 않을 수 있습니다.

이 문제를 해결하기 위해서 두 가지 방법이 존재합니다. 우리는 첫번째 방법을 사용합니다.

* VK\_MEMORY\_PROPERTY\_HOST\_COHERENT\_BIT 사용
* flush를 사용

메모리를 플러시하거나 VK\_MEMORY\_PROPERTY\_HOST\_COHERENT\_BIT 를 사용하는 것은 드라이버가 buffer에 쓴 내용을 인지하도록 만드는 것입니다.

그러나 **그 내용이 GPU에 즉시 보이는 것을 보장하지는 않습니다. 하지만** **다음 vkQueueSubmit 호출 시점까지는 전송이 완료되는 것은 보장합니다.**

### Binding the vertex buffer

마지막 단계를 렌더링 중에 vertex buffer를 binding 하는 것입니다. ( graphics pipeline에 우리의 vertex buffer를 붙혀주는 느낌)

이를 위해 recordCommandBuffer 함수를 확장해봅시다.

```
vkCmdBindPipeline(commandBuffer, VK_PIPELINE_BIND_POINT_GRAPHICS, graphicsPipeline);

VkBuffer vertexBuffers[] = {vertexBuffer};
VkDeviceSize offsets[] = {0};
vkCmdBindVertexBuffers(commandBuffer, 0, 1, vertexBuffers, offsets);

vkCmdDraw(commandBuffer, static_cast<uint32_t>(vertices.size()), 1, 0, 0);
```

vkCmdBindVertexBuffers 함수는 버텍스 버퍼를 **바인딩 슬롯(binding)** 에 연결합니다.

첫 번째, 두 번째 매개변수는 **바인딩 시작 인덱스**와 **바인딩 count를** 지정합니다.

마지막 매개변수는 vertex data를 읽기 시작할 **byte 단위 오프셋 배열**입니다.

vkCmdDraw 호출도 수정해줍시다.

 이제 실행시켜보면 익숙한 삼각형이 보일 것입니다.

![](https://blog.kakaocdn.net/dna/9zDvu/btsNFSNfqc8/AAAAAAAAAAAAAAAAAAAAADZmBoJqpxYJYWkGg8lMRk6MmQYPvF8vL92o3v5nNsT4/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Z1O9%2FInEZLfcmdiyFCNKcC2k8X8%3D)

우리가 vertex data를 잘 주고 있는건지 확인하기 위해서 색상을 바꿔봅시다

```
const std::vector<Vertex> vertices = {
    {{ 0.0f, -0.5f }, {1.0f, 1.0f, 1.0f}},  // 아래쪽 중앙 - 흰색
    {{ 0.5f,  0.5f }, {0.0f, 1.0f, 0.0f}},  // 오른쪽 위 - 초록색
    {{-0.5f,  0.5f }, {0.0f, 0.0f, 1.0f}},  // 왼쪽 위 - 파란색
};
```

![](https://blog.kakaocdn.net/dna/buPg38/btsNFusmoXa/AAAAAAAAAAAAAAAAAAAAABS1t5pHO64zAUD_4C5ij2Fs3jMkSdsTXkoxHYC0xbqt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=m0UgrOD559oi5IoLGaehJxC2kw4%3D)

좋습니다~

### Staging Buffer

지금 우리가 사용 중인 버텍스 버퍼는 정상적으로 작동하긴 하지만,  
**CPU가 접근할 수 있는 메모리 타입은 GPU가 읽기엔 최적이 아닐 수 있습니다.**

그래픽 카드 입장에서 최적인 메모리는 VK\_MEMORY\_PROPERTY\_DEVICE\_LOCAL\_BIT 속성을 가진 메모리이며,  
전용 GPU에서는 **CPU가 이 메모리에 직접 접근할 수 없습니다**.

이번 챕터에서는 두 개의 버텍스 버퍼를 만들 것입니다

**Staging Buffer:** cpu에서 접근 가능한 memory

여기에 vertex array의 data를 먼저 업로드합니다.

**Final Vertex Buffer:** (GPU에 최적화된) device local memory

stating buffer의 내용을 복사합니다.

### Transfer queue

buffer 복사 명령은 **전송 작업(transfer operations)** 을 지원하는 **큐 패밀리**가 필요합니다.  
해당 queue family는 VK\_QUEUE\_TRANSFER\_BIT 플래그로 표시됩니다.

다행히 대부분의 경우

VK\_QUEUE\_GRAPHICS\_BIT 또는 VK\_QUEUE\_COMPUTE\_BIT 기능을 가진 **모든 큐 패밀리**는 **암묵적으로 VK\_QUEUE\_TRANSFER\_BIT도 지원합니다.**

우리는 따로 transfer-only-queue(전송 전용 큐)를 찾지 않아도 됩니다.

### Abstracting buffer creation

이번 챕터에서는 여러 종류의 buffer를 만들 예정이므로, **버퍼 생성 코드를 별도 함수로 분리**하는 것이 좋습니다.  
이름은 createBuffer()로 하고, 기존 createVertexBuffer() 함수의 버퍼 생성 관련 코드를 이 함수로 옮깁니다:

```
void createBuffer(VkDeviceSize size, VkBufferUsageFlags usage,
                  VkMemoryPropertyFlags properties,
                  VkBuffer& buffer, VkDeviceMemory& bufferMemory) {
    VkBufferCreateInfo bufferInfo{};
    bufferInfo.sType = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO;
    bufferInfo.size = size;
    bufferInfo.usage = usage;
    bufferInfo.sharingMode = VK_SHARING_MODE_EXCLUSIVE;

    if (vkCreateBuffer(device, &bufferInfo, nullptr, &buffer) != VK_SUCCESS) {
        throw std::runtime_error("failed to create buffer!");
    }

    VkMemoryRequirements memRequirements;
    vkGetBufferMemoryRequirements(device, buffer, &memRequirements);

    VkMemoryAllocateInfo allocInfo{};
    allocInfo.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;
    allocInfo.allocationSize = memRequirements.size;
    allocInfo.memoryTypeIndex =
        findMemoryType(memRequirements.memoryTypeBits, properties);

    if (vkAllocateMemory(device, &allocInfo, nullptr, &bufferMemory) != VK_SUCCESS) {
        throw std::runtime_error("failed to allocate buffer memory!");
    }

    vkBindBufferMemory(device, buffer, bufferMemory, 0);
}
```

이렇게 createBuffer 함수를 만들었다면, createVertexBuffer함수도 간소화 할 수 있을 것 입니다.

```
void createVertexBuffer() {
    VkDeviceSize bufferSize = sizeof(vertices[0]) * vertices.size();

    createBuffer(bufferSize,
                 VK_BUFFER_USAGE_VERTEX_BUFFER_BIT,
                 VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT |
                 VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
                 vertexBuffer,
                 vertexBufferMemory);

    void* data;
    vkMapMemory(device, vertexBufferMemory, 0, bufferSize, 0, &data);
    memcpy(data, vertices.data(), (size_t)bufferSize);
    vkUnmapMemory(device, vertexBufferMemory);
}
```

### 

### Using a Staging Buffer

이제 createVertexBuffer 함수를 수정하여, **CPU에서 접근 가능한 버퍼를 임시로만 사용하고**,  
**실제 vertex buffer는 GPU 전용 디바이스 local memory에 생성**하도록 바꿀 것입니다.

```
void createVertexBuffer() {
    VkDeviceSize bufferSize = sizeof(vertices[0]) * vertices.size();

    VkBuffer stagingBuffer;
    VkDeviceMemory stagingBufferMemory;
    createBuffer(bufferSize,
                 VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
                 VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
                 stagingBuffer,
                 stagingBufferMemory);

    void* data;
    vkMapMemory(device, stagingBufferMemory, 0, bufferSize, 0, &data);
    memcpy(data, vertices.data(), (size_t)bufferSize);
    vkUnmapMemory(device, stagingBufferMemory);

    createBuffer(bufferSize,
                 VK_BUFFER_USAGE_TRANSFER_DST_BIT | VK_BUFFER_USAGE_VERTEX_BUFFER_BIT,
                 VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
                 vertexBuffer,
                 vertexBufferMemory);
}
```

이제 stagingBuffer와 stagingBufferMemory는 vertex data를 **임시로 담기 위한 buffer**입니다.

GPU만 접근 가능한 버퍼 플래그는 다음과 같습니다:

**VK\_BUFFER\_USAGE\_TRANSFER\_SRC\_BIT:** 해당 buffer가 **source**로 사용될 수 있음.

**VK\_BUFFER\_USAGE\_TRANSFER\_DST\_BIT:** 해당 buffer가 **destination**으로 사용될 수 있음.

**vertexBuffer는 이제 device local memory**에서 할당됩니다.  
이 메모리는 보통 vkMapMemory를 사용할 수 없습니다.

**하지만 stagingBuffer에서 vkCmdCopyBuffer를 통해 복사할 수는 있습니다.**

```
void copyBuffer(VkBuffer srcBuffer, VkBuffer dstBuffer, VkDeviceSize size) {
    VkCommandBufferAllocateInfo allocInfo{};
    allocInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;
    allocInfo.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
    allocInfo.commandPool = commandPool;
    allocInfo.commandBufferCount = 1;

    VkCommandBuffer commandBuffer;
    vkAllocateCommandBuffers(device, &allocInfo, &commandBuffer);
```

바로 command buffer에 기록합시다.

```
    VkCommandBufferBeginInfo beginInfo{};
    beginInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
    beginInfo.flags = VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT;

    vkBeginCommandBuffer(commandBuffer, &beginInfo);
```

**VK\_COMMAND\_BUFFER\_USAGE\_ONE\_TIME\_SUBMIT\_BIT:**해당 command buffer가 한번만 사용될 것임을 드라이버에 알려줘 최적화에 도움을 줍니다.

vkCmdCopyBuffer 함수를 통해서 복사를 해줍시다.

```
    VkBufferCopy copyRegion{};
    copyRegion.srcOffset = 0; // 생략 가능
    copyRegion.dstOffset = 0; // 생략 가능
    copyRegion.size = size;

    vkCmdCopyBuffer(commandBuffer, srcBuffer, dstBuffer, 1, &copyRegion);
    vkEndCommandBuffer(commandBuffer);
```

이 command buffer는 복사를 위한 command이기 때문에, record를 바로 멈추고, 실행이 완료되길 기다립니다.

```
    VkSubmitInfo submitInfo{};
    submitInfo.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO;
    submitInfo.commandBufferCount = 1;
    submitInfo.pCommandBuffers = &commandBuffer;

    vkQueueSubmit(graphicsQueue, 1, &submitInfo, VK_NULL_HANDLE);
    vkQueueWaitIdle(graphicsQueue);
```

여기서는 단순히 전송(transfer)만 완료되기를 기다리면 됩니다.

vkQueueWaitIdle를 통해서 복사 작업이 끝나는 것을 기다립니다.

( fence를 사용해서 여러 작업을 비동기적으로 관리할 수 있습니다.)

```
    vkFreeCommandBuffers(device, commandPool, 1, &commandBuffer);
    }
```

복사작업에서 사용된 임시 command buffer를 해제합니다.

이제 createVertexBuffer()에서 copyBuffer()를 호출하고, staging buffer를 없애주시면 됩니다.

```
createBuffer(bufferSize,
             VK_BUFFER_USAGE_TRANSFER_DST_BIT | VK_BUFFER_USAGE_VERTEX_BUFFER_BIT,
             VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
             vertexBuffer,
             vertexBufferMemory);

copyBuffer(stagingBuffer, vertexBuffer, bufferSize);

vkDestroyBuffer(device, stagingBuffer, nullptr);
vkFreeMemory(device, stagingBufferMemory, nullptr);
```

이제 실행시켜보면 역시나 잘 동작하는 것을 볼 수 있을 것입니다!!

하지만 vkAllocateMemory를 매번 호출하는 것은 좋은 방식은 아닙니다

vkAllocateMemory를 통한 **동시 메모리 할당의 최대 수가 정해져있고, 고성능 GPU도 ( 4096개 정도가 최대입니다 )**

많은 객체에 대해 메모리를 한꺼번에 할당하려면,  
**하나의 메모리 블록을 여러 객체에 나눠서 사용하는 custom allocator** 를 구현하는 것이 올바른 방식입니다.  
이때는 여러 Vulkan 함수에서 등장한 **offset 파라미터를 활용하여** 메모리 내에서 구간을 나누게 됩니다.

 ( 물론 튜토리얼에서는 상관없음 )

이거를 사용하다고 하네요

<https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator>

[GitHub - GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator: Easy to integrate Vulkan memory allocation library

Easy to integrate Vulkan memory allocation library - GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator

github.com](https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator)

### Index Buffer

![](https://blog.kakaocdn.net/dna/cFGyiA/btsNGBEHOfx/AAAAAAAAAAAAAAAAAAAAAHNNHzCW3htarl27evcODrQUJ-1Sh30qSue9YqilNom1/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FrQiCXuXjRKsZIgzyQxW8Cm%2FG2I%3D)

인덱스 버퍼는 **정점 버퍼를 참조하는 인덱스 배열**입니다.

(잘 아시겠지만**, 중복 없이 하나의 정점을 여러 삼각형에서 재사용**할 수 있게 해주는 친구입니다.)

사각형을 그려봅시다.

```
const std::vector<Vertex> vertices = {
    {{-0.5f, -0.5f}, {1.0f, 0.0f, 0.0f}}, // 아래 왼쪽: 빨간색
    {{ 0.5f, -0.5f}, {0.0f, 1.0f, 0.0f}}, // 아래 오른쪽: 초록색
    {{ 0.5f,  0.5f}, {0.0f, 0.0f, 1.0f}}, // 위 오른쪽: 파란색
    {{-0.5f,  0.5f}, {1.0f, 1.0f, 1.0f}}  // 위 왼쪽: 흰색
};
```

```
const std::vector<uint16_t> indices = {
    0, 1, 2,  // 첫 번째 삼각형
    2, 3, 0   // 두 번째 삼각형
};
```

정점 수가 65535개 미만이면 uint16\_t로 충분합니다.

항상 하던 것과 같이, 인덱스 버퍼와 메모리를 멤버 변수로 선언합니다.

```
VkBuffer vertexBuffer;
VkDeviceMemory vertexBufferMemory;
VkBuffer indexBuffer;
VkDeviceMemory indexBufferMemory;
```

createVertexBuffer()와 거의 동일하게 동작하지만,  
**usage 플래그 +** **인덱스 데이터를 처리**한다는 점이 다릅니다.

```
void createIndexBuffer() {
    VkDeviceSize bufferSize = sizeof(indices[0]) * indices.size();

    VkBuffer stagingBuffer;
    VkDeviceMemory stagingBufferMemory;

    // CPU에서 접근 가능한 임시 버퍼 생성
    createBuffer(bufferSize, 
                 VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
                 VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
                 stagingBuffer, stagingBufferMemory);

    // 인덱스 데이터 복사
    void* data;
    vkMapMemory(device, stagingBufferMemory, 0, bufferSize, 0, &data);
    memcpy(data, indices.data(), (size_t)bufferSize);
    vkUnmapMemory(device, stagingBufferMemory);

    // GPU 전용 인덱스 버퍼 생성
    createBuffer(bufferSize,
                 VK_BUFFER_USAGE_TRANSFER_DST_BIT | VK_BUFFER_USAGE_INDEX_BUFFER_BIT,
                 VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
                 indexBuffer, indexBufferMemory);

    // 스테이징 버퍼에서 실제 인덱스 버퍼로 복사
    copyBuffer(stagingBuffer, indexBuffer, bufferSize);

    // 스테이징 버퍼 제거
    vkDestroyBuffer(device, stagingBuffer, nullptr);
    vkFreeMemory(device, stagingBufferMemory, nullptr);
}
```

vertex buffer 정리할 때 같이 정리해줍시다.

```
void cleanup() {
    cleanupSwapChain();

    vkDestroyBuffer(device, indexBuffer, nullptr);
    vkFreeMemory(device, indexBufferMemory, nullptr);

    vkDestroyBuffer(device, vertexBuffer, nullptr);
    vkFreeMemory(device, vertexBufferMemory, nullptr);

    ...
}
```

### Using an index buffer

인덱스 버퍼를 사용하여 렌더링하려면, recordCommandBuffer 함수에 두 가지 변경이 필요합니다.

1. index buffer binding

```
vkCmdBindVertexBuffers(commandBuffer, 0, 1, vertexBuffers, offsets);

vkCmdBindIndexBuffer(commandBuffer, indexBuffer, 0, VK_INDEX_TYPE_UINT16);
```

2. chaing drawing command

```
vkCmdDrawIndexed(commandBuffer,
    static_cast<uint32_t>(indices.size()), 1, 0, 0, 0);
```

따란 드디어 indexing을 사용해서 사각형을 그렸다!!

![](https://blog.kakaocdn.net/dna/bidGoJ/btsNE49b01V/AAAAAAAAAAAAAAAAAAAAAGd6cIkoPZuTyzBKVzU4EBa8ZF5AIBsJHVAz_1mhii06/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=XTgRJ4NO7Zg0j5wmQ8gEYutb5L4%3D)