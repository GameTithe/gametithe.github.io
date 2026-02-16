---
title: "[Vulkan] Loading Models"
date: 2025-05-15
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### Loading Models

이 장에서는 실제 model 파일에서 vertex와 index 데이터를 불러와 그래픽 카드가 더 많은 일을 하도록 확장해보겠습니다.  
많은 그래픽스 API 튜토리얼에서는 이 단계에서 직접 OBJ 로더를 작성하도록 유도하지만, OBJ 포맷은 skeletal animation처럼 복잡한 기능을 지원하지 않기 때문에 한계가 있습니다.  
이 장에서는 OBJ 모델에서 mesh 데이터를 불러오되, 파일 파싱 자체보다는 불러온 데이터를 프로그램에 어떻게 통합할지에 초점을 맞춥니다.

### Library

OBJ 파일에서 vertex와 face 정보를 불러오기 위해 tinyobjloader 라이브러리를 사용합니다. 이 라이브러리는 빠르고, stb\_image처럼 하나의 헤더 파일만 포함하면 되기 때문에 통합이 간단합니다.  
상단에 있는 저장소 링크에서 tiny\_obj\_loader.h 파일을 다운로드해 프로젝트의 라이브러리 디렉토리에 저장하세요.

**Visual Studio**  
tiny\_obj\_loader.h 파일이 있는 디렉토리를 **Additional Include Directories** 경로에 추가합니다.

<https://github.com/tinyobjloader/tinyobjloader>

