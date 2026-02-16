---
title: "[Vulkan] Uniform Buffer"
date: 2025-05-14
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### Descriptor layout and buffer

우리는 이제 각 vertex에 대해 임의의 attribute을 vertex shader에 전달할 수 있게 되었지만, 글로벌 변수는에 대해서는 배우지 않았습니다.

이번 장부터는 **3D 그래픽스**로 넘어가게 되며, 그에 따라 Model-View-Projection Matrix(일명 MVP matrix)가 필요해집니다.

이 행렬을 vertex data로 포함시키는 것도 가능하지만, 그렇게 하면 **메모리가 낭비**되고, 변환될 때마다 vertex buffer를 갱신해야 합니다. 특히, **변환은 매 프레임마다 생길 수 있기 때문에** 비효율적입니다.

Vulkan에서 이 문제를 해결하는 좋은 방법은 **Resource Descriptor**를 사용하는 것입니다.

**descriptor는 shader가 buffer나 이미지 같은 리소스에 자유롭게 접근**할 수 있도록 해주는 메커니즘입니다.

**우리는 변환 행렬들을 담고 있는 버퍼를 만들고,** **vertex shader가 descriptor를 통해 해당 버퍼에 접근**하도록 설정할 것입니다.

디스크립터를 사용하는 과정은 다음의 세 단계로 구성됩니다

1. **파이프라인 생성 시 descriptor layout 생성**
2. **descriptor pool 로부터 descriptor set 할당**
3. **렌더링 시 descriptor set 바인딩**

**descriptor layout은 파이프라인에서 접근할 리소스 타입을 명시하는 역할을 하며,** **렌더 패스가 접근할 첨부 이미지 타입을 명시하는 것과 유사합니다.**  
**descriptor set는** **실제 buffer나 이미지 리소스를 지정하며, 프레임버퍼가 실제 이미지 뷰를 지정하는 것과 같은 역할을 합니다.**

이후, 해당 descriptor  set를 그리기 명령 시 바인딩하여 사용합니다. 이는 vertex buffer나 framebuffer를 바인딩하는 방식과 동일합니다.

descriptor에는 여러 타입이 존재하지만, 이번 장에서는 UBO(uniform buffer object)만 다룹니다.

아래와 같은 정보가 필요하다고 가정해봅시다.

```
struct UniformBufferObject {
    glm::mat4 model;
    glm::mat4 view;
    glm::mat4 proj;
};
```

이 데이터를 VkBuffer에 복사하고, shader에서는 uniform buffer descriptor를 통해 다음과 같이 접근할 수 있습니다

vertex  shader

```
#version 450

layout(binding = 0) uniform UniformBufferObject {
    mat4 model;
    mat4 view;
    mat4 proj;
} ubo;

layout(location = 0) in vec2 inPosition;
layout(location = 1) in vec3 inColor;

layout(location = 0) out vec3 fragColor;

void main() {
    gl_Position = ubo.proj * ubo.view * ubo.model * vec4(inPosition, 0.0, 1.0);
    fragColor = inColor;
}
```

우리는 model, view, projection 행렬을 갱신하여, 이전 장에서 만든 사각형이 3D 공간에서 회전하도록 만들어 볼 것 입니다.  (여기까지 오신 분들이라면 mvp matrix를 왜 이렇게 곱하는 지는 잘 알고 있겠죠?  ^^ )

### Descriptor Set Layout

이제 C++ 쪽에서 UBO(Uniform Buffer Object)를 정의하고, 해당 descriptor가 vertex shader에 사용된다는 사실을 Vulkan에 알려야 합니다.

```
struct UniformBufferObject {
    glm::mat4 model;
    glm::mat4 view;
    glm::mat4 proj;
};
```

 

GLM의 행렬 데이터는 shader에서 기대하는 바이너리 구조와 호환되므로, 나중에 UniformBufferObject를 VkBuffer에 memcpy로 그대로 복사해도 문제 없습니다.

shader에서 사용하는 각 descriptor 바인딩에 대해 **파이프라인 생성 시 명시**해야 합니다. 이는 vertex attribute와 해당 location 인덱스를 정의했던 방식과 유사합니다.

