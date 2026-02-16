---
title: "[논문 정리] Gaussian Ray Tracing: Fast Tracing of Particle Scenes (ing)"
date: 2024-11-14
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

뭐가 됐든 그래픽스는 시연 영상을 봐야지 논문 읽는 맛이 난다. :)

<https://www.youtube.com/watch?v=UwL-4LOhxx8>



논문을 읽기 위해서는 Gaussian Splatting에 대해서 먼저 알긴해야된다. 나중에 시간 되면 정리해보겠다. 읽는 분이 모르실 수 있으니 아주아주 간단하게 설명하자면: <https://tithingbygame.tistory.com/87>

[[논문저장소] Gaussian Splatting (미완..이여서 미안...해요)

Gaussian Splashing, Raytracing을 읽는데 필요한 지식이지만,,,, 정리 순서는 어쩌다보니,, 마지막이 될 것 같아서 일단은 간단히만 정리해두고나중에 다시 와서 추가하겠다!!!  일단 이미지를 많이 가

tithingbygame.tistory.com](https://tithingbygame.tistory.com/87)

ray tracing은  컴퓨터 그래픽스에서 그림자, 반사와 같은 두개의 조명 효과를 처리하거나, 로봇 공학에서 흔히 사용하는 왜곡된 카메라로부터의 렌더링등 여러 이점들이 있다.

여기서 다루는 렌더러는 이러한 유연성을 제공하면서도 rasterization과 비교해 성능 손실이 거의 없다.

또한, 기본적인 가우시안 표현에 대한 개선점을 제안하고, 일반화된 커널 함수를 사용하여 입자(hit count)의 개수를 크게 줄일 수 있다고 포문을 열었다!!!! :)

입자를 사용한 씬에서 전역(global) 조명, inverse lighting에 대한 완벽한 정리를 제공하는 것이 아니라

문제에 대한 중요한 알고리즘인 **빠른 미분 가능 레이 트레이서를 제공**하는 것이라고 미리 말한다.

논문에서 말하고자 하는 것은

* 반투명 입자를 위한 GPU 가속 레이 트레이싱 알고리즘.
* 레이 트레이싱된 입자 기반 필드를 위한 최적화된 파이프라인.
* 교차점을 줄여서 렌더링을 더 효율적으로 만들어주는 가우시안 입자 공식

### 

### 관련 연구들을 설명한다.

본론으로 갈 때까지 간단히 적고 넘어갈게요!

**2.1 Novel-View Synthesis and Neural Radiance Fields**

NerF + 후속 연구들..

NeRF(NeuralRadiance Fields)의 등장으로 장면을 신경망으로 표현하여 고품질의 새로운 시점 이미지를 생성하는 것이 가능해졌다.

이후 다양한 연구를 통해 속도, 품질, 적용 범위 등이 개선되었지만, 여전히 trainig 과정에서의 높은 계산 비용이라는 문제가 남아 있다.

개선된 방법들은 높은 품질과 빠른 렌더링 속도를 제공하지만, **계산 비용이 많이 드는 다단계 훈련 절차**를 필요하다.

**2.2 Point-Based and Particle Rasterization**

**flow**

1. 객체 표면을 점으로 구성해보자 => 점이 작아서 구멍, aliasing이 발생

2. 그럼 Particle로 만드는거 어때?

3. 거기에 신경망까지 더하는거 어때?

4. 미분 가능 렌더링으로 빠른 렌더링 가능

* 수백만 개의 입자가 있는 장면의 실시간 최적화 가능.

5. 3D Gaussian Splatting (3DGS)의 등장

**후속 연구**

* **렌더링 시간 및 메모리 사용량 감소:** Fan et al. 2023; Niedermayr et al. 2023; Papantonakis et al. 2024.
* **표면 표현 개선:** Guédon and Lepetit 2023; Huang et al. 2024.
* **대규모 장면 지원:** Kerbl et al. 2024; Ren et al. 2024.

