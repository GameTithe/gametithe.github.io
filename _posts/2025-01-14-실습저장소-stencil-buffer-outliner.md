---
title: "[실습저장소] Stencil Buffer (outliner)"
date: 2025-01-14
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

![](https://blog.kakaocdn.net/dna/cG2KwX/btsLMpgm0ck/AAAAAAAAAAAAAAAAAAAAACox37yXH4UiKGf6L3FGWwblVhxsE96DJPUt59AUInrp/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=46keMBQP26x%2Fp78atLC3icQ9Td8%3D)

StencilBuffer를 통해서 추가적은 효과를 얻었다.  
  
glStencilMask(0x00); // 쓰기를 막아준다.

glStencilMask(0xff);    // 쓰기를 가능하게 해준다.

아래가 핵심 코드인데

glStencilFunc(GL\_ALWAYS,1,0xff)   => 무조건 통과 + 물체 render + 그 위치에 stencil을 1로 교체

glStencilMask(0xff)  => stencil buffer 쓰기 가능

// 원 그리기

glStencilFunc(GL\_NOTEQUAL, 1,0xff)   => Stencil이 1이 아닐 때 통과 => 그렇기 때문에 물체부분은 흰색으로 칠해지지 않는 것

glStencilMask(0xff)  => stencil buffer 쓰기 불가능 ( 아웃라이너 그리면서 stencil이 1로 변하는 것을 방지)

// 아웃라이너 그리기

glStencilFunc(GL\_ALWAYS, 0 ,0xff)   => 무조건 통과 + 물체 render + 그 위치에 stencil을 0로 교체

glStencilMask(0xff)  => stencil buffer 쓰기 가능

```
glStencilFunc(GL_ALWAYS, 1, 0xff);
glStencilMask(0xff);

//spere
for (int i = 0; i < 4; i++)
{
	sphere.Translate(shaderProgram, floorBasePos, vec3(0, 0.2, 0.4 + i * -0.4));
	sphere.Draw(shaderProgram, camera);
}
 
glStencilFunc(GL_NOTEQUAL, 1, 0xff);
glStencilMask(0x00); 

outliningShader.Activate();
glUniform1f(glGetUniformLocation(outliningShader.ID, "outlining"), 0.03f);

for (int i = 0; i < 4; i++)
{
	sphere.Translate(outliningShader, floorBasePos, vec3(0, 0.2, 0.4 + i * -0.4));
	sphere.Draw(outliningShader, camera);
}

glStencilFunc(GL_ALWAYS, 0, 0xff);
glStencilMask(0xff);
```