**우리는 이를 처리할 createDescriptorSetLayout()이라는 함수를 새로 만들고, 그래픽스 파이프라인을 생성하기 전에 호출해야 합니다.**

```
void initVulkan() {
    ...
    createDescriptorSetLayout();
    createGraphicsPipeline();
    ...
}
```

descriptor layout을 정의하려면 각 바인딩에 대해 VkDescriptorSetLayoutBinding 구조체를 채워야 합니다.

```
void createDescriptorSetLayout() {
    VkDescriptorSetLayoutBinding uboLayoutBinding{};
    uboLayoutBinding.binding = 0;
    uboLayoutBinding.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
    uboLayoutBinding.descriptorCount = 1;
```

binding = 0은 셰이더의 layout(binding = 0)과 일치해야 합니다.

descriptorType은 이 바인딩이 uniform buffer임을 나타냅니다.

descriptorCount = 1은 배열이 아닌 단일 UBO를 의미합니다.  
(예: bone 애니메이션처럼 여러 개의 UBO가 필요한 경우 배열을 만들고 카운트를 늘릴 수 있습니다.)

```
    uboLayoutBinding.stageFlags = VK_SHADER_STAGE_VERTEX_BIT;
```

stageFlags는 이 descriptor가 참조되는 shader를 알리는 단계입니다.

(vertex라고 알려주는 모습)

VK\_SHADER\_STAGE\_ALL\_GRAPHICS와 같이 여러 shader stage를 동시에 지정할 수도 있습니다.'

```
    uboLayoutBinding.pImmutableSamplers = nullptr; // 이미지 샘플링용이 아니므로 생략 가능
```

pImmutableSamplers는 텍스처 샘플러와 관련된 descriptor에서만 필요하므로 지금은 무시해도 됩니다.

이제 모든 descriptor 바인딩들을 하나의 VkDescriptorSetLayout 객체로 결합합니다.

아래 변수들은 멤버 변수로 선언합시다.

```
VkDescriptorSetLayout descriptorSetLayout;
VkPipelineLayout pipelineLayout;
```

다음으로 vkCreateDescriptorSetLayout를 사용해 레이아웃 객체를 생성합니다:

```
VkDescriptorSetLayoutCreateInfo layoutInfo{};
layoutInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO;
layoutInfo.bindingCount = 1;
layoutInfo.pBindings = &uboLayoutBinding;

if (vkCreateDescriptorSetLayout(device, &layoutInfo, nullptr, &descriptorSetLayout) != VK_SUCCESS) {
    throw std::runtime_error("failed to create descriptor set layout!");
}
```

파이프라인 생성 시, Vulkan에 어떤 descriptor들이 사용될지 알려주기 위해 **descriptor layout을** **파이프라인 layout에 명시해야** 합니다

```
VkPipelineLayoutCreateInfo pipelineLayoutInfo{};
pipelineLayoutInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO;
pipelineLayoutInfo.setLayoutCount = 1;
pipelineLayoutInfo.pSetLayouts = &descriptorSetLayout;​
```

**descriptor layout** 은 프로그램이 종료되거나 새로운 그래픽스 파이프라인을 만들기 전까지 유지되어야 합니다.

```
void cleanup() {
    cleanupSwapChain();
    vkDestroyDescriptorSetLayout(device, descriptorSetLayout, nullptr);
    ...
}
```

### Uniform Buffer

우선 Uniform Buffer를 **먼저 생성합시다.**

**1. Staging  buffer 사용안할게요**

우리는 값이 변경될 때마다 (매 frame마다 변경시킴) UBO에 **새로운 데이터를 복사**해야 하므로, **여기서 staging buffer를 사용하는 것은 오히려** **오버헤드만 증가시키고 성능을** 저하시킬 수 있습니다. (맵핑/언매핑 시키는 것도 비용이 듭니다)

따라서 이 경우에는 staging buffer를 쓰지 않는 것이 더 적절합니다.

**2. uniform buffer 수를 frame 수 만큼 만들게요**

**이전 프레임이 GPU에서 해당 버퍼를 읽고 있는 도중**에, **CPU가 다음 프레임을 위한 데이터를 덮어쓰게 되는** 상황이 생길 수 있습니다.