[GitHub - tinyobjloader/tinyobjloader: Tiny but powerful single file wavefront obj loader

Tiny but powerful single file wavefront obj loader - tinyobjloader/tinyobjloader

github.com](https://github.com/tinyobjloader/tinyobjloader)

여기서 다운을 받고, 헤더 파일이 있을거예요 그걸 Libraries에 넣고,

![](https://blog.kakaocdn.net/dna/dHgmpY/btsNUTfllgu/AAAAAAAAAAAAAAAAAAAAANyiXFvrYyDD2W74yrHI89tlJFnxJyU02yCEaBKlp-sm/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=kCSm79tBKsvQZagWydKnvU7x1PQ%3D)

이렇게 경로 설정해주면 사용할 수 있습니다.

### Sample mesh

Sketchfab에서 3D 스캔 모델을 찾아보면 OBJ 형식 모델이 많습니다. 본 튜토리얼에서는 nigelgoh의 Viking room 모델(CC BY 4.0)을 사용합니다. 크기와 방향을 약간 조절하여 드롭인 교체할 수 있게 했습니다:

=> 지금 이게 다운이 안되는것 같아서 Cyberpunk bike (daCruz) 로 했습니다.

자신의 모델을 사용해도 무방하지만, 반드시 하나의 머티리얼(material)로만 이루어져 있고 대략 1.5 × 1.5 × 1.5 단위 크기를 갖은 모델을 사용합시다.   
더 크면 뷰 행렬(view matrix)을 조정해야 합니다. 프로젝트 디렉터리 내에 shaders와 textures 옆에 models 디렉터리를 만들고 모델 파일을, textures 디렉터리에는 텍스처 이미지를 넣습니다.

다음처럼 프로그램에 모델과 텍스처 경로를 정의하는 설정 변수를 두 개 추가합시다.

```
const uint32_t WIDTH  = 800;
const uint32_t HEIGHT = 600;

const std::string MODEL_PATH   = "models/viking_room.obj";
const std::string TEXTURE_PATH = "textures/viking_room.png";
```

그리고 createTextureImage 함수를 다음과 같이 경로 변수를 사용하도록 업데이트합시다.

```
stbi_uc* pixels = stbi_load(
    TEXTURE_PATH.c_str(),
    &texWidth,
    &texHeight,
    &texChannels,
    STBI_rgb_alpha
);
```

### Loading vertices and indices

이제 model 파일로부터 vertex와 index를 로드할 것이므로, 기존에 전역으로 선언했던 vertices와 indices 배열은 삭제합시다.

대신const가 아닌 container로 대체하고,  클래스 멤버로 정의합시다.

```
std::vector<Vertex> vertices;
std::vector<uint32_t> indices;
VkBuffer vertexBuffer;
VkDeviceMemory vertexBufferMemory;
```

index의 타입은 uint16\_t가 아닌 uint32\_t로 변경해야 합니다. vertex 수가 65,535개를 초과할 수 있습니다.

또한, vkCmdBindIndexBuffer 함수 호출 시 인자도 다음과 같이 변경해야 합니다:

```
vkCmdBindIndexBuffer(commandBuffer, indexBuffer, 0, VK_INDEX_TYPE_UINT32);
```

tiny obj loader 라이브러리는 stb\_image와 같은 방식으로 포함합니다. 헤더 파일 tiny\_obj\_loader.h를 include한 뒤, 함수 정의를 포함시키기 위해 **하나의 소스 파일에서** TINYOBJLOADER\_IMPLEMENTATION을 정의해야 합니다. 그래야 링크 에러가 발생하지 않습니다:

```
#define TINYOBJLOADER_IMPLEMENTATION
#include <tiny_obj_loader.h>
```

이제 우리는 이 라이브러리를 활용하여 vertices와 indices 컨테이너에 데이터를 채워 넣는 loadModel() 함수를 작성할 것입니다. 이 함수는 vertex 및 index buffer를 생성하기 **이전** 단계에서 호출되어야 합니다

```
void initVulkan() {
    ...
    loadModel();
    createVertexBuffer();
    createIndexBuffer();
    ...
}
```

loadModel() 함수는 다음처럼 작성됩니다:

```
void loadModel() {
    tinyobj::attrib_t attrib;
    std::vector<tinyobj::shape_t> shapes;
    std::vector<tinyobj::material_t> materials;
    std::string warn, err;

    if (!tinyobj::LoadObj(&attrib, &shapes, &materials, &warn, &err, MODEL_PATH.c_str())) {
        throw std::runtime_error(warn + err);
    }
}
```

Obj 파일은 위치(position), 노멀(normal), 텍스처 좌표(texture coordinates), 그리고 face로 구성됩니다. 각 face는 여러 vertex로 구성되며, 각 vertex는 position, normal, texcoord에 대한 인덱스를 가집니다.

OBJ 모델은 face마다 다른 material이나 texture를 지정할 수도 있지만, 우리는 이 부분은 무시합니다.

우리는 모든 shape의 face를 단일 모델로 병합할 것이므로, shapes 전체를 순회하며 처리합니다:

```
for (const auto& shape : shapes) {
    for (const auto& index : shape.mesh.indices) {
        Vertex vertex{};

        vertex.pos = {
            attrib.vertices[3 * index.vertex_index + 0],
            attrib.vertices[3 * index.vertex_index + 1],
            attrib.vertices[3 * index.vertex_index + 2]
        };

        vertex.texCoord = {
            attrib.texcoords[2 * index.texcoord_index + 0],
            attrib.texcoords[2 * index.texcoord_index + 1]
        };

        vertex.color = {1.0f, 1.0f, 1.0f}; // 일단 하얀색 고정

        vertices.push_back(vertex);
        indices.push_back(static_cast<uint32_t>(indices.size()));
    }
}
```

지금은 간단히 처리하기 위해 "모든 vertex가 유일하다(unique)"고 가정하고 index를 단순히 auto-increment 방식으로 추가합니다.  
tinyobj::index\_t 타입은 3가지 종류가 있습니다.

* vertex\_index
* normal\_index
* texcoord\_index

우리는 이 인덱스를 이용해 attrib 배열에서 실제 값을 참조합니다.

attrib.vertices는 float 값의 배열로 구성되어 있기 때문에 glm::vec3가 아닌 단순 배열로 접근해야 하며, 따라서 인덱스를 3배 해줘야 합니다. 마찬가지로 texture coordinates는 U, V 두 개의 요소만 있으므로 인덱스는 2배 해야 합니다.

근데 이렇게하고 실행시키면 검정화면만 나옵니다.

그 이유로 가설을 몇개 세울 수 있는데,

1. load가 잘 못되고 있다.

2. 물체가 너무 커서, 내가 물체안으로 들어와져있고 backface culling 때문에 아무것도 안보인다.

3. 물체가 너무 커서 내 viewport 밖으로 나갔다.

1번 -> breakpoint로 vertex 수를 확인했는데 19만개정도 있음, 잘 들어오는 것 같으니 패스

2번 -> backface culling 껐는데 안보임 패스

3번 -> 물체의 크기를 normalize해봄

우리가 verteies, indices를 불러오는 것까지는 잘 했다.

불러온 것을 바탕으로 x,y,z축의 max, min 값을 알아내고, 그것을 사용해서

크기, 위치를 정규화 해주자 ( 이건 문서에 없는 내용..이예요 하핳)

```
void loadModel()
{
	tinyobj::attrib_t attrib;
	std::vector<tinyobj::shape_t> shapes;
	std::vector<tinyobj::material_t> materials;
	std::string warn, err;
	 
	if (!tinyobj::LoadObj(&attrib, &shapes, &materials, &warn, &err, MODEL_PATH.c_str()))
	{
		throw std::runtime_error(warn + err);
	}

	// pos 범위 계산
	float maxX = FLT_MIN, minX = FLT_MAX, maxY = FLT_MIN, minY = FLT_MAX, maxZ = FLT_MIN, minZ = FLT_MAX;

	for (const auto& shape : shapes)
	{
		for (const auto& index : shape.mesh.indices)
		{
			float x = attrib.vertices[3 * index.vertex_index + 0];
			float y = attrib.vertices[3 * index.vertex_index + 1];
			float z = attrib.vertices[3 * index.vertex_index + 2];
			
			maxX = x > maxX ? x : maxX;
			minX = x < minX ? x : minX;

			maxY = y > maxY ? y : maxY;
			minY = y < minY ? y : minY;
			
			maxZ = z > maxZ ? z : maxZ;
			minZ = z < minZ ? z : minZ;
		}
	}

	float extentX = (maxX - minX);
	float extentY = (maxY - minY);
	float extentZ = (maxZ - minZ);

	for (const auto& shape : shapes)
	{
		for (const auto& index : shape.mesh.indices)
		{
			Vertex vertex{};

			vertex.pos = 
			{ 
				attrib.vertices[3 * index.vertex_index + 0],
				attrib.vertices[3 * index.vertex_index + 1],
				attrib.vertices[3 * index.vertex_index + 2]
			};
			
			vertex.texCoord =
			{
				attrib.texcoords[2 * index.texcoord_index + 0],
				1.0f - attrib.texcoords[2 * index.texcoord_index + 1]
			};

			vertex.color = { 1.0f, 1.0f, 1.0f };

			vertices.push_back(vertex);
			indices.push_back(indices.size());
		}
	}

	float resize = 2.0f / (std::max({ extentX, extentY, extentZ, 0.001f }));

	float centerX = (maxX + minX) * 0.5f, centerY = (maxY + minY) * 0.5f, centerZ = (maxZ+ minZ) * 0.5f;

	// resacaling, repositioning
	for (auto& vertex: vertices)
	{
		vertex.pos.x = ( vertex.pos.x - centerX ) * resize;
		vertex.pos.y = ( vertex.pos.y - centerY ) * resize;
		vertex.pos.z = ( vertex.pos.z - centerZ ) * resize;
	}
	// normal vector	정규화 
}
```

따단 잘됨 나이스!!

![](https://blog.kakaocdn.net/dna/bIaCA6/btsNVBd8eZ9/AAAAAAAAAAAAAAAAAAAAAE-_nkufWtqGjZVi5vgeG3FZs-20ChyAPmZAT6sO2Vhd/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=OEEJDHu492QBmmLuqJcrRR%2FMrBU%3D)

근데 texture가 이상하게 mapping되어있다.

OBJ 포맷에서는 v = 0이 이미지의 **하단(bottom)** 을 의미

Vulkan에서는 v = 0이 이미지의 **상단(top)** 을 의미

이 불일치를 해결하려면, **텍스처 좌표의 Y축(v)** 값을 뒤집어야 합니다:

```
vertex.texCoord = {
    attrib.texcoords[2 * index.texcoord_index + 0],
    1.0f - attrib.texcoords[2 * index.texcoord_index + 1]
};
```

texture 좌표만 뒤집어 주면 잘 작동이된다.

![](https://blog.kakaocdn.net/dna/bZCjEC/btsNVKa3ywY/AAAAAAAAAAAAAAAAAAAAACFFqlFa4rMD3MNlboe95vzSHmMTPyeHn0S_Z4Cmt3uV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FI31%2BeRY1uvHm7OJRAStMFVca40%3D)

### Vertex Deduplication

현재 우리가 작성한 코드는 Index Buffer를 제대로 활용을 못하고 있습니다.

(삼각형 1개당 서로 다른 vertex 3개를 정식하게 쓰고있다.)

우리는 **중복되지 않은(unique) 정점만 저장**하고,

중복되는 vertex는 index를 활용해서 재사용해야됩니다.

이를 구현하는 가장 간단한 방법은 map이나 unordered\_map을 사용해서,  
이미 저장된 정점인지 여부와 해당 정점의 인덱스를 저장하는 것입니다.

```
#include <unordered_map>

...

std::unordered_map<Vertex, uint32_t> uniqueVertices{};

for (const auto& shape : shapes) {
    for (const auto& index : shape.mesh.indices) {
        Vertex vertex{};

        ...

        if (uniqueVertices.count(vertex) == 0) {
            uniqueVertices[vertex] = static_cast<uint32_t>(vertices.size());
            vertices.push_back(vertex);
        }

        indices.push_back(uniqueVertices[vertex]);
    }
}
```

이 코드는 .obj 파일에서 하나의 정점을 읽을 때마다,  
**같은 위치(pos), 색(color), 텍스처 좌표(texCoord)를 가진 정점이 이미 존재하는지 검사하고,**  
**존재하지 않으면 vertices에 추가하고 그 인덱스를 저장합니다.**

이미 존재하는 정점이라면 저장하지 않고, 해당 인덱스를 재사용할 것입니다.

하지만 이 코드는 아직 컴파일되지 않습니다.....

Vertex는 사용자 정의 타입이기 때문에, unordered\_map의 키로 사용하려면 **두 가지 조건**을 만족시켜야 합니다.

1. 동등성 비교 연산자 (==) 정의
2. 해시 함수 (std::hash) 정의

#### 1. 동등성 비교 연산자

다음과 같이 Vertex 구조체 내에 == 연산자를 오버라이딩해야 됩니다.

```
bool operator==(const Vertex& other) const {
    return pos == other.pos && color == other.color && texCoord == other.texCoord;
}
```

#### 2. Hash 함수 정의

Vertex의 해시 함수는 std::hash<Vertex>의 **템플릿 특수화**로 구현합니다.

```
namespace std {
    template<> struct hash<Vertex> {
        size_t operator()(const Vertex& vertex) const {
            return ((hash<glm::vec3>()(vertex.pos) ^
                    (hash<glm::vec3>()(vertex.color) << 1)) >> 1) ^
                    (hash<glm::vec2>()(vertex.texCoord) << 1);
        }
    };
}
```

위 코드는 Vertex의 세 필드를 각각 해시한 다음, **비트 연산을 통해 결합**하는 방식이다.  
이렇게 하면 충돌 가능성이 낮고 품질도 높은 해시가 만들어집니다.

(이 코드는 Vertex 구조체 외부에 작성해야 합니다.)

glm::vec3, vec2 등에 대한 해시 함수를 사용하려면 다음을 포함해야 됩니다.

```
#define GLM_ENABLE_EXPERIMENTAL
#include <glm/gtx/hash.hpp>
```

이 해시 구현은 GLM의 **실험적 기능(gtx)** 이므로 GLM\_ENABLE\_EXPERIMENTAL을 정의해야만 사용할 수 있습니다.  
이 기능은 실험적이긴 하지만 **실제 GLM에서는 매우 안정적으로 유지되고** 있습니다.

코드를 성공적으로 컴파일하고 실행하면,

19만개의 vertex에서 4만개로 줄었습니다!! 야호잇