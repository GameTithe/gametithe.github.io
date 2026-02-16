---
title: "[논문정리]Gaussian-Splashing"
date: 2024-11-01
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

<https://www.youtube.com/watch?v=KgaR1ni-Egg>



읽어보고 있는데, 지금까지 이해한것을 간단하게 적고 업데이트 해보겠다!

1. 3DGS(Gaussian-Splatting) 을 통해서 Object의 위치에 타원(Particle)을 형성한다

2. SPH도 유체 시뮬레이션 할 때 입자 기반으로 한다. (Smoothed-**Particle**-HydroDynamics)

3. SPH도 입자간의 상호작용, 3DGS도 입자 생성

4. 상호작용하게 만들면 잘 작동되겠는데?

가 기본 아이디어인 것 같다.

3DGS에서 발전된 것은

여기서 유체의 표면을 계속 추적해서, 표면장력과 Material(PBR을 위해 여러 matrial을 가져온다.)을 표현할 수 있게했다.

시연 영상을 보면 유체 표면에도 환경맵이 적용된 것을 볼 수 있다.

앞부분을 읽었을 때는 Simultaion을 자랑하는 줄 알았지만, 사실 Rendering을 잘한다고 말하는 논문이었던 것..

#### 

우선 시뮬레이션은 Position Based Dynamics 와 Position Based Fluid로 이루어진다.

**자세한 공식 설명은 여기서하기 어려울 것 같다.(어렵고 복잡하고,,)** 설명하는 아이디어를 열거하는 방식으로 글을 이어가겠다.

#### **Position-Based Fluids**

* **입자 기반 모델**: 유체를 많은 수의 입자로 표현한다.
* **비압축성 유지**: 유체의 비압축성을 보장하기 위해 **밀도 제약 조건(SPH커널을 쓰더라구요)**을 각 입자에 적용한다.
* **제약 조건 투영**: 제약 조건을 만족시키기 위해 입자들의 위치를 반복적으로 조정한다.

#### **표면 추적 & 표면장력**

**===추가중..====**

![](https://blog.kakaocdn.net/dna/cM0KoE/btsKAskhYKX/AAAAAAAAAAAAAAAAAAAAAKrimWvADCx3A4HplLA0uS6faN0vvb7-3Q1oPKgRUl3K/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=dtXOVnd%2Bsh7gxuKYwbZ6yiK0iM4%3D)

**입자 분포**

입자의 분포가 불균일해서 시뮬레이션이 잘 안되었다. 그래서 균일하게 맞춰주었다. 그랬더니 렌더링에 이상이 생겼다.

**불균일해도 문제 균일해도 문제다.**

![](https://blog.kakaocdn.net/dna/bks1VZ/btsKAXqwpde/AAAAAAAAAAAAAAAAAAAAAMbgNS8eEVqSOUF6rFaCko5nOn75ZnyRgGKfFqcjIHOg/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=EIn5eXr3JeBksYV8PIhw8oACH%2Fk%3D)

좌측(가우시안 커널), 우측(NeuS로 재구성)

**불균일한 가우시안 커널 분포**

* **불안정하고 부정확한 모션 합성**을 야기한다.
* 가우시안 커널은 주로 객체의 **표면과 가장자리** 주변에 불균일하게 분포하는 경향이있다..
* **시뮬레이션에서 경계 설명**이 **부정확**해져 객체 간의 상호작용에 문제가 발생한다.

**지나치게 균일한 분포**

* **너무 균일한 분포**는 **렌더링 품질**에 부정적인 영향을 미친다.
* **객체가 변하는 텍스처**를 표현하는 데 어려움이 있다.

그래서 **결론**

**시뮬레이션과 렌더링 두개의 별도의 커널을 가지고 있겠다!**

**GMLS로 가우시안 커널의 애니메이션화**

* **GMLS(Generalized Moving Least Squares):**
  + Sr커널의 임의의 포인트 지점 i를 Pri라고 하고, Sr커널의 임의의 포인트 지점 i를 Pri라고 하자. (S 는 포인트들의 집합)
  + Ss에서 Pri에 인접한 포인트들을 저장한다. -> N(i)
  + 시뮬레이션이 진행되면 N(i)를 이용해서 렌더링한다.

**귀찮게 왜 Ss, Sr을 매핑시켜놔요...?**

위에서 말한 것처럼 시뮬레이션하기 위해 사용하는 커널로는 렌더링을 할 수 없다!

두개를 같이 쓰기 위한 초기 작업을 하는 것이라고 생각하면된다.

**===추가중..==== 조금남았습니다..**