이를 피하기 위해, **프레임 수만큼의 유니폼 버퍼**를 생성하고, **현재 GPU가 읽고 있지 않은 버퍼에만 데이터를 쓰는 방식**으로 처리해야 합니다.

멤버 변수를 추가해봅시다.

```
VkBuffer indexBuffer;
VkDeviceMemory indexBufferMemory;

std::vector<VkBuffer> uniformBuffers;
std::vector<VkDeviceMemory> uniformBuffersMemory;
std::vector<void*> uniformBuffersMapped;
```

createIndexBuffer() 호출 이후에 createUniformBuffers()를 호출하여 초기화합시다.

```
void initVulkan() {
    ...
    createVertexBuffer();
    createIndexBuffer();
    createUniformBuffers();
    ...
}
```

createUniformBuffers() 함수 정의는 다음과 같습니다:

```
void createUniformBuffers() {
    VkDeviceSize bufferSize = sizeof(UniformBufferObject);

    uniformBuffers.resize(MAX_FRAMES_IN_FLIGHT);
    uniformBuffersMemory.resize(MAX_FRAMES_IN_FLIGHT);
    uniformBuffersMapped.resize(MAX_FRAMES_IN_FLIGHT);

    for (size_t i = 0; i < MAX_FRAMES_IN_FLIGHT; i++) {
        createBuffer(
            bufferSize,
            VK_BUFFER_USAGE_UNIFORM_BUFFER_BIT,
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
            uniformBuffers[i],
            uniformBuffersMemory[i]
        );

        vkMapMemory(device, uniformBuffersMemory[i], 0, bufferSize, 0, &uniformBuffersMapped[i]);
    }
}
```

### Persistent Mapping

buffer는 생성하자마자 vkMapMemory를 호출하여 **포인터를 미리 매핑**해둡니다.

이 포인터는 계속 맵핑하는 번거로움을 피하기 위해서 전체 실행 시간 동안 **계속 유지시키겠습니다.**

이러한 방식을 Persistent Mapping이라 불리며, 모든 Vulkan 구현에서 지원됩니다.

매번 매핑/언매핑하는 것은 비용이 크기 때문에 ( 변환 행렬에서 사용하려고 만들고 있는데, 변환행렬은 매 frame마다 바뀔 가능성이 높다. 그럼 매 프레임마다 매핑/언매핑을 계~~~속 하는 것이다.. 이걸 피하자는 것이다)

**성능 향상을 위해 영구적으로 매핑이 유리**합니다.

uniform data는 모든 드로우 콜에서 사용되므로, **렌더링이 완전히 종료되기 전까지**는 버퍼를 해제하지 않아야 합니다.

cleanup()

```
void cleanup() {
    ...
    for (size_t i = 0; i < MAX_FRAMES_IN_FLIGHT; i++) {
        vkDestroyBuffer(device, uniformBuffers[i], nullptr);
        vkFreeMemory(device, uniformBuffersMemory[i], nullptr);
    }

    vkDestroyDescriptorSetLayout(device, descriptorSetLayout, nullptr);
    ...
}
```

### Updating Uniform Data

새로운 함수를 만들어 매 프레임마다 UBO를 업데이트합시다.

이 함수는 drawFrame() 함수 내에서 **다음 frame을 제출하기 전에** 호출되어야 합니다.

```
void drawFrame() {
    ...
    updateUniformBuffer(currentFrame);
    ...
    VkSubmitInfo submitInfo{};
    submitInfo.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO;
    ...
}
```

```
void updateUniformBuffer(uint32_t currentImage) {
}
```

이 함수는 **geometry가 회전하도록 매 frame마다 새로운 변환 행렬**을 업데이트할 것입니다.

수학 함수를 사용하기 위해서 추가할 코드들이 있습니다.

```
#define GLM_FORCE_RADIANS // 단위는 라디안
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp> // glm::rotate, glm::lookAt, glm::perspective 이런 함수 지원
#include <chrono> //시간측정
```

초당 회전을 위해서 시간을 재봅시다.

```
void updateUniformBuffer(uint32_t currentImage) {
    static auto startTime = std::chrono::high_resolution_clock::now();

    auto currentTime = std::chrono::high_resolution_clock::now();
    float time = std::chrono::duration<float, std::chrono::seconds::period>(currentTime - startTime).count();
```

