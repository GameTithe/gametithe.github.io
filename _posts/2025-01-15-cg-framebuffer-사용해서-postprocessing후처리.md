---
title: "[CG] FrameBuffer 사용해서 postProcessing(후처리)"
date: 2025-01-15
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

결과물:

<https://tithingbygame.tistory.com/141>

[[실습저장소] FrameBuffer 사용해서 postProcessing(후처리)

이론:https://tithingbygame.tistory.com/142 [CG] FrameBuffer 사용해서 postProcessing(후처리)Framgbuffer를 적용한 간략한 순서1. 후처리 FrameBuffer를 만든다.2. 후처리 FrameBuffer에 물체들을 그려준다. (texture에 따로

tithingbygame.tistory.com](https://tithingbygame.tistory.com/141)

### 

### Framgbuffer를 적용한 간략한 순서

1. 후처리 FrameBuffer를 만든다.

2. 후처리 FrameBuffer에 물체들을 그려준다. (texture에 따로 저장)

3. 기존 FrameBuffer에 사각형에 후처리 FrameBuffer에 저장된 texture를 입힌다.

4. 해당 texture를 shader에서 kernel을 이용해서 색 조정을 한다.

5. 완성된 rendering을 보고 만족해한다.

(framebuffer.cpp파일은 하단에 첨부했습니다)

#### **1. 후처리 FrameBuffer를 만든다.**

대단한 건 없다.

1. 물체들이 rendering 된 것을 저장할 사각형 하나를 만든다.

2. FrameBuffer를 만들고, bind 해준다.

```
// Prepare framebuffer rectangle VBO and VAO
Framebuffer frameBuffer; 
frameBuffer.Init(screenWidth, screenHeight);
   
//framebuffer 생성
frameBuffer.GenFrameBuffer();
```

#### **2. 후처리 FrameBuffer에 물체들을 그려준다. (texture에 따로 저장)**

물체를 frameBuffer에 그려줘야되는데, 그릴 곳이 필요할 것이다.

그래서 texture를 만들어준다.

depth Stencil을 책임지는 RenderBuffer도 같이 만들어 준다. (renderBuffer는 shader에서 접근 불가) 

```
frameBuffer.BindTextureBuffer();
frameBuffer.BindRenderBuffer();
```

기본 세팅을 했으면 FrameBuffer를 바꿔서

후처리 frameBuffer에 물체를 그려준다.

```
glBindFramebuffer(GL_FRAMEBUFFER, frameBuffer.FBO);
glClearColor(baseColor.x, baseColor.y, baseColor.z, baseColor.w); 
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);
glEnable(GL_DEPTH_TEST);


// 물체 그리기
```

#### 

#### **3. 기존 FrameBuffer에 사각형에  후처리 FrameBuffer에 저장된 texture를 입힌다.**

```
// Bind the default framebuffer
glBindFramebuffer(GL_FRAMEBUFFER, 0);

// Draw the framebuffer rectangle
framebufferShader.Activate(); 
frameBuffer.Draw();
```

#### **4. 해당 texture를 shader에서 kernel을 이용해서 색 조정을 한다**.

이건 shader에서 원하는 대로 바꿔보자

```
#version 330 core

out vec4 FragColor;
in vec2 texCoords;

uniform sampler2D screenTexture;
uniform float width;
uniform float height;

vec2 offset[9] = vec2[9](
    vec2(-1.0 / width,  1.0 / height), vec2(0.0,  1.0 / height), vec2( 1.0 / width,  1.0 / height),
    vec2(-1.0 / width,  0.0),          vec2(0.0,  0.0),          vec2( 1.0 / width,  0.0),
    vec2(-1.0 / width, -1.0 / height), vec2(0.0, -1.0 / height), vec2( 1.0 / width, -1.0 / height)
);

    
float kernel[9] = float[9]
(
    2,2,2,
    2,-20,2,
    2,2,2
);

void main()
{
   //회색
   vec4 color = texture(screenTexture, texCoords);
   float avg = (color.r + color.g + color.b) / 3.0f;
   FragColor = vec4(avg);

   //vec4 color = vec4(0,0,0,0);
   //for(int i = 0; i < 9;i ++)
   //{ 
   //      color += texture(screenTexture, vec2(texCoords + offset[i])) * kernel[i];
   //}

   //FragColor = color;
}
```

#### **5. 완성된 rendering을 보고 만족해한다.**

![](https://blog.kakaocdn.net/dna/b5A4Iq/btsLPlDgxwr/AAAAAAAAAAAAAAAAAAAAAGtqyhgtGQ-IcPRqzpYZsvZv-XjDz0M1AO34avW27tMd/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Kwdi0qQcC8PaX8vfaemSDgZAlik%3D)
![](https://blog.kakaocdn.net/dna/bPv7Bs/btsLOLCtSLu/AAAAAAAAAAAAAAAAAAAAAK7eV_tKMFDQiMnBoHktMRqJJfXowiUeknTpJ-tuyRQn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=4NacHFnyxLGcpJPxvBaKlO91zSk%3D)

Framebuffer.cpp

```
#include "Framebuffer.h"
#include "OpenGL.h"

Framebuffer::Framebuffer(int screenWidth, int screenHeight)
{	 
	if (bInit) return;
	Init(screenWidth, screenHeight);
}

void Framebuffer::Init(int screenWidth, int screenHeight)
{
	if (bInit) return;
		
	width = screenWidth;
	height = screenHeight;

	float rectangleVertices[] =
	{
		// Coords    // texCoords
		 1.0f, -1.0f,  1.0f, 0.0f,
		-1.0f,  1.0f,  0.0f, 1.0f,
		-1.0f, -1.0f,  0.0f, 0.0f,

		 1.0f,  1.0f,  1.0f, 1.0f,
		-1.0f,  1.0f,  0.0f, 1.0f,
		 1.0f, -1.0f,  1.0f, 0.0f
	};

	// Prepare framebuffer rectangle VBO and VAO
	unsigned int rectVBO;
	glGenVertexArrays(1, &rectVAO);
	glGenBuffers(1, &rectVBO);
	glBindVertexArray(rectVAO);
	glBindBuffer(GL_ARRAY_BUFFER, rectVBO);
	glBufferData(GL_ARRAY_BUFFER, sizeof(rectangleVertices), &rectangleVertices, GL_STATIC_DRAW);
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(1);
	glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(float), (void*)(2 * sizeof(float)));

}

void Framebuffer::BindRenderBuffer()
{
	unsigned int RBO;
	glGenRenderbuffers(1, &RBO);
	glBindRenderbuffer(GL_RENDERBUFFER, RBO);
	glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, width, height);
	glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, RBO);

	auto fboStatus = glCheckFramebufferStatus(GL_FRAMEBUFFER);
	if (fboStatus != GL_FRAMEBUFFER_COMPLETE)
		std::cout << "Framebuffer error: " << fboStatus << std::endl;

}

void Framebuffer::Draw()
{
	glActiveTexture(GL_TEXTURE0);
	glBindVertexArray(rectVAO);
	glDisable(GL_DEPTH_TEST); // prevents framebuffer rectangle from being discarded
	glBindTexture(GL_TEXTURE_2D, framebufferTexture);
	glDrawArrays(GL_TRIANGLES, 0, 6);
}

void Framebuffer::GenFrameBuffer()
{ 
	glGenFramebuffers(1, &FBO);
	glBindFramebuffer(GL_FRAMEBUFFER, FBO);
}

void Framebuffer::BindTextureBuffer()
{
	glGenTextures(1, &framebufferTexture);
	glBindTexture(GL_TEXTURE_2D, framebufferTexture);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, NULL);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE); // Prevents edge bleeding
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE); // Prevents edge bleeding

	glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, framebufferTexture, 0);

	auto fboStatus = glCheckFramebufferStatus(GL_FRAMEBUFFER);
	if (fboStatus != GL_FRAMEBUFFER_COMPLETE)
		std::cout << "Framebuffer error: " << fboStatus << std::endl;

}
```