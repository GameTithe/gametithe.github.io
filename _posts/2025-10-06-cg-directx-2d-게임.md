---
title: "[CG] DirectX 2D 게임"
date: 2025-10-06
toc: true
categories:
  - "자체 엔진"
sub_category: "DX11 Bgario" 
tags:
  - "DirectX"
---

2박 3일 동안 만든 게임입니다.

첫째날은 4-5시쯤 시작했으니.. 1.5박 2.5일 입니다 ㅎㅎ

어쩌다보니 해본 적 없는 UI를 담당하게 되었습니다..하하

0. 물체의 움직임에 대한 것도 제가 구현하긴 했지만,, 저의 첫 UI작업이었기에 UI위주로 작성했습니다

### 

### 1. UI 이미지를 넣어보자

스크린 좌표계를 이용해서 UI를 배치했고, 절대 위치로 배치하면 윈도우가 움직일 때 이상하게 보여질 것이기 때문에

비율도 같이 넘겨서 배치했습니다.

```
float w = targetSize[0] * (winSize[0] / winWidth), h = targetSize[1] * (winSize[1] / winHeight);
float cx = winSize[0] * ratio[0], cy = winSize[1] * ratio[1];
float x0 = cx - w * 0.5f, y0 = cy - h * 0.5f;
float x1 = cx + w * 0.5f, y1 = cy + h * 0.5f;
```



### 

### 2.  반응형 UI 제작

window size에서 React UI의 범위를 정하고, 이 안으로 마우스 커서가 들어오면 bool(true)값을 반환해

hovering을 처리했다.

```
inline bool CheckMouseOnUI(const UIReact& TestUIReact, float x, float y)
{
	return (x < TestUIReact.x1 && x > TestUIReact.x0) && (y < TestUIReact.y1 && y > TestUIReact.y0);
}

inline UIReact MakeRect(const float winSize[2], const float targetSize[2], const float ratio[2])
{
	// 하드 코딩 고치자
	float w = targetSize[0] * (winSize[0] / 1024);
	float h = targetSize[1] * (winSize[1] / 1024);
	float cx = winSize[0] * ratio[0];
	float cy = winSize[1] * ratio[1];
	
	UIReact r;
	r.x0 = cx - w * 0.5f; r.y0 = cy - h * 0.5f;
	r.x1 = cx + w * 0.5f; r.y1 = cy + h * 0.5f;
	return r; 
}
```

아래 이미지를 사용해서 위치도 screen 배경 색에 닿아도 hovering되는 문제..!

target size를 만들어서 크기를 임의로 ㅈ박 3일 동안 만든 게임입니다.

첫째날은 4-5시쯤 시작했으니.. 1.5박 2.5일 입니다 ㅎㅎ

어쩌다보니 해본 적 없는 UI를 담당하게 되었습니다..하하

1. UI 이미지를 넣어보자

스크린 좌표계를 이용해서 UI를 배치했고, 절대 위치로 배치하면 윈도우가 움직일 때 이상하게 보여질 것이기 때문에

비율도 같이 넘겨서 배치했습니다.

```
float w = targetSize[0] * (winSize[0] / winWidth), h = targetSize[1] * (winSize[1] / winHeight);
float cx = winSize[0] * ratio[0], cy = winSize[1] * ratio[1];
float x0 = cx - w * 0.5f, y0 = cy - h * 0.5f;
float x1 = cx + w * 0.5f, y1 = cy + h * 0.5f;
```

2. Hovering

window size에서 React UI의 범위를 정하고, 이 안으로 마우스 커서가 들어오면 bool(true)값을 반환해

hovering을 처리했다.

```
inline bool CheckMouseOnUI(const UIReact& TestUIReact, float x, float y)
{
	 return (x < TestUIReact.x1 && x > TestUIReact.x0) && (y < TestUIReact.y1 && y > TestUIReact.y0);
}

inline UIReact MakeRect(const float winSize[2], const float targetSize[2], const float ratio[2])
{
 	// 하드 코딩 고치자
     float w = targetSize[0] * (winSize[0] / 1024);
     float h = targetSize[1] * (winSize[1] / 1024);
     float cx = winSize[0] * ratio[0];
     float cy = winSize[1] * ratio[1];

     UIReact r;
     r.x0 = cx - w * 0.5f; r.y0 = cy - h * 0.5f;
     r.x1 = cx + w * 0.5f; r.y1 = cy + h * 0.5f;
     return r; 
}
```