### 

모델(Model) 행렬 – Z축 기준 회전

```
    UniformBufferObject ubo{};
    ubo.model = glm::rotate(glm::mat4(1.0f), time * glm::radians(90.0f), glm::vec3(0.0f, 0.0f, 1.0f));
```

첫번째 인자: 회전을 적용할 대상 행렬 ( 아직 뭐 없으니 Identity mat으로 )

뷰(View) 행렬 – 카메라 위치

```
    ubo.view = glm::lookAt(
        glm::vec3(2.0f, 2.0f, 2.0f),  // eye: 카메라 위치
        glm::vec3(0.0f, 0.0f, 0.0f),  // center: 바라보는 지점
        glm::vec3(0.0f, 0.0f, 1.0f)   // up: 위쪽 방향
    );
```

대각선 위에서 정면을 내려다보는 시점 구성.

투영(Projection) 행렬 – 원근 투영

```
    ubo.proj = glm::perspective(
        glm::radians(45.0f), 
        swapChainExtent.width / (float)swapChainExtent.height, 
        0.1f, 10.0f
    );​
```

Y축 반전

```
    ubo.proj[1][1] *= -1;
```

GLM은 기본적으로 OpenGL 기준이므로, Vulkan과 달리 **Y축이 반대로** 되어 있습니다. ( frame buffer에서 y가 위로 올라갈 수 록 값이 낮아졌던 것을 공부했었다..!)

### UBO 데이터 버퍼에 복사

모든 행렬이 정의되었으면, ubo 구조체를 해당 프레임의 유니폼 버퍼에 복사합시다.

```
    memcpy(uniformBuffersMapped[currentImage], &ubo, sizeof(ubo));
}
```

UBO는 **변경 빈도가 높은 데이터**를 넘기기에는 효율이 떨어질 수 있습니다.

Vulkan에서는 **Push Constant**라는 더 빠른 방법이 존재하며, 뒤에서 다룰 예정입니다.

### Descriptor pool and sets

이전 장에서 만든 **descriptor layout**은 shader에서 참조할 **descriptor**의 유형을 정의했다.  
이번 장에서는 각 VkBuffer 리소스를 **uniform buffer descriptor**에 바인딩할 수 있도록 **descriptor set**을 생성한다.

### Descriptor Pool

descriptor set은 직접 생성할 수 없고, 반드시 **descriptor pool**에서 **할당** 받아야 한다.  
이를 위해 createDescriptorPool() 함수를 작성한다:

```
void initVulkan() {
    ...
    createUniformBuffers();
    createDescriptorPool();
    ...
}
```

```
VkDescriptorPoolSize poolSize{};
poolSize.type = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
poolSize.descriptorCount = static_cast<uint32_t>(MAX_FRAMES_IN_FLIGHT);
```

이 pool은 uniform buffer descriptor를 프레임 수만큼 보유할 수 있도록 설정

```
VkDescriptorPoolCreateInfo poolInfo{};
poolInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO;
poolInfo.poolSizeCount = 1;
poolInfo.pPoolSizes = &poolSize;
poolInfo.maxSets = static_cast<uint32_t>(MAX_FRAMES_IN_FLIGHT);
```

VK\_DESCRIPTOR\_POOL\_CREATE\_FREE\_DESCRIPTOR\_SET\_BIT 플래그는 동적으로 descriptor set을 해제할 때만 필요하다.

여기선 생성 후 수정하지 않으므로 생략 가능.

```
 VkDescriptorPool descriptorPool;
 
 
 // ...
 
 
 if (vkCreateDescriptorPool(device, &poolInfo, nullptr, &descriptorPool) != VK_SUCCESS) {
    throw std::runtime_error("failed to create descriptor pool!");
}
```

### Descriptor Set

### 이제 descriptor set을 할당해보자

```
void initVulkan() {
    ...
    createDescriptorPool();
    createDescriptorSets();
    ...
}

void createDescriptorSets() {
    std::vector<VkDescriptorSetLayout> layouts(MAX_FRAMES_IN_FLIGHT, descriptorSetLayout);
    VkDescriptorSetAllocateInfo allocInfo{};
    allocInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO;
    allocInfo.descriptorPool = descriptorPool;
    allocInfo.descriptorSetCount = static_cast<uint32_t>(MAX_FRAMES_IN_FLIGHT);
    allocInfo.pSetLayouts = layouts.data();
}
```

