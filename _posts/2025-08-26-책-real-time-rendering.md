---
title: "[책] Real-Time Rendering"
date: 2025-08-26
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### Physically Based Shading

**광학적인 개념에 대한 소개이다.**

개인적으로 정~~~말~~ 재미없었다... 그래도 BRDF를 알려면 읽어야하지 않는가...! 하하.. 허허.. OTL

<https://tithingbygame.tistory.com/258>

[[RealTimeRendering] Physically Based Shading(1)

NPR 부분을 읽어보려다가 PBR먼저 정리하고 가면 좋을 것 같아서Physically Based Shading을 한 번 정리해보려고 합니다. Physics of Light 빛과 물질의 상호작용은 물리 기반 셰이딩의 토대를 이룬다. 이러한

tithingbygame.tistory.com](https://tithingbygame.tistory.com/258)

<https://tithingbygame.tistory.com/259>

[[RealTimeRendering] Physically Based Shading(2)

Surfaces광학적 관점에서, 물체의 표면은 서로 다른 굴절률 값을 가진 두 부피를 구분하는 2차원 경계면이다. 빛 파동이 어떤 표면에 부딪히면, 두 가지 요소가 결과에 중요한 영향을 준다:1. 표면

tithingbygame.tistory.com](https://tithingbygame.tistory.com/259)

**드디어 BRDF 이론 시작이다**

고생끝 고생시작이다. 수학 수식이 조금 나온다.. .그래도 겁먹지 말고 도전해보자!  
<https://tithingbygame.tistory.com/260>

[[RealTimeRendering] BRDF

BRDF궁극적으로, 물리 기반 렌더링은 어떤 view ray 집합을 따라 카메라에 들어오는 radiance(휘도)를 계산하는 것이다. 주어진 뷰 레이에 대해 우리가 계산해야 하는 값은 Li(c, v) 이다.c 는 카메라 위

tithingbygame.tistory.com](https://tithingbygame.tistory.com/260)

**Fresnel에 대한 글**

반사율과 굴절률에 관한 내용이다.

[[RealTimeRendering] BRDF

BRDF궁극적으로, 물리 기반 렌더링은 어떤 view ray 집합을 따라 카메라에 들어오는 radiance(휘도)를 계산하는 것이다. 주어진 뷰 레이에 대해 우리가 계산해야 하는 값은 Li(c, v) 이다.c 는 카메라 위

tithingbygame.tistory.com](https://tithingbygame.tistory.com/260)

<https://tithingbygame.tistory.com/261>

[[RealTimeRendering] Fresnel Effect

Illumination (조명) 전역 조명은 BRDF가 끝난 이후의 장에서 따로 다룬다.이 장과 다음 장에서는 각 표면 지점에서 반사 방정식을 사용해 local illumination(로컬 조명)에 초점을 맞춘다.로컬 조명 알고리

tithingbygame.tistory.com](https://tithingbygame.tistory.com/261)

### Non-Photorealistic Rendering

NPR의 전반적인 내용애 대해서 다룹니다.

주로 윤곽선에 대한 내용입니다.

<https://tithingbygame.tistory.com/256>

[[RealTimeReadering] Non-Photorealistic Rendering

렌더링에 대해서 공부하다가 NPR을 크래프톤 테크랩에서 구현해보고 싶어서, 이론을 먼저 학습해보려고한다. Non-Photorealistic RenderingPhotorealistic rendering은 이미지를 실제 사진과 구분할 수 없도록

tithingbygame.tistory.com](https://tithingbygame.tistory.com/256)

### 

### Transforms

좌표계 변환에 대해서 다룹니다.

<https://tithingbygame.tistory.com/30>

[[RealTimeRendering-4th] Transforms (1)

변환(Transform)은 굉장히 중요합니다. 객체, 빛, 카메라를 배치, reshape(모양 재배치), 애니메이션을 다룰 수 있게 해줍니다. Linear Transform (선형 변환)선형 변환임을 확인하기 위해서 2가지를 만족해

tithingbygame.tistory.com](https://tithingbygame.tistory.com/30)

<https://tithingbygame.tistory.com/63>

[[RealTimeRendering-4th] Transforms (2)

Shearing 게임에서 왜곡 효과를 줄 때 사용되는 효과이다. 환각제 효과나 오브젝트를 휘게(warp) 만들 때를 예로 들 수 있다. 6개의 기본적인 shearing matrices가 있다. 첫번 째 첨자는 변경이 되는 좌표

tithingbygame.tistory.com](https://tithingbygame.tistory.com/63)[[RealTimeRendering-4th] Transforms (2)

Shearing 게임에서 왜곡 효과를 줄 때 사용되는 효과이다. 환각제 효과나 오브젝트를 휘게(warp) 만들 때를 예로 들 수 있다. 6개의 기본적인 shearing matrices가 있다. 첫번 째 첨자는 변경이 되는 좌표

tithingbygame.tistory.com](https://tithingbygame.tistory.com/63)

<https://tithingbygame.tistory.com/64>

[[RealTimeRendering-4th] Transforms (3)

The Euler Transform(오일러 변환)The Euler Transform(오일러 변환)은 자신 또는 다른 Entity를 특정 방향으로 변환시키는 직관적인 방법이다.첫번째로 defualt view 방향이 설정되어야한다. (대부분은 -z)Euler Tra

tithingbygame.tistory.com](https://tithingbygame.tistory.com/64)