6. 래스터화의 한계와 우회 방법

왜곡된 장면, 조명이 여러개 있을 때, 모션 블러 같은 특정 장면 시뮬레이션 불가

어찌 어찌 우회는 해서 시뮬레이션 해도 근본적인 해결은 아님

**그래서 우리는~**

**3DRT의 장점 (논문의 기술)**

* **최적화된 레이 트레이싱을 훈련과 추론을 전체에 사용한다****.**
  + **Rasteriazation의 한계를 극복: **굴절, 렌즈 왜곡 등 복잡한 효과 가능****
  + **stretched icosahedron(이십면체)를 사용하여 높은 FPS 달성.=>빠른 렌더링**

2.3 Differentiable Ray Tracing of Volumetric Particles

**기존 연구들의 한계**

* 반투명 입자를 효율적으로 처리하는 데 어려움이 있다.
* 모든 입자를 순회하는데 제한사항이 있다. (가우시안 스플레팅에서)
* hit 순서 처리가 일관성이 없어서 아티팩트가 발생할 수 있다.

**근데 우리는**

* 광선과 교차하는 모든 입자를 일관된 순서로 처리하여 미분 가능성을 보장한다.
* 수백만 개의 입자가 있는 복잡한 장면에서도 실시간으로 고해상도의 이미지를 렌더링할 수 있다.

### 

### **배경지식**

### **3.1 3D Gaussian Parameterization**

μ는 **입자의 중심 위치**이고, x는 **그 중심 위치 주변의 어떤 좌표**를 의미한다. 이를 통해 3D 가우시안 입자의 밀도 분포 x에서 계산되며, 이때 x−μ를 통해 x가 입자의 중심으로부터 얼마나 떨어져 있는지를 나타낸다.

