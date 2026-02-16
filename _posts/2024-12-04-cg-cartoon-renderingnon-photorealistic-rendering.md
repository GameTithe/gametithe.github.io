---
title: "[CG] Cartoon Rendering(Non-Photorealistic Rendering)"
date: 2024-12-04
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

**핵심: 명암의 단계가 나뉜다.**

굉장히 쉽게 구현을 할 수 있다. Base는 Phong Shading이고, Fragment Shader를 살짝만 고쳐주면 된다.

아래가 Phong Shading으로 구를 그린 것이다.

![](https://blog.kakaocdn.net/dna/6kvio/btsK5zi4IKG/AAAAAAAAAAAAAAAAAAAAAKsjqTX8F7EQOSpm_nNwQPpuMc65bQedOsr61G9JW2aG/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=j8TQ%2FlKokwpI9BYX1%2FDwIscN5Ak%3D)

이 코드에서 Shader를 살짝만 바꿔보자.

Cartoon Rendering을 보면 명암이 딱딱 끊기는 것을 볼 수 있다.

![](https://blog.kakaocdn.net/dna/mhqyT/btsK45WO5f7/AAAAAAAAAAAAAAAAAAAAAOlO2JAi8NXa-QMDRLGe5mG3rHyTODhaC66uqyvvcmMO/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nrHJwPrLvqTKLjBaf4WNGYQadWQ%3D)

if, else if, ... 로 구역을 나눠서 렌더링을 해보면 

```
	float d = max(dot(N3, L3),0);
	vec4 diff; 

	// 딱딱 나눠지는 명암  
    
    // Diffuse
	// 딱딱 나눠지는 명암  
	if (d > 0.6) diff = vec4(242.0f /255.0f , 22.0f / 255, 22.0f /255.0f, 1);
	else if (d > 0.2) diff = vec4(213 / 255.0f, 12 / 255.0f, 12 / 255.0f, 1);
	else diff = vec4(179 / 255.0f, 11 / 255.0f, 11 / 255.0f, 1);
	
    // Specular
    float s = pow(max(dot(R3, V3),0), sh);
    if(s > 0.2) s = 1;
    else s = 0;
```

이렇게 이쁘장하게, Cartoon같이 rendering이 된다. 살짝 아쉬운 부분은 실루엣 라인이 도드라지면 더 카툰 같을 것 같다.

![](https://blog.kakaocdn.net/dna/7qlPq/btsK4JNx1rQ/AAAAAAAAAAAAAAAAAAAAAFkMwSl31kPfgQi9LAQIOq19bY69diFDImmm0uAF-tFm/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=R7KkSpdkERclRlEalBV7rcYaTBg%3D)

정말 간단하게, 내적을 이용해서 나에게 안보이기 직전(?)인 부분을 검정색으로 그려준다.

```
float edge = abs(dot(V3, N3));
if(edge < 0.2) fColor = vec4(0.1,0.1,0.1,1);
```

![](https://blog.kakaocdn.net/dna/uAhaS/btsK6uODf5M/AAAAAAAAAAAAAAAAAAAAAJZS-VvEc_1ZV9_Sib2pkI7qoBbt7EAsCva_bQsLyRLb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GHAeHpycMBV%2FY%2BFaQvpign2PUIM%3D)