아래 이미지를 사용해서 위치도 screen 배경 색에 닿아도 hovering되는 문제..!

이미지가 배경의 알파값이 0이기 때문에 UI 버튼 자체 크기는 작지만, 어쨌큰 전체키는 UI버튼 크기보다는 크다

![](https://blog.kakaocdn.net/dna/byjYuT/btsQjmYNymP/AAAAAAAAAAAAAAAAAAAAADXwu4TkQa-wJERTRDUQ5TLOcckSJNJu1DoF2thx2JKY/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3tmuLJwmtm62HUlhNCGAUltCyM8%3D)

이를 target size를 만들어서 크기를 임의로 조정해주었다. 

이렇게 UI를 잘 만들었다

![](https://blog.kakaocdn.net/dna/oCpMK/btsQmP7ww2A/AAAAAAAAAAAAAAAAAAAAAIQs-7GR-44M-DS_uAXpX9SaKFBCbWsVOtQQWOQa8p4C/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=EHhLA1bTrzJVO9yICr3UObOHFXk%3D)![](https://blog.kakaocdn.net/dna/MyJMP/btsQmWetMUA/AAAAAAAAAAAAAAAAAAAAAErrH4SXLH2zO0Yo7PQS-uUNtm9NFyyfsOoZmFSSyBq2/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=pcc78642ad21HsP1uvrSnCVJKAo%3D)![](https://blog.kakaocdn.net/dna/Rnw0V/btsQkf70rFE/AAAAAAAAAAAAAAAAAAAAAIgqcL_X-fN91utdezSEiaTfmwTjcJFmQ2d08CE5ksPl/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FzyKG%2BJxu%2BRBj3XJIocsLLlFdws%3D)

### 

### 3. Shader 입히기

Shader Toy에서 간단하고 예쁜 shader가 있어서 이를 적용시켰다.

<https://www.shadertoy.com/view/4dtcRs>

[Shadertoy

0.00 00.0 fps 0 x 0

www.shadertoy.com](https://www.shadertoy.com/view/4dtcRs)

계속 중앙 정렬이 안되서 골치가 아팠는데,, glsl를 hlsl로 바꾸는 과정에서 texture sampling을 하는데

이때 좌표계 y값이 반전되어야하는 것을 신경쓰지 못해서 이상하게 렌더링되는 것이였다..

OpenGL/Shadertoy: Y=+1 이 화면 위쪽

* DirectX: Y=+1 이 화면 아래쪽

```
float2 uv = input.uv; 
float a = max(0.0f, 1.0f - distance(uv, float2(0.5f, 0.5f)) / 0.5f);
```

![](https://blog.kakaocdn.net/dna/vAOBc/btsQjkAFEJ2/AAAAAAAAAAAAAAAAAAAAAGLkQ306FlfygIJRNZ69hTt_s2dXIRVeGAFvajTgBNqx/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GR%2FrJCOKL2SW0ysEHkZXA8lif7Q%3D)![](https://blog.kakaocdn.net/dna/eeXoBQ/btsQkkfW2zZ/AAAAAAAAAAAAAAAAAAAAAB48syDc7ngLT7dy0hoJw_YW8-PVtP3H5u1jkrfrqwvW/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=pwbRpPZDGXDPCHKhb5hn%2Bx24Umk%3D)

알파블렌딩을 하고, 파라매터 값도 잘 바꿔주면 예쁘게 잘 나온다.

여기서 구끼리 부딪히면서 먹을 때, Smooth blending이 일어났으면 좋겠다.

PS에서는 일렁이는 것을 처리하는 식 때문에, PS에서 하기에는 어려울 것 같아서

주면 Enemy나 Prey에 가까워지면 Vertex Position을 수정해서 빨려들어가는 것처럼 수정해주었다!

![](https://blog.kakaocdn.net/dna/qMolk/btsQlz5C1a5/AAAAAAAAAAAAAAAAAAAAAIeFYOkXNTfxCuC_zZox6kqLqWhLR0WWyCd6QE-9Mya5/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Wk6u3jkX5UWhFhn8pBb1%2F6wuho4%3D)

### 4. 최종