![](https://blog.kakaocdn.net/dna/bUIbgg/btsKDWkBFnG/AAAAAAAAAAAAAAAAAAAAAH26T8jCQsMCz7Bj5F643ddy0JuW2sUk4OSx4GjGGMr-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ytZkdB%2Bza3Reb82MwrWrJbOonS0%3D)

Σ 를 최적화할 때 양의 준정치성을 보장하기 위해, 우리는 이를 다음과 같이 나타낸다.

양의 준치성: xTAx≥0 (대칭행렬이면서 이를 보장할 때)

![](https://blog.kakaocdn.net/dna/qFa7X/btsKDVMLrSN/AAAAAAAAAAAAAAAAAAAAAIs5G5rgyy2dNCzD-nVhRbQSfaF2iwsCpljmWFhFoU5S/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=yTiTBkhklTF53iEW5t1WDFv6b3g%3D)

보충설명

S\*ST를 보면 S의 제곱이라고 볼 수 있다. => 양수

Rotation으로는 음수 못 만듬 => 양수

ϕ: 방사함수인데, direct의 따른 빛의 세기와 특성으로 보면됨

![](https://blog.kakaocdn.net/dna/bkp3lB/btsKCwgHXSt/AAAAAAAAAAAAAAAAAAAAAIvkbQ7aOSppEgZjTU-ru46I-yEbcTRHQ4U8uePCXv5w/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=VXil8kgFwkkRw9RiteZrF0zKXL4%3D)

* Y(구면조호함수): 구의 표면 위를 정의한 함수, 다양한 방향에서 빛의 변화를 표현( 복잡한 방향 의존성을 효율적으로 표현하는 데 사용된다. )
* β: 계수 벡터로, 입자의 색상 정보를 담고 있다.
* f: 시그모이드 함수로, 출력 값을 [0, 1] 범위로 정규화한다.

### **3.2 Differentiable Rendering of Particle Representations\\**

**장면은 ray를 통해서 그려지고,** **r( τ ) = o + τ d이다.**

L은 광선의 최종 색상이고, 아래의 공식과 같다.

![](https://blog.kakaocdn.net/dna/uBGJn/btsKDj8qOmG/AAAAAAAAAAAAAAAAAAAAAFeVrSfTrLzfOgGF0ZTwVlsu5najHwQgmsFDBic3uact/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nZwTrNn5BxD5Csx1ZkA7GbIEe88%3D)

i번째 가우시간의 색상을 나타내는데 c이다. 그러니 c = ϕ이다.

**T(o,d)는 투과함수이다.**

![](https://blog.kakaocdn.net/dna/wnFmG/btsKEkej2dc/AAAAAAAAAAAAAAAAAAAAADrNsK66VFvYxEGZ_jA8jmPT4mjIVHW9SjHOTObjnakP/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=6zlhwiT84Ni8czTUqXc6bz38Id8%3D)

함수가 너무 복잡해서, 비용이 비싸니 단순화해본게 아래와 같다.

x는 광선r를 따라 갔을 때 가질 수 있는 p의 최댓값이다.

σ는 불투명도이다.

![](https://blog.kakaocdn.net/dna/cnvkF1/btsKEG9ikp5/AAAAAAAAAAAAAAAAAAAAAEtvS8xfNmPKOMw2jK_C7-p4IznsvM1msOGW653SXa5F/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=lwjmbleWxraFfPYlT%2FYdt6lQSFI%3D)

최종 식은

![](https://blog.kakaocdn.net/dna/b92aU4/btsKCwViU3s/AAAAAAAAAAAAAAAAAAAAALgN9Eiu20t3jVrVphc98HqO39PDLGoHrpdoK57Iy1Lv/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=yHkqLTwicS%2FKyEqSmBpyY9q%2FgP0%3D)

( i에서의 생상 \* 불투명도) \* ( i 까지 도달하기 전에 빛이 물체를 만나서 투과되는 양 (점점 줄어들겠죠?) )

### **3.3 Hardware-Accelerated Ray Tracing**

**NVIDIA OptiX:** GPU에서 레이 트레이싱을 수행하기 위한 프로그래밍 인터페이스(API)이다. 개발자들이 레이 트레이싱 알고리즘을 쉽게 구현하고, GPU의 고성능을 활용할 수 있도록 도와줍니다.

**NVIDIA RTX:**하드웨어는 레이 트레이싱을 가속화하기 위해 **RT 코어**라는 전용 하드웨어 유닛을 포함하고 있다. RT 코어는 광선(ray)과 기하학적 프리미티브(삼각형, 곡면 등)의 교차 검사를 매우 빠르게 수행할 수 있습니다.

* **SMs(Streaming Multiprocessors)**: 일반적인 계산 작업(예: 셰이딩, 텍스처링 등)
* **RT 코어**: 광선과 프리미티브의 교차 검사
* **상호작용**: SM은 RT 코어에 광선의 교차 검사를 요청하고, RT 코어는 교차 결과를 반환한다.

ray tracing을 위해서 Hardware에서 특정 파이프라인을 사용해서 가속화해준다. (programable)

**1. ray-gen 프로그램(광선 생성)**

각 픽셀 또는 샘플에 대한 광선을 생성하고, 해당 광선에 대한 장면 순회를 시작한다.

**2. intersection 프로그램(교차 계산)**

RT 코어는 삼각형과 같은 기본 프리미티브에 최적화되어 있으므로, 다른 유형(ex. 복잡한 곡면, 사용자 정의 기하학 등)의 프리미티브에 대해서는 intersection 프로그램에서 교차 검사를 구현해야된다.

**3. any-hit 프로그램(모든 히트 처리)**

광선이 프리미티브와 교차할 때마다 호출되며, 해당 히트를 추가로 처리하거나 무시할 수 있다.

반투명한 재질의 경우, 광선이 여러 프리미티브를 통과하면서 각각의 히트를 처리해야 한다.

**4. closest-hit 프로그램(가장 가까운 히트 처리)**

광선의 순회가 끝난 후, 가장 마지막에 적용된 히트에 대해 추가 처리를 수행할 수 있다

**5. miss 프로그램(미스 처리)**

 광선이 어떠한 프리미티브와도 교차하지 않았을 때 호출되며, 추가 처리를 수행한다 (ex. 배경 색상 설정, 환경 맵 적용 등)

만약에 교차점이 적었다면 ( 광선과 object간에) 연산량도 적을 것이다.

이 work의 목표는

파이프라인의 목표는 효과적이고, 미분 가능한 알고리즘으로구현하는 것이다.

### **4. Method**

![](https://blog.kakaocdn.net/dna/D2ng6/btsKNrE908o/AAAAAAAAAAAAAAAAAAAAAHexio_p_E5dg1gNfrqmArBCIYwvrazgyXFhCeUnI_sN/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=7ynMwUcFyUyJWYp0cBe9qOGXcqs%3D)

**2개의 핵심 구성요소가 있다.**

**1. BVH (Bounding Volume Hierarchy):**

교차점을 효과적으로 구할 수 있도록 도와준다.

**2. rendering algorithm**

광선을 발사하고 교차 지점들의 배치를 수집하여, 효율적으로 스케줄링하는 렌더링 알고리즘.

( NVIDIA OptiX 트레이싱 모델)

### **4.1 Bounding Primitives**

**BVH가 뭐예유?**

공간 내의 객체들을 계층적으로 분할해서 광선과의 교차 검사를 빠르게 수행하기 위한 데이터 구조입니다.

그렇다면...

입자들을 BVH에 어떻게 삽입하고, 광선과의 교차를 효율적으로 테스트할 것인가?

**여러 가지 전략과 그 한계**

**단순한 AABB:** 각 입자를 둘러싸는 AABB를 사용하면 빠르게 교차 검사를 할 수 있다.

**한계:** 많은 **거짓 양성(false-positive)** 교차가 발생할 수 있다.

아래 그림과 같이 빨간색이 aabb로 생긴 bounding box이다.

두 개의 삼각형은 서로 교차하지 않지만, aabb를 사용하면 교차한다고 판단을 할 것이다.

이것이 false-positive라고 볼 수 있다 :)

![](https://blog.kakaocdn.net/dna/bTd0rG/btsKOm3WQfD/AAAAAAAAAAAAAAAAAAAAANXC7IubvwYYYUKmN-yFnmecpP6Nv1CmLdyFwGSA0HDb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9MgzP3howKFOurzEBq1o2pL0s%2BY%3D)

**그럼 타이트하게 계산할까요?** 그럼  검사 비용이 증가해서 tradeoff가 발생한다....

여기서 사용된 방법은

**늘린 정이십면체 메쉬(Streched Icosahedron Geometry)이다.**

![](https://blog.kakaocdn.net/dna/xBBV7/btsKN5nQdZj/AAAAAAAAAAAAAAAAAAAAAFpcdgX-qVKgqeuYFn3eIZp8JO69nVMMrPYnCmhg3Uk_/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=l0eekF9REhNDRfchekUO2OPjwlY%3D)

**늘린 정이십면체 메쉬 사용**

최소 응답 값 a\_min(보통 0.01)을 설정해서, 그 값 이상을 커버하도록 정이십면테를을 비등방성(anisotropic)으로 스케일링한다.

(여기서 비등방성 스케일링은 비대칭으로 스케일링이라고 생각하면 된다.)

늘린 정이십면테 메쉬의 식은 아래와 같다.

![](https://blog.kakaocdn.net/dna/DQs7N/btsKMgxEESz/AAAAAAAAAAAAAAAAAAAAAMtwm0VS2oQa5lH0gxlL1gA_8znzxq559m6IIZPVHHQK/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=YHaSVeOQFBftaFllQ69LJpAJewg%3D)

v: icosahedron의 정점.

σ: 입자의 불투명도(opacity).

S: 입자의 스케일

R: 입자의회전 행렬.

μ: 입자의  중점 위치.

σ(불투명도)와 비례한다. => 투명도가 늦을 수록 v가 작아진다 => 투명하면 빛 흡수가 적으니 영향을 준다.

### **4.2 Ray Tracing Renderer**

광선을 따라 입자들의 기여도를 정렬된 순서로 누적하여, 볼륨 렌더링을 수행한다. (6번 식)

![](https://blog.kakaocdn.net/dna/b92aU4/btsKCwViU3s/AAAAAAAAAAAAAAAAAAAAALgN9Eiu20t3jVrVphc98HqO39PDLGoHrpdoK57Iy1Lv/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=yHkqLTwicS%2FKyEqSmBpyY9q%2FgP0%3D)

**어떻게 누적할건데?**

**가장 가까운 히트 반복 처리? => 비효율적임**

광선을 반복적으로 발사하여 가장 가까운 입자를 처리하고, 다시 광선을 발사하는 것.

**장면 두 번 순회? => 비효율적임**

한 번은 투과 함수(transmittance function)를 추정하고, 다른 한 번은 적분을 계산하는 방법

**제안된 알고리즘**

**Figure 5, Figure 3, Procedure 1 및 Procedure 2 참고( 아래 순서대로 넣었습니다.)**

![](https://blog.kakaocdn.net/dna/cyyHK4/btsKNoPgn9P/AAAAAAAAAAAAAAAAAAAAADIvLeyBs8EDtrA5o8VIXjwaEqCBxy-VB_O_piR51GBm/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=r5V%2FadRAcCMOt7JWpRhh4IZlt1E%3D)
![](https://blog.kakaocdn.net/dna/dzzCa6/btsKMDl3sr0/AAAAAAAAAAAAAAAAAAAAAOP9UKrz0YSVqnsu1kfqPHgIxMl36Az10ZXUtk38rwGv/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=erkZ6DgPws9aV7R33udDrL%2BFg48%3D)


![](https://blog.kakaocdn.net/dna/mWdj7/btsKNWrdBHJ/AAAAAAAAAAAAAAAAAAAAABoH65vx8NAvXWz1CL-LrTpFgltdTRkdw-kAo4BHUv9g/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Jh8HWve5wb7chYYmOtIM5OXYOkM%3D)![](https://blog.kakaocdn.net/dna/qtpME/btsKNp8r9qS/AAAAAAAAAAAAAAAAAAAAAODPsgilLL7eVd7U0XdXPKGh8HbmEJ01QTY76Cb6yK6c/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=de1vnt0Spz663EWbs8%2Fn5PwR%2FGQ%3D)

**광선 생성(ray-gen) 프로그램으로** BVH에 대해 광선을 추적하여 다음 k개의 입자를 수집한다.

**any-hit 프로그램**을 사용하여 입자의 인덱스를 정렬된 버퍼에 저장한다.

아직 이 단계에서는 입자의 응답(response)을 아직 평가하지 않는다. (추가적인 계산을 하지 않는다는 의미)

**ray의 충돌 검사가 끝난 후(정해둔 k가**

**) 렌더링하자**

광선 생성 프로그램은 정렬된 히트 배열을 반복하며, 각 입자에 대해 식 6에 따라 렌더링한다. (누적계산할 떄 사용했던,,, 올려보면 나옵니다)

**위의 내용들을 반복한다**

마지막으로 렌더링된 입자부터 새로운 광선을 추적하여 다음 k개의 입자를 수집합니다.

**종료 조건**

광선과 교차하는 **모든 입자가 처리**되면 종료한다.

또는 미리 정의된 **최소 투과율 t\_minT​에 도달**하면 조기 종료

우리의 알고리즘에 왜 좋으냐면..

**일관된 순서로 교차를 처리해서**, 입자를 놓치거나 근사 투과율을 사용하지않고 렌더링할 수 있다.

**미분 가능성:** 정확한 렌더링을 통해 미분 가능하며, 이는 학습 과정에서 중요하다.