.

여기서는 Frame in Flight마다 하나씩 descriptor set를 생성한다.

클래스 멤버로 descriptor set 핸들을 저장하는 벡터를 만들고 vkAllocateDescriptorSets로 할당합시다.

```
VkDescriptorPool descriptorPool;
std::vector<VkDescriptorSet> descriptorSets;
...
descriptorSets.resize(MAX_FRAMES_IN_FLIGHT);
if (vkAllocateDescriptorSets(device, &allocInfo, descriptorSets.data()) != VK_SUCCESS) {
    throw std::runtime_error("failed to allocate descriptor sets!");
}
```

descriptor set는 명시적으로 해제할 필요는 없다. descriptor pool을 제거할 때 자동으로 모두 해제된다.

**이 vkAllocateDescriptorSets 호출은 각 프레임마다 하나의 uniform buffer descriptor를 가진 descriptor set을 할당한다.**

cleanup

```
void cleanup() {
    ...
    vkDestroyDescriptorPool(device, descriptorPool, nullptr);
    vkDestroyDescriptorSetLayout(device, descriptorSetLayout, nullptr);
    ...
}
```

이제 descriptor set은 할당되었지만, 내부의 descriptor 설정은 아직 남아 있다. 각 set에 대해 반복하면서 구성 정보를 채워야 합니다.

```
for (size_t i = 0; i < MAX_FRAMES_IN_FLIGHT; i++) {
    VkDescriptorBufferInfo bufferInfo{};
    bufferInfo.buffer = uniformBuffers[i];
    bufferInfo.offset = 0;
    bufferInfo.range = sizeof(UniformBufferObject);
```

버퍼 전체를 사용할 경우에는 range에 VK\_WHOLE\_SIZE를 사용할 수 있습니다.

VkWriteDescriptorSet 구조체를 채워서 DescriptorSet을 업데이트합시다.

```
VkWriteDescriptorSet descriptorWrite{};
descriptorWrite.sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
descriptorWrite.dstSet = descriptorSets[i];         // 업데이트할 descriptor set
descriptorWrite.dstBinding = 0;                      // shader에서 설정한 binding index
descriptorWrite.dstArrayElement = 0;                 // 배열형일 경우 시작 인덱스 (여기선 0)
descriptorWrite.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
descriptorWrite.descriptorCount = 1;


descriptorWrite.pBufferInfo = &bufferInfo;
descriptorWrite.pImageInfo = nullptr;       // 이미지 타입이 아니므로 사용 안 함
descriptorWrite.pTexelBufferView = nullptr; // 텍셀 버퍼 뷰도 사용 안 함

vkUpdateDescriptorSets(device, 1, &descriptorWrite, 0, nullptr);
```

```
void cleanup() {
    ...
    vkDestroyDescriptorPool(device, descriptorPool, nullptr);
    vkDestroyDescriptorSetLayout(device, descriptorSetLayout, nullptr);
    ...
}
```

### Using Descriptor Set

이제 recordCommandBuffer 함수를 수정하여, 매 프레임마다 올바른 **descriptor set**을 **shader**에 바인딩하도록 합시다.

**이 작업은 반드시 vkCmdDrawIndexed 호출 전에 수행되어야 합니다!!**

```
vkCmdBindDescriptorSets(
    commandBuffer,
    VK_PIPELINE_BIND_POINT_GRAPHICS,
    pipelineLayout,
    0,
    1,
    &descriptorSets[currentFrame],
    0,
    nullptr
);

vkCmdDrawIndexed(
    commandBuffer,
    static_cast<uint32_t>(indices.size()),
    1,
    0,
    0,
    0
);
```

**Vertex buffer나 index buffer와는 달리, descriptor set은 graphics pipeline에만 국한되지 않고, compute pipeline에도 사용될 수 있습니다.**

그래서 vkCmdBindDescriptorSets에서 pipeline 종류를 명확하게 지정해줘야됩니다.

여기서는 VK\_PIPELINE\_BIND\_POINT\_GRAPHICS로 설정합시다.

