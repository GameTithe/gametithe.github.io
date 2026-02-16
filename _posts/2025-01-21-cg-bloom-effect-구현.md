---
title: "[CG] Bloom Effect 구현"
date: 2025-01-21
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

<https://tithingbygame.tistory.com/manage/newpost/148?type=post&returnURL=https%3A%2F%2Ftithingbygame.tistory.com%2Fmanage%2Fposts%2F>

[티스토리

좀 아는 블로거들의 유용한 이야기, 티스토리. 블로그, 포트폴리오, 웹사이트까지 티스토리에서 나를 표현해 보세요.

www.tistory.com](https://tithingbygame.tistory.com/manage/newpost/148?type=post&returnURL=https%3A%2F%2Ftithingbygame.tistory.com%2Fmanage%2Fposts%2F)

단계별로 먼저 설명을하면,

1. Gaussian Blur

2. treshold를 통해 밝은 부분 검수(?)

3. 검수하 부분을 원본에 입히기

4. Bloom effect 감상하기

Bloom효과를 입히면서 몇가지 애먹은 부분이 있었다.

1. 내가 지금 write하고 있는 framebuffer는 read를 할 수 없다는 것이다.

2. glActiveTexture.... 를 안하고 Draw.. 해서 read하고 싶은 framebuffer texture를 못가져왔다.

이런 부분들만 신경써서 만들면 쉽게할 수 있을 것이다.

우선 gaussian blur를 처리할 때 gaussian fitler를 바로 적용하면 n개의 크기의 filter면 pixel 수 \* n\*n 만큼 반복해야됩니다.

하지만 가로 세로를 나눠서 처리하게 되면 pixel 수 \* n \* 2(가로 1번, 세로 1번) 으로 반복 횟수가 많이 줄게 됩니다.

그래서 저는 OpenGL의 subroutine를 사용해서 가로 세로를 따로 처리해주었습니다.

주석되어있는  sum =vec4(1,0,0,1)은 framebuffer가 잘 쓰고 있나 테스트하려고, 색을 입혀서 체크해봤습니다

```
subroutine(RenderPassType)
vec4 Horizontal()
{   
    //vec4 bloomColor = textureLod(screenTexture, texCoords, 3);
    float dx = 1.0 / float(width);  // x 방향으로 변경
    vec4 sum = texture(screenTexture, texCoords) * weight[0];
    for (int i = 1; i < 17; i++) // 17개의 샘플링
    {
        sum += texture(screenTexture, texCoords + vec2(pixelOffset[i] * dx, 0)) * weight[i];
        sum += texture(screenTexture, texCoords - vec2(pixelOffset[i] * dx, 0)) * weight[i];
    }
    //sum = vec4(1,0,0,1);
    return sum;
}

subroutine(RenderPassType)
vec4 Vertical()
{
    float dy = 1.0 / float(height);  // y 방향으로 변경
    vec4 sum = texture(screenTexture, texCoords) * weight[0];
    for (int i = 1; i < 17; i++) // 17개의 샘플링
    {
        sum += texture(screenTexture, texCoords + vec2(0, pixelOffset[i] * dy)) * weight[i];
        sum += texture(screenTexture, texCoords - vec2(0, pixelOffset[i] * dy)) * weight[i];
    }
    //sum = vec4(0,1,0,1);
    return sum;
}
```

while문은 아래와 같습니다.

framebuffer에 원본 저장

gaussianHori, Verti framebuffer를 만들어서 filter적용

default frame buffer에서 framebuffer에 있는 원본 + gaussian frame buffer에 있는 필터적용된 texture => bloom effect

```
while (!glfwWindowShouldClose(window))
{	
	// frameBuffer: 원본 저장
	glBindFramebuffer(GL_FRAMEBUFFER, frameBuffer.FBO); 
	glClearColor(baseColor.x, baseColor.y, baseColor.z, baseColor.w); 
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);
	glEnable(GL_DEPTH_TEST);
     
    //Rendering
    // ...
    // ...

	// gaussian fitler 가로 실행
	glBindFramebuffer(GL_FRAMEBUFFER, gaussianHoriFrameBuffer.FBO);		
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);
	  
	gaussianShader.Activate();
	GLuint horiIndex = glGetSubroutineIndex(gaussianShader.ID, GL_FRAGMENT_SHADER, "Horizontal");
	glUniformSubroutinesuiv(GL_FRAGMENT_SHADER, 1, &horiIndex);
	frameBuffer.Draw();
	
	 
	// gaussian fitler 세로 실행
	glBindFramebuffer(GL_FRAMEBUFFER, gaussianVertiFrameBuffer.FBO);
	gaussianShader.Activate(); 
	GLuint vertiIndex = glGetSubroutineIndex(gaussianShader.ID, GL_FRAGMENT_SHADER, "Vertical");
	glUniformSubroutinesuiv(GL_FRAGMENT_SHADER, 1, &vertiIndex); 
	gaussianHoriFrameBuffer.Draw();  
	  
	glBindFramebuffer(GL_FRAMEBUFFER, 0);  
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);
	 
    //filter 적용 된 texture + framebuffer에 있는 원본 => bloom
	bloomShader.Activate(); 
	const unsigned int texID[1] = { frameBuffer.framebufferTexture };
	const char* texName[1] = { "baseTexture" };
	gaussianVertiFrameBuffer.Draw(bloomShader.ID, texID, texName,1);
}
```

bloom 쉐이더 입니다 .간단합니다.

원본 +  filter적용 된 부분

```
#version 400

in vec2 texCoords;
out vec4 FragColor; 

uniform sampler2D screenTexture;  
uniform sampler2D baseTexture;

uniform float width;
uniform float height;

uniform float bloomStrength;

uniform float threshold;

void main()
{   

    // 텍스처에서 색상 가져오기
     vec4 screenColor = texture(baseTexture, texCoords);   
     vec4 bloomColor = textureLod(screenTexture, texCoords, 5);
  
    // 고휘도 추출: threshold 이상만 유지
    vec3 highPassColor = (any(greaterThan(bloomColor.rgb, vec3(threshold)))) ? bloomColor.rgb : vec3(0.0);

    // Bloom 효과: 고휘도 값에 강도 적용
    vec4 bloom = vec4(highPassColor, 1.0) * bloomStrength;

    // 원본 색상과 Bloom 효과 결합
    FragColor =  screenColor + bloom; 
}
```

![](https://blog.kakaocdn.net/dna/sWZIG/btsLZHsL0ki/AAAAAAAAAAAAAAAAAAAAAAnLTxGRVOKr0cPbAS5Aj27WTGzc05NMXbbhgsyl9U0v/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1RBUmKD5MeLKivz%2B%2FiT8TOAfVuA%3D)

그럼 이렇게 좋은 효과를 얻을 수 있습니다.

근데 조금은 부자연스럽죠??

mipmap으로 우리가 덮어씌우는 이미지를 부드럽게하고, 값을 잘 조정해면 이렇게 자연스럽고 멋지게 이미지를 얻을 수 있습니다.

![](https://blog.kakaocdn.net/dna/H7GLa/btsLZ8KloHo/AAAAAAAAAAAAAAAAAAAAACk6mYT-En0y91FCUyfjwDOxuNrLjPgAQyawNfyBpspK/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=7yuH9ewjL4lK1Hfy6p6TkkHR1cU%3D)