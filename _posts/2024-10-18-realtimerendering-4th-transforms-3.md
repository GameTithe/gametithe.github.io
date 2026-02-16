---
title: "[RealTimeRendering-4th] Transforms (3)"
date: 2024-10-18
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

## **The Euler Transform(오일러 변환)**

The Euler Transform(오일러 변환)은 자신 또는 다른 Entity를 특정 방향으로 변환시키는 직관적인 방법이다.

첫번째로 defualt view 방향이 설정되어야한다. (대부분은 -z)

**Euler Transform은 3개의 Transform Matrices가 곱해진 것이다. ( E(h,p,r) )**

![](https://blog.kakaocdn.net/dna/b3mhkk/btsKcOtMsjs/AAAAAAAAAAAAAAAAAAAAANkIxUTctsVPWMUzSfv_ZFjpibeRpSSZL3cKTA_AIbNP/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=PFwrI4UvSVxFTUlfo%2B%2F9qK5DMos%3D)

행렬의 순서에 따라 24개의 Matrix를 만들 수 있다. 위의  E는 가장 common한 것으로 예시를 든것이다.

( 근데 Rx \* Rx \* Ry는 사실 Rx \* Ry 와도 같기에 제외하고 보는 곳도 있는 것 같다.

![](https://blog.kakaocdn.net/dna/mNu4h/btsKbE6Hnxv/AAAAAAAAAAAAAAAAAAAAAJbCCV-0x-Mki_sMTYmsLVSuLDN81wqtIHsN11ueDRio/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=JLhmSLm%2BfX7I%2FarGCiO2Rkfc5I0%3D)

그래서 학교에서는 12개의 조합이 있다고 배웠다. )

이전 글에 계속 설명했던 것처럼

Rotation은 Orthogonal Matrix이다. 그렇기 때문에 아래와 같이 볼 수 있다.

![](https://blog.kakaocdn.net/dna/oEavX/btsKcOAyeup/AAAAAAAAAAAAAAAAAAAAAHOTLHrG82PYfkjqv21SEvnY9skUwbxwudMoJT9RKwX0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FQtxs%2FW5GwQMXWcT8lyUpYq9khQ%3D)

Euler angle은 h, p, r 로 나타낼 수 있다. h = head, p = pitch, r = roll 이다. h(head)는 yaw로도 많이 알려져있다.

![](https://blog.kakaocdn.net/dna/crQCJI/btsKbI8VhvJ/AAAAAAAAAAAAAAAAAAAAAMgeRmuWWmGSm5AdxaaTnjsv3G2RXXOq2A2WzVmxAswb/tfile.svg?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=u%2FRcNaiHUdfO4OcI5SCGPSl2y%2Fw%3D)

Euler Transform은 카메라 뿐만 아니라 객체의 방향 또한 변환할 수 있다. 또한 World space나 local spae(relative to a local frame of reference라고 적혀있음)에서 사용가능하다.

Euler Anlge에서는 up vector가 z인경우도 있고, y인 경우도 있다. 우리는 y가 up vector라고 생각하겠다. (어느 좌표가 up vector인지는 굉장히 중요한 것이다!)

**또한 카메라의 up vector와 world 의 upvector는 아무 연관이 없다.**

그림을 그려봤다. 아무 연관이 없다는 것을...!

![](https://blog.kakaocdn.net/dna/cIkrn9/btsKb355kla/AAAAAAAAAAAAAAAAAAAAAFlXNAI_oBPujPXNrv7_PrqyzguARwD4KV0N1PufP_Rw/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=6WnpCnQE6gKyjckVe28clk4nTWE%3D)

사실 Euler angle에는 몇 가지 심각한 한계점이 있다.

1. 두 세트의 Euler angle을 결합(combination)하기 어렵다.

하나의 세트와 다른 세트 사이를 보간(interpolation)하는 것은 각각의 각도를 단순히 보간하는 문제가 아니다. 예를 들어 만약 두 가지의 다른 Euler angle임에도 같은 방향을 나타내고 있다면, 보간할 때 물체가 회전하지 않는다.

2. gimbal lock (짐벌락) 현상이 발생할 수 있다.

가운데 변환이 +90/-90도 회전할 시 회전 축 1개가 사라지는 현상

이러한 이유들 때문에 Euler angle은 사용되지 않고 Quaternian(쿼터니언)이 사용된다. 

## Rotation about an Arbitrary Axis

때로는 임의의 좌표축으로 Rotation을 하는 것이 편리하다. 임의의 축을 r이라고 해보자. (noramlized된 상태의 r)

r축을 기준으로 a  radian만큼 회전하고 싶은 상황이라고 가정하자.

r축을 기준으로 회전하기 위해서는

1.  Matrix M을 이용해서  회전 space를 x축으로 맞춘다.

2. 원하는 회전을한다.

3. M^-1을 해서 다시 돌아간다.   
  
그림으로 보면 아래와 같다.

![](https://blog.kakaocdn.net/dna/581dt/btsKb2TEvOf/AAAAAAAAAAAAAAAAAAAAABAZ_QiQIlx0yTNKqwQWdnx5aaD_drF4OR2ADN5XGHY6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2Frx%2F%2FQBoGCrNvX8g7boaf1yFhjg%3D)

여기서 궁금한건 M(r을 x축으로 어떻게 옮기냐)을 어떻게 만드냐는 것이다.   
M을 계산하기 위해서는 r에 수직이면서 서로 수직인 2개의 축(s, t)이 필요하다. (r에 수직인 2개의 축, 그 2개의 축끼리고 수직)

2개의 축 구하는 법

1. r에서 가장 작은 component를 0으로 바꾼다.

2. 남은 component 2개의 위치를 바꾼다.(swap)

3. 바꾼 component 중 앞에 있는 component에 -를 붙여준다.

(2D에서 (x,y) 벡터의 의 수직인 벡터는 (-y,x)이다. 이 아이디어를 사용한 것이다.)

이렇게 r에 수직인 축 s를 구하고, s와 r을 cross product해서 수직인 축 t를 구하면

 r에 수직이면서 서로 수직인 2개의 축 s,t를 구한것이다. 

수식으로 보면 아래와 같다.

![](https://blog.kakaocdn.net/dna/bMhWDU/btsKbFdr7Es/AAAAAAAAAAAAAAAAAAAAAMwJkYQelF_xZDe5D4RwAnaWyxKFprBzMfJ6dK2Li4wf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=CBh49r3n9OJ562C2JZVpMZScgPY%3D)

## 

## **Projection**

Scence에 실제로 렌더링하기 전에, 관련 모든 객체들을 plane이나 simple volume(NDC Coordinate로 보인다)에 projection(투영)을 해야된다.

그 후, clipping과 렌더링을 진행한다.

![](https://blog.kakaocdn.net/dna/bqkfMn/btsKcgRvR8U/AAAAAAAAAAAAAAAAAAAAAD_CNOgu8DGKferNpuiJYU3h931zcTlfwvObLyFa4i30/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=HhTXQGkWm0u7xIihJekIiPd1CMg%3D)

**지금까지 다룬 변환들은 4번째 component인 w에는 영향을 주지 않았다.** 이 말인 즉 변환 후에도 벡터는 벡터, point는 point로 유지되었고, 4x4 행렬의 마지막 행은 항상 (0,0,0,1)을 유지했다.

**하지만 Perspective projection은 이러한 속성에서 제외된다.(예외이다)** 그렇기 때문에 동차화(homogenization) 과정이 필요할 때가 있다. homogenization은 w가 1이 아니기 때문에 비동차 점(nonhomogeneous point)을 얻기 위해 w로 나눠주는 것을 의미한다.

하지만 **Orthographic projection(정사영)**은 더 단순한 형태의 투영으로, w에 영향을 주지 않는다.

여기서는 viewer가 카메라의 -z축을 따라 바라보고 있고, y축은 위쪽, x축은 오른쪽을 가리키는 것으로 가정하겠다. handedness는 오른손 좌표계다. DirectX에서는 시청자가 카메라의 +z축을 따라 바라보는 왼손 좌표계를 사용한다. 이론은 두 시스템에 모두 동일하게 유효하다.