이제 실행시키면?  
아마 검정화면만 등장할 것입니다 하하

저희가 projection matrix의 y축에 -1을 곱해줬었는데 그것 때문입니다. 지금은 반시계 방향으로 그려지고 있기 때문에 rasterizer를 조금 수정해줍시다.

```
rasterizer.cullMode = VK_CULL_MODE_BACK_BIT;
rasterizer.frontFace = VK_FRONT_FACE_COUNTER_CLOCKWISE;
```

이제 빙글빙글 돌아가는 사각형을 볼 수 있을 겁니다

![](https://blog.kakaocdn.net/dna/VkpZi/btsNHxC1x5M/AAAAAAAAAAAAAAAAAAAAAKHr3pz56klglurWdbDUvtS5_0B9T3-j7-pJK3ariAfx/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=jeKvt7rH3%2BdVBdxuK5fKFUXz9Yk%3D)

### 

### Alignment

지금까지는 C++ 구조체의 데이터가 shader의 uniform 정의와 정확히 어떻게 일치해야 하는지를 생각을 안했을 겁니다.

겉보기에는 타입만 맞춰주면 될 것같은 느낌이였죠? 하지만 조금 더 신경써야할 부분이 있습니다.

우리가 사용하던 구조체를 아래처럼 수정해보면 어떻게 될까요?

```
struct UniformBufferObject {
    glm::vec2 foo;
    glm::mat4 model;
    glm::mat4 view;
    glm::mat4 proj;
};

layout(binding = 0) uniform UniformBufferObject {
    vec2 foo;
    mat4 model;
    mat4 view;
    mat4 proj;
} ubo;
```

사각형이 사라집니다..

Vulkan에는 메모리 정렬 규칙이 있습니다.

구조체 내부 멤버 변수의 기준 정렬값을 **16바이트 배수로 반올림해서 정렬한다는 것입니다.**

**mat4는 float4개로 구성되어있습니다. 4btye \* 4로 16byte입니다. 그래서 mat4로만 구성된 우리의 uniform은 정상적으로 작동했던 것입니다.**

하지만 vec2 foo가 끼면서 엉켜버리게된거죠...

그래서 16byte로 정렬해줄 필요가 있습니다.

```
struct UniformBufferObject {
    glm::vec2 foo;
    alignas(16) glm::mat4 model;
    glm::mat4 view;
    glm::mat4 proj;
};
```

또는 이렇게 매크로로 자동정렬을 시킬 수 있지만, 구조체가 중첩됐을 때 작동이 잘 안됩니다. 그냥 매크로로 합시다!

```
#define GLM_FORCE_RADIANS
#define GLM_FORCE_DEFAULT_ALIGNED_GENTYPES
#include <glm/glm.hpp>
```

```
// uniform buffer
struct UnifromBufferObject
{
	alignas(16) glm::mat4 model;
	alignas(16)	glm::mat4 view;
	alignas(16)	glm::mat4 proj;
};
```

### 

### Multiple Descriptor Sets

**여러 개의 descriptor set을 동시에 바인딩**하는 것도 가능합니다. 이를 위해서는 **pipeline layout을 생성할 때**, 각각의 descriptor set에 대한 layout을 명시해줘야됩니다.

그리고 shader에서는 다음과 같이 특정 descriptor set을 참조할 수 있습니다.

```
layout(set = 0, binding = 0) uniform UniformBufferObject { ... }
```

이 기능은 다음과 같은 경우에 유용하게 사용된다:

**오브젝트마다 다른 descriptor를 사용할 때,**

**모든 오브젝트에서 공유되는 descriptor를** **서로 다른 descriptor set에 분리해서 배치할 때**

이렇게 구성하면 **draw call마다 대부분의 descriptor를 다시 바인딩할 필요 없이**, 꼭 필요한 일부만 바꾸면 되므로 성능상 이점이 생기게 됩니다.

사용하는 예시입니다.

```
layout(set = 0, binding = 0) uniform UniformBufferObject {
    mat4 model;
} ubo;

layout(set = 1, binding = 0) uniform sampler2D texSampler;
```

set = 0: 오브젝트마다 다른 model matrix

set = 1: 모든 오브젝트에서 공통으로 사용하는 텍스처