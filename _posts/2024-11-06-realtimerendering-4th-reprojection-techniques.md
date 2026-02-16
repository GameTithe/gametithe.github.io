---
title: "[RealTimeRendering-4th] Reprojection Techniques"
date: 2024-11-06
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

Reprojection은 이전 프레임에서 이미 계산된 샘플들을 재사용하는 아이디어에 기반한다. 명칭에서 알 수있듯 **새로운 시점**과 **방향**에서 가능한 한 이전에 계산된 샘플들을 재활용하여 렌더링 비용을 줄이는 방법이다.

이를 방법으로 여러 프레임에 걸쳐 렌더링 비용을 분산시키는 것이 목표이다. (temporal coherence을 활용).

이는 **temporal 안티앨리어싱**과도 관련이 있으며, 특정 상황에서 현재 프레임에서 렌더링을 끝내지 못한 경우에도 대략적인 결과를 생성하는 것이 또 다른 목표이다. 특히 가상 현실(VR) 애플리케이션에서 렌더링이 지연될 경우  멀미를 느낄 수 있기 때문에 Reprojection이 중요하다.

  Reprojection 방식으로 **Reverse Reprojection**과 **Forward Reprojection**의 두 가지가 있다.

## **Reverse Reprojection**

![](https://blog.kakaocdn.net/dna/bsecAm/btsKxPUwp4U/AAAAAAAAAAAAAAAAAAAAAH47-CyFI9LcNeP355cfACj1Zi8VBiNqWSWU_vo99Q3G/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=lzkpGmABSuHfYSYZcZufzkaq%2Bho%3D)

삼각형을 렌더링할 때 VertexShader에서 각 정점의 현재 프레임(t)과 이전 프레임(t-1)의 위치를 계산한다.

Vertex Shader에서 얻은 z와 w를 통해서, Pixel Shader에서 보간된 z/w 값을 얻을 수 있다.

각 정점의 깊이(z)와 균일한 좌표(w)를 사용하여 현재 프레임(t)과 이전 프레임(t-1)에서 보간된 깊이 값을 비교합니다. 만약 **두 값이 충분히 유사하다면, 이전 프레임(t-1)의 색상 버퍼에서 해당 위치의 색상값을 가져와 새롭게 계산하는 대신 이전 값을 사용**할 수 있습니다.

#### 

#### **주의사항**

**이전에 가려져 있던 부분이 새롭게 보이게 될 경우(p0부분)에는 색상값을 사용할 수 없기 때문에 새로 계산이 필요요하다.** 이러한 상황을 cache miss라고 부른다. 이런 경우 픽셀 쉐이더를 통해서 빈 공간을 채워야한다. 역방향 Reprojection은 일반적으로 **짧은 시간** 동안만 값을 재사용한다.  **쉐이딩 값을 재사용하는 것은 새로운 움직임(카메라, 조명 등)과 독립적이라고 가정하기에 부정확할 수 있다. 떄문에 너무 많은 프레임에 걸쳐서 재사용하지 말자**

#### **방지하기 위한 방법**

화면을 **n개의 2×2 픽셀 영역으로 나눈다.** 각 프레임마다, **단일 그룹을 업데이트시켜 픽셀 값이 너무 오래 재사용되지 않도록** 한다. 

더 나은 품질을 위해,  **running-average filter**를 사용할 수도 있다. 이는 오래된 값을 점차적으로 제거한다. 이러한 필터는 특히 안티앨리어싱, 부드러운 그림자, 글로벌 일루미네이션에 권장된다. 필터는 아래와 같다.

![](https://blog.kakaocdn.net/dna/bi85vK/btsKyjVvHUY/AAAAAAAAAAAAAAAAAAAAACissLQ2-Tx9pFB8AHbxRLIC5P2ih0bt4Zx-qb32ITAi/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1ocZ6nfgfwP5o0IGu1cgCIXccZU%3D)

**c(pt)는 현재 위치 pt**에서 새로 셰이딩된 픽셀 값이고, **c(pt−1)은 이전 프레임에서 reprotection된 색상**이며,

**cf(pt)는 필터를 적용한 후**의 최종 색상이다.

Nehab 등은 일부 사용 사례에서 α=3/5를 사용하지만, 렌더링되는 내용에 따라 다른 값을 시도해 볼 것을 권장한다.

(현재 위치의 pixel 색을 계산할 거면 왜 이전프레임이랑 섞는거예요? 그냥 쓰면되지? 라는 의문이 들 수 있다.

=> 안티앨리어싱을 위함이라고 생각하면 될 것같다. 변화를 부드럽게 표현할 수 있다. 부드러운 그림자를 표현할 때 그림자의 끝부분에서 주변 픽셀들 색을 이용했었다. 이와 같은 느낌같다.)

## 

## **Forward Reprojection**

forward reprojection은  **t−1 프레임의 픽셀에서 시작하여 그것들을 t 프레임으로 투영**한다. 이는 이중 버텍스 셰이딩이 필요없다. 즉**, t−1 프레임의 픽셀들이 t 프레임으로 scattering된다.**

**reverse reprojection 방법은 t−1에서 t로 픽셀 값을 수집합니다.** 이러한 방법들도 가려진 영역이 보이게 되는 상황을 처리해야 하며,  다양한  hole-filling 방법을 통해 이루어진다. (누락된 영역의 값들은 주변 픽셀로부터 추론된다).

reprojection이 관한 논문들은 책의 부록에 기되어있다.