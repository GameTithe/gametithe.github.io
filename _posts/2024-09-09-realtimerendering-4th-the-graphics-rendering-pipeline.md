---
title: "[RealTimeRendering-4th] The Graphics Rendering Pipeline"
date: 2024-09-09
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### 

![](https://blog.kakaocdn.net/dna/Sa2mb/btsJvvh1npd/AAAAAAAAAAAAAAAAAAAAAEt_H_IqJSQCnW6ftkM_tYg1wJNlnSXPAvoiwtTJ93jW/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=B6eBUA4H7m0KjGotcsu8XSmRIQk%3D)

### Pipeline을 보면 위의 그림과 같다. ( 책에서 제공 )

![](https://blog.kakaocdn.net/dna/M4731/btsJuE07Af9/AAAAAAAAAAAAAAAAAAAAAMbdHLm5A9GRvFdPhUdqtPwi6eZJXlo00mreYBpF7geo/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=kPz6MgoL%2B85uIhMt%2FG45Eh85L%2FE%3D)

개인적으로 이게 더 좋은 것 같다 (vulkan graphics pipeline)

### 1. Application Stage

* **역할**: 주로 CPU에서 실행되며, 충돌 감지, 물리 시뮬레이션, 입력 처리(키보드, 마우스), 컬링(culling) 등과 같은 다양한 작업을 수행합니다.
* **병렬 처리**: 이 단계는 성능 향상을 위해 여러 프로세서 코어에서 병렬로 실행됩니다.
* **출력**: Application Stage가 끝나면, 렌더링할 기하학적 데이터를 Geometry Stage로 전달합니다.

( inputAssembler는 정점, 인덱스를 받는 과정이라고 생각하자. DX11을 하면서 tagentVector, normalVector도 같이 넘겨준 기억이 있다.)

### 2. Geometry Stage

* **구성:** Vertex Shader, Tessellation, Geometry Shader로 구성되어있다**.**
* **역할**: 주로 GPU에서 처리되며, 물체의 기하학적 데이터(정점, 삼각형)를 변환하고 처리합니다.
* **Vertex Shading:** 정점의 위치를 계산하고, 각 정점의 Normal, Texture 좌표 등 vertex output 데이터를 평가합니다. 여기서 계산된 정점의 정보는 이후의 단계에서 사용됩니다.
  + **좌표계 변환:** 물체는 모델 좌표계(local space)에서 Screen Space까지 좌표계가 변환된다.
  + **투영:** 물체를 투영하여 Canonical View Volume으로 변환한다. (**이후(rasterization)** 단계에서의 Clipping 작업을 위해 / Canonical View Volume은 Normlized Device Coordinate과 동일하게 봐도 된다. NDC는 크기가 1인 단위 정육면체 볼륨으로 좌표계를 바꿔준다고 생각하자.)

좌표계 변환 과정을 그림으로 보자

![](https://blog.kakaocdn.net/dna/bcKdkb/btsJuXGbARJ/AAAAAAAAAAAAAAAAAAAAAMciWrn9ll_7FFv1KjgyjnNNdZdxWw-yqkzyVI8CGYL0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=21oKZCoiboGNnKhi5%2FwfHTbSzcs%3D)

( Clip Space는 **투영 변환**이 적용된 후의 좌표 공간이다. 이 공간에서 정점은 동차 좌표계(homogeneous coordinates)로 표현되며, 각 좌표는 x, y, z, w의 형태로 나타낸다.

NDC는 Clip Space 좌표를 w 값으로 나눈 후의 좌표 공간이다. 즉, x/w, y/w, z/w의 결과로 나타나는 좌표 공간입니다. 이 변환은 정점을 **정규화된 범위**로 제한한다. NDC 좌표는 클리핑 후에 Rasterization 단계에서 픽셀로 변환될 준비가 된 상태를 나타낸다.)

* **Tessellation:**  멀리있는 물체는 가까이 있는 물체보다 덜 자세히 그려도된다. 이것을 조절해주는 단계이다.                 ( Level of Detail, Unreal5 의 Nanite에 이용된다. )

* **Geometry Shader****:** inputAssember에 보내준 정점 외에 추가로 정점을 생성할 수 있다. (사용예로는 불꽃놀이 시뮬레이션이 있다.)

### 3. Rasterization Stage

* **역할**
  + **Find Area:** Geometry Stage에서 전달된 삼각형의 정점을 받아, 삼각형 내부의 모든 픽셀을 찾아내고 이를 다음 단계로 넘겨줍니다.
  + **Clipping****:** ClipSpace 밖에 있는 부분을 잘라낸다. (그리지 않는다)
* **출력**: 각 픽셀의 위치와 색상에 대한 정보를 Pixel Processing Stage로 전달합니다. ( 이때 정규화가 된 자표로 보내진다. NDC)

### 4. Pixel Processing Stage

* **역할**: 전달받은 픽셀의 색상을 결정하고, Depth 값을 사용해 해당 픽셀이 화면에 표시될지를 판단합니다. 블렌딩(Blending)과 같은 추가 처리도 여기서 수행됩니다.