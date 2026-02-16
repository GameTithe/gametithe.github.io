---
title: "[CG] Deferred Shading"
date: 2025-01-31
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **Deferred Shading 이란**

복잡한 조명효과에 대한 계산 부하를 줄이기 위해서 등장한 방법이다. 화면에 그려질 물체를 조명 효과 없이 그리고 그 뒤에 조명 효과를 적용하는 것이다.

이렇게 하면 화면에 나타나지 않는 픽셀, vertex에 대해서 조명효과를 계산하지 않아도 되기에 성능이 좋아진다.

1. G- buffer를 생성하면서, 물체를 그려준다.

2. 생성한 G-buffer를 이용해서 light 효과를 적용시켜준다.

3. cubeMap을 사용중이라면 cubeMap에 depthBuffer를 넘겨줘서 depth가 1인 부분에만 그려준다.

### **1. G- buffer를 생성하면서, 물체를 그려준다.**

아래와 같이 처음 초기화를 할 때 G-buffer를 초기화 해준다.

G-buffer란 geometry buffer로 position, normal, depth 등등을 저장해 놓는 것을 의미합니담

position과 normal은 자세한 정보가 필요하기 때문에 GL\_RGB32F를 사용했습니다.

```
	//Gen Position Buffer
	glActiveTexture(GL_TEXTURE0); 
	glGenTextures(1, &posTex); 
	glBindTexture(GL_TEXTURE_2D, posTex);

	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, width, height, 0,
		GL_RGB, GL_FLOAT, NULL);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
		GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
		GL_NEAREST);

	//Gen Normal Buffer 
	glActiveTexture(GL_TEXTURE1); // Use texture unit 1 for normal  
	glGenTextures(1, &normTex);
	glBindTexture(GL_TEXTURE_2D, normTex);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, width, height, 0,
		GL_RGB, GL_FLOAT, NULL);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
		GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
		GL_NEAREST);

	//Gen Diffuse Buffer
	glActiveTexture(GL_TEXTURE2); // Texture unit 2 for diffuse color
	glGenTextures(1, &colorTex);
	glBindTexture(GL_TEXTURE_2D, colorTex);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0,
		GL_RGB, GL_UNSIGNED_BYTE, NULL);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
		GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
		GL_NEAREST);

	//Gen Depth buffer 
	glActiveTexture(GL_TEXTURE3);
	glGenTextures(1, &depthTex);
	glBindTexture(GL_TEXTURE_2D, depthTex);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT24, width, height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, NULL);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
```

만들어준 texture를 shader에서 채워준다고 설정한다.

0번은 fragColor로 사용했고, G-buffer를 만들 때 사용하지 않을 것이기 때문에 GL\_NONE으로 채웠고,  
1,2,3 번 인덱스는 각각 GL\_COLOR\_ATTACHMENT로  채웠습니다.

```
glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1,
    GL_TEXTURE_2D, posTex, 0);

glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT2,
    GL_TEXTURE_2D, normTex, 0);

glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT3,
    GL_TEXTURE_2D, colorTex, 0);

drawBuffers = {
drawBuffers[0] = GL_NONE,
drawBuffers[1] = GL_COLOR_ATTACHMENT1,
drawBuffers[2] = GL_COLOR_ATTACHMENT2,
drawBuffers[3] = GL_COLOR_ATTACHMENT3,
        
glDrawBuffers(drawBuffers.size(), drawBuffers.data());
```

그러면 이렇게 G-buffer를 얻을 수 있다.

