---
title: "[CG] Texturing"
date: 2024-12-04
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

Texturing을 바로 다루기 전에, 셋팅해야 될 내용들이 있다.

### **1.Wrapping**

0~1인 해당 범위를 벗어 났을 경우 어떻게 처리할 지에 대한 것이다.

Repeat와 Clamp가 있다.

Repear는 1을 다시 0부터 시작하게 하는 것이고,  Clamp는 1이상은 모두 1로 처리하는 것이다.

![](https://blog.kakaocdn.net/dna/bnR7TQ/btsK46hy5R6/AAAAAAAAAAAAAAAAAAAAAI_lKuJKJ26L0itTZbNWvgXN_y6iCI5PHUHYEAmRZTYT/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KMYA1TpwdzUxkAaDy4i2tmlqz28%3D)

### 

### **2. Magnification, Minification**

Texture의 크기 보다 크게 맵핑할 때(Magnification), 작게 맵핑할 때(Minification) 어떻게 처리할 지 우리가 미리 정해줘야된다.

![](https://blog.kakaocdn.net/dna/ZuMgL/btsK5BhjMio/AAAAAAAAAAAAAAAAAAAAABG-e9vywqW0NT_EeKvde5saBwZC0CGPtt-8Njo23p7O/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KwWlPDyL4yztcUuaykDxQuj%2F1eE%3D)

그 방법으로는 Nearest(가까운 값 선택) , Interpolaion(보간)이 있다.

Nearest는 가까운 값을 선택하기 때문에 무늬가 생긴다. ( 부드럽게 처리가 아니라 색을 선택하기 때문에 순간적으로 색이 변화한다.)

Interpolaion은 보간하는 방법이기에 부드럽게 표현된다.

![](https://blog.kakaocdn.net/dna/bqd9Jb/btsK7GOMiek/AAAAAAAAAAAAAAAAAAAAANjxHEhDbXIn7MvyiqfeOaLPKvVY12tWjz-iBI428wGt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=44iuulr0NJ5TrrNmLU3iSo0MncA%3D)

아래의 코드를 보게된다면 WRAPING과 (\_S, \_T는 uv좌표를 의미한다.) MAG,MIN Filter를 초기화해주는 것을 볼 수있다.

이렇게 초기화하면 Texture을 넘겨줘야 Texture를 사용할 수 있다.

```
glTexImage2D(GL_TEXTURE_2D,
	0/*/mipmap*/, GL_RGB, w, h, 0 /*1 or 0*/, GL_BGR, GL_UNSIGNED_BYTE, img);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR); //GL_NEAREST
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
```

아래에서 Texture Color \* (Ambient + Diffuse) + Specult 로 구현했다.

이것을 변형하면 색다르게 렌더링을 할 수 있다.

```
	vec4 texColor = texture(uTex, T2);
	vec4 cldColor = texture(uTexCld, T2 + vec2(uTime / 10, 0));
	
	//fColor = (uAmb + uDif*NL)*texColor + uSpc*VR; 
	//fColor = (uAmb + uDif*NL) + uSpc*VR*texColor; 
	fColor = (uAmb + uDif * NL ) * (texColor + cldColor) + uSpc * VR;
```

좌측이 Linear ( 부드럽 ), 우측이 Nearest ( 딱딱 )이다.

![](https://blog.kakaocdn.net/dna/tGb81/btsK5N9NcTV/AAAAAAAAAAAAAAAAAAAAANG_22PMh2oYFe2Btp0sOysHbqqj1dTWYmSIsl60zZWF/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=c72lrIMem7jcKrmtaQuYh4NjT8E%3D)![](https://blog.kakaocdn.net/dna/Az1QA/btsK58Z7Zoc/AAAAAAAAAAAAAAAAAAAAAJrDqB8NNtBmb8WMQzC7QLrm4_EIZFYF7tDsd6GWL-Jw/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2Bmi2lb2DdM36zDjZHk2WsXubDSA%3D)

![](https://blog.kakaocdn.net/dna/c9mmB1/btsK59LwiVR/AAAAAAAAAAAAAAAAAAAAADaLcdigzxgExX6iHA6gGOzS0XJcinrPqr-QEctXibjF/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=VV55xZ1KpcGe%2F32AtZduNug0%2B3Y%3D)![](https://blog.kakaocdn.net/dna/rlTy7/btsK5ubwUW7/AAAAAAAAAAAAAAAAAAAAAF6UKGuJLSjvdgTp7Mw93satBnEtyDyKKc6kQhQ6oTkU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=OKUl%2FIovSuW3fnMhJhjMyMg3IKQ%3D)

Specular Map

이거는 단순히 격자무늬를 texture(배열로 만들어서 texture처럼 사용했다.)로 그린 것이지만 ,

그럴싸한 texture를 사용하면 더 멋이게 렌더링을 할 수 있다.

texture를 여러개 사용할 수도 있다.

![](https://blog.kakaocdn.net/dna/JpPQ5/btsK66fY888/AAAAAAAAAAAAAAAAAAAAAHEgh6Pezg5JOuZm5puZU_bSQh9QeJWaoibnXGbMGCUZ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=dON6PHZxjQ7%2Bl1x701%2F%2BEG45wCU%3D)![](https://blog.kakaocdn.net/dna/nAE2L/btsK7dMSfm9/AAAAAAAAAAAAAAAAAAAAAPEuagVO1kJ90d0ooul1uJLsjUeZiHRhsM0YxN1pDdyJ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=PU4vmSeyG8ipv83oRz0koBTV19c%3D)