---
title: "[Vulkan] VK_ERROR_EXTENSION_NOT_PRESENT 에러"
date: 2025-05-16
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

튜토리얼 문서를 다 보고, 파일을 분할하고 있는데 instance를 분할하니까 이런 오류가 나타났다.

코드를 수정하지는 않았기 때문에 헤딩을 꽤 했다.

![](https://blog.kakaocdn.net/dna/bKhpoc/btsNYhNJJoj/AAAAAAAAAAAAAAAAAAAAAHdHU9AH0lSIfbd9A2owaQ2qqqKbF2jykWngDOVYvSRD/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=6fxM7A7oPnK2dr4RU3fUODDhlq8%3D)

정답은 아래의 코드가 문제였다.

```
std::vector<const char*> Instance::getRequiredExtensions()
{								   
	uint32_t glfwExtensionCount = 0;
	const char** glfwExtensions;
	glfwExtensions = glfwGetRequiredInstanceExtensions(&glfwExtensionCount);

	std::vector<const char*> extensions(glfwExtensions, glfwExtensions + glfwExtensionCount);

	if (enableValidationLayers)
	{
		extensions.push_back(VK_EXT_DEBUG_UTILS_EXTENSION_NAME);
	}

	return extensions;
}
```

glfw가 초기화 되지 않은 상태에서 glfwExtention을 가져왔기 때문에 여기서 window surface present Extension이 포함이 안되어버린 것이다.

이제 main에서 glfw를 초기화하고, vulkan을 초기화하도록 수정하니까 문제가 해결됐다.

```
int main()
{
	if (!glfwInit())
	{
		std::cerr << "Failed to initialized GLFW\n";
		return EXIT_FAILURE;
	}
	glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
 	//InitVulkan
 }
```