![](https://blog.kakaocdn.net/dna/cNIcu5/btsL4o7HwMY/AAAAAAAAAAAAAAAAAAAAALHNvn43y_2MWuTDD3EUL7HVx3O9mVQlOC2JFEuZbHlG/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xQJqLrzPvrk7ZOqqethygkgK%2FC8%3D)![](https://blog.kakaocdn.net/dna/3jPTd/btsL4pyJ9AN/AAAAAAAAAAAAAAAAAAAAAHad-_iMNL2sRJg8oHI0ZKDg8jm1cu9gjrgcyGz-Jq2L/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=aRXyzDGbhXVh7ytKXC%2B2aMA0wJk%3D)

몇가지 실수? 문제? 가 있었는데

첫 번째 이미지:

아래의 스크릿 샷 처럼, 조명 효과를 계산하지 않은 정보가 output 에 잘 저장되고

두 번째 이미지:

다음 draw call의 input으로도 잘 들어가는 것을 확인했다.

![](https://blog.kakaocdn.net/dna/wtDkf/btsL3lW9E7n/AAAAAAAAAAAAAAAAAAAAAJQWamXMzX0i8cdBpWzZlru41-uUs6d9Njed5_l9wfpL/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=QyiY2r7USKmnD8cFxjaadjN3SMs%3D)![](https://blog.kakaocdn.net/dna/9MZ9c/btsL1hPoBJh/AAAAAAAAAAAAAAAAAAAAAN1c-Ur7pfL9CNEa1er4Wy6MJp9Bocxa11Z_HMt9MW-M/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Pb%2F4UVJFGSCzQdn8LLBUy9mjIoA%3D)

하지만 output으로는 이상한 그림이 그려졌다

![](https://blog.kakaocdn.net/dna/5zSAg/btsL3lixXxe/AAAAAAAAAAAAAAAAAAAAAKR3lK3R87BxcTQtHyoMWkCOGKci2tJk5N_05hAMcTQc/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=r4g8qRg1%2BCdAcFmOjKLYrSkesgc%3D)

~~몇시간 고생을 했는데 문제는 deferred shading을 위한 초기화 함수를 따로 만들어주었는데,~~

~~그 함수를 첫 frame buffer에만 적용시키고 두 번째 framebuffer에는 다른 함수로 초기화한게 문제였다.~~

~~그래서 옳바른 정보를 받아오지 못한것이었다.~~ + 나중에 알게된 것인데 position을 잘 못주고 있었다...

```
void Framebuffer::Draw_Deferred(unsigned int ShaderID) 
{
	// 위치 텍스처 (posTex) -> Texture unit 0
	glBindVertexArray(rectVAO);
	glDisable(GL_DEPTH_TEST);

	glActiveTexture(GL_TEXTURE0);
	glBindTexture(GL_TEXTURE_2D, posTex); // 미리 저장해둔 posTex
	glUniform1i(glGetUniformLocation(ShaderID, "PositionTex"), 0);

	// 노멀 텍스처
	glActiveTexture(GL_TEXTURE1);
	glBindTexture(GL_TEXTURE_2D, normTex); // 미리 저장해둔 normTex
	glUniform1i(glGetUniformLocation(ShaderID, "NormalTex"), 1);

	// 디퓨즈(Albedo) 텍스처
	glActiveTexture(GL_TEXTURE2);
	glBindTexture(GL_TEXTURE_2D, colorTex); // 미리 저장해둔 colorTex
	glUniform1i(glGetUniformLocation(ShaderID, "ColorTex"), 2);


	glDrawArrays(GL_TRIANGLES, 0, 6);

}
```

위의 문제를 해결하면

![](https://blog.kakaocdn.net/dna/btjQB0/btsL1gjf3HB/AAAAAAAAAAAAAAAAAAAAAG3w13AA9WYmKRDkeHCFw7Vhde3t6M-Sgn7SD3e0Hqfr/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wc4seCZqHLasQCwVUHNgUmekmFo%3D)

근데 화면을 움질일 때마다, 색이 변했다.

Position을 저장할 때 screen 좌표계로 저장을 해서 그렇다. 월드 좌표계로 저장해주면 아래와 같이 고정된 값을 얻을 수 있다. (사진이여서 크게 바뀐 느낌은 안들지만 카메라 위치를 변경해도 동일한 색이다.)   
남은 문제점은 skybox를 어떻게 적용시키냐는 것이다...  
skybox에는 deferred shading이 적용되면 안된다.

처음 물체들을 그리고 그 이후에는 2D이미지로 들고 다니고 있는데 ( framebuffer)  skybox만 shading을 적용을 회피할 방법을 찾아야한다.

![](https://blog.kakaocdn.net/dna/baiC8P/btsL2Pq98Nj/AAAAAAAAAAAAAAAAAAAAAF-ebH2tuofkpHiB0cOSHpaxxLXhxHFed0uOncbT3tRX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=PSgtOwUsWDyBQp7EVFR7jzFBxcQ%3D)

### 

### **2. 생성한 G-buffer를 이용해서 light 효과를 적용시켜준다.**

input으로 색, 위치, normal을 넘겨줘서 이전에 만들어둔 조명효과를 입혀주면 된다.

![](https://blog.kakaocdn.net/dna/bG6wXZ/btsL2Q49X7d/AAAAAAAAAAAAAAAAAAAAAJ7mqIeQfLoTOG1cFZoWZDvGV8gzE13mw8AHMFkIzZB5/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=L9hFuUe%2FDdJUCtZvQQuCn6Z4f5w%3D)![](https://blog.kakaocdn.net/dna/b8f8J3/btsL2zbciGl/AAAAAAAAAAAAAAAAAAAAAJ30-o3yrJUUYFcexDNfJPuJp6c8XIySj9_wl3iiODiK/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=WJAjRO0FgRnNSm%2FLT%2Bb%2BwmID2tY%3D)

depth buffer를 skybox에게 넘겨줘서 skybox에서 depth buffer가 1일 때만 skybox를 그리도록 해주었다!

### 

### **3. cubeMap을 사용중이라면 cubeMap에 depthBuffer를 넘겨줘서 depth가 1인 부분에만 그려준다.**

제목이 곧 설명이다.

이렇게 depth를 넘겨주었고, shader에서 비교했다.

원래는 renderBuffer를 사용해서 depthBuffer를 관리했지만, shader에서는 renderBuffer를 접근하지 못하기 떄문에 texture로 바꿔준 비하인드 스토리가 있다 :)

![](https://blog.kakaocdn.net/dna/UnnJq/btsL4cM33Yg/AAAAAAAAAAAAAAAAAAAAAJO-OXm0x5jX3Uk3v4zi6-Z3JruE5rgU9hFPPdMMvLHp/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GbQMIQwfuPp8E0p5rUpGZD5F4Kk%3D)![](https://blog.kakaocdn.net/dna/TylCA/btsL3spldZD/AAAAAAAAAAAAAAAAAAAAAFAdmDf_edGQ-d6xJb3DgDZX8-xQWk6w8FS75-twJwaj/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=n%2BVLeg0gRrsE2G0uou6zgZBbX6A%3D)

후... 드디어...

여기까지 하면 deferred shading은 끝이다.   
저는 deferredShading을 적용하기전에 만들어놓았던 bloom effect를 적용시켜보겠습니다.

few hours later....

완성 :)

![](https://blog.kakaocdn.net/dna/nxl9W/btsL4Mm0Bhu/AAAAAAAAAAAAAAAAAAAAAJaURGvfSdMWHMLZYMk6OF2mHTGxWm6bblj-KTCytVpH/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Br1iChcenly5yoKGcBOk1o2nhb4%3D)

마지막으로 Deferred Shading에 대한 여러견해가 있습니다.

Deferred Shading을 할 경우 하드웨어적으로 anti-aliasing을 제공해주지 못하기 때문에 second pass를 본인이 만들어서 구현해야 됩니다. 여기서도 문제가 생기는데

second pass에서도 필셀 1개당 1개의 sampler만 소지하고 있는 상태이기에

유저가 한 픽셀에 대해 다른 샘플링을 한 texture들을 만들고, 거기서 선택해서 사용해야한다고 합니다.

이러한 방법이 어려우니 야매로(?) edge detection filter를 사용해서 edge를 blur처리하는 방법도 있다고 알려줍니다.

장점으로는 조명계산에 이득을 볼 수 있다는 점도 있고,

blending/transparency한 object rendering에 있다고 합니다. depth-peeling을 추가로 g-buffer에 저장해서 사용하면 용이하다고 합니다.

Chapter 9 in GPU Gems 2 edited by Matt Pharr and Randima Fernando (Addison-Wesley Professional 2005) and Chapter 19 of GPU Gems 3 edited by Hubert Nguyen (Addison-Wesley Professional 2007). 여기에 더 자세한 이야기가 있다고합니다.

보고있는 책 다보면 GPU Gems로 넘어가봐야겠습니당