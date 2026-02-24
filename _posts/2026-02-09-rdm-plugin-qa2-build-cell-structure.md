---
title: "[RDM Plugin] QA2: Build Cell Structure"
date: 2026-02-09
toc: true
categories:
  - "UE5_Plugins"
sub_category: "Realtime Destructible Mesh"
tags:
  - "UE5_Plugin"
---

중간 중간 작은 파편들이 발생하는 경우가 생겨서 Debug 모드로 자세히 살펴보았다.

아마 테스트하단 mesh가 육면체였기 때문에 아래의 이미지처럼 convex한 mesh에는 정확하게 생성이 안되는 모습을 띄었다.

![](https://blog.kakaocdn.net/dna/DfLQL/dJMcag5mAot/AAAAAAAAAAAAAAAAAAAAAGM5O44S0mBmo_BPmEbs4dMYhjcFz9chu1npVXqZqlEw/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=XQiaR26m%2B0eAoO3w4GafWuXPeVg%3D)![](https://blog.kakaocdn.net/dna/YAWqj/dJMcagdc58U/AAAAAAAAAAAAAAAAAAAAAHxejkXophRU27N9koV4LhWb1H_O-l7_qL1SHphWc1Kh/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=MlIRtxjlin%2BaHOyhUg0GITO5MS0%3D)

삼각형을 순회하면서 grid cell을 만들어주는 방법으로 변경했고 잘 생성되는 것을 확인했다.

(editor 모드에서 생성하는 것이기 때문에 성능보다는 정확성이 더 중요하다고 판단했다.)

(mesh의 vertex/ 삼각형 에 대한 데이터를 접근하기 위해서 정보가 들어있는 FMeshDescription를 사용했다.)

#### 

#### SAT(Separating Axis Theorem) 적용

삼각형이 복셀(AABB)을 아주 미세하게 스치기만 해도 감지하기 위해 **분리 축 이론**을 사용했습니다.

![](https://blog.kakaocdn.net/dna/bsRgc4/dJMcaaqwUNh/AAAAAAAAAAAAAAAAAAAAAM8TT8Gb2twQ5iztx2Mz1yJtfVk17YtuItGE_xlqXQtu/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=dE0ZehaAXbaBqRzhkjDCyxiFTSI%3D)

근데 vertex로 순회하니까 내부가 안생김.. 그래서 내부를 채울 수 있는 flood fill을 도입

### 

### Flood Fill 알고리즘

껍데기(Shell)만 있으면 파괴 시 내부가 텅 비어 보입니다. 속을 꽉 채우기(Solidification) 위해 **Flood Fill(플러드 필)** 알고리즘을 역으로 사용했습니다.

위의 방법으로 껍데기는 만들어져습니다. 이제 flood fill하면 위부 내부 판별이 가능해질 것입니다.

#### 알고리즘 로직

1. Bound는 무조건 바깥이다.
2. Bound에서 flood fill 알고리즘을 시작합니다.
3. 위에서 vertex에 겹치는 곳에 cell이 존재하기 때문에 내부에는 flood fill flag가 체크가 안됩니다.
4. 이제 flag가 false인 부분이 내부이기 때 해당부분을 cell로 채우면 vertex에 알맞는 cell들이 생성되게 됩니다.

결과물

![](https://blog.kakaocdn.net/dna/bUA6G7/dJMcajgFgUJ/AAAAAAAAAAAAAAAAAAAAAJzWr_Y7YouLy4xk3qem2oxsjkQn8F6CnDL62nJKIgz8/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=mNGDtNj4PROtwSfg3ZNe2%2BKQ3SE%3D)

![](https://blog.kakaocdn.net/dna/dADLqd/dJMcaiviidn/AAAAAAAAAAAAAAAAAAAAANanj2ZMzVLivQqYax8wHk2H8-4PNppiWXDbd0MGcIdi/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Y%2BTTrr4uaf7QBBH4OEfX5Ii5cd8%3D)![](https://blog.kakaocdn.net/dna/YAWqj/dJMcagdc58U/AAAAAAAAAAAAAAAAAAAAAHxejkXophRU27N9koV4LhWb1H_O-l7_qL1SHphWc1Kh/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=MlIRtxjlin%2BaHOyhUg0GITO5MS0%3D)

잘 생성된다. 굳

![](https://blog.kakaocdn.net/dna/V1san/dJMcafyBXxm/AAAAAAAAAAAAAAAAAAAAAOHd8a08GpSR4BeGuXhiy0TduOSs4mgzxGmcxB4aBDQg/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=En6tL5dyBvDqJzJ2pp%2BzXmEr1HQ%3D)![](https://blog.kakaocdn.net/dna/bcfPaZ/dJMcaihNY9w/AAAAAAAAAAAAAAAAAAAAAHh3g6w3LdYG1PX5VmH8-erZKSpGH6wCmlHHlSzBps7Z/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fTzm09BloJJl%2FfXna9Wq0QLpYOU%3D)



![](https://blog.kakaocdn.net/dna/ce9irl/dJMcabiGGxV/AAAAAAAAAAAAAAAAAAAAAF-eQ27pDrx0lawygKsSgzFxk9LuWz1tDhUXgP_qMV4e/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=YKN1EcRbrKk38FUimMaPxCb%2BnrI%3D)![](https://blog.kakaocdn.net/dna/dg6HrN/dJMcadU3dKL/AAAAAAAAAAAAAAAAAAAAAFNb-DA5tt9j4KNYzjrjDKbZFx6pVvb6nv3raK1bcbJ3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=UaCph%2BG0%2BJ41YJ0ZV1aKKvJfArg%3D)

###