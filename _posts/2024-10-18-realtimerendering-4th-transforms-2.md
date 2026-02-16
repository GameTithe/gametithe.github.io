---
title: "[RealTimeRendering-4th] Transforms (2)"
date: 2024-10-18
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

## **Shearing**

게임에서 왜곡 효과를 줄 때 사용되는 효과이다. 환각제 효과나 오브젝트를 휘게(warp) 만들 때를 예로 들 수 있다.

6개의 기본적인 shearing matrices가 있다.

![](https://blog.kakaocdn.net/dna/w6TwG/btsJ8UvcGsR/AAAAAAAAAAAAAAAAAAAAAIJvopMZZtz-MDOLxqEmDxpXKKqKYXmf0Ad4t1csjsWk/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=TPKt8zuR%2F0in6BfTyNyunjE9d9Y%3D)

![](https://blog.kakaocdn.net/dna/q5LHm/btsJ9bjqpw4/AAAAAAAAAAAAAAAAAAAAAFmNeQqgalDw9j4KWV2MMcc2ZbATNPRC_8VJELmk0tCt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=eDSMp%2Br%2B9ovsyF1mZj%2BE%2FG373zc%3D)

첫번 째 첨자는 변경이 되는 좌표이고, 두번 째 첨자는 shearing 시키는 첨자이다.

그림으로 보면 **x가 변경되는 좌표인데, 그 기준이 z의 변화율인것이다**. z의 값이 커질 때 x의 값도 같이 커지고 있다.

![](https://blog.kakaocdn.net/dna/6nULn/btsKav8MmDf/AAAAAAAAAAAAAAAAAAAAAAyU2gITEENhhyZ3daCDxOnhD1RF9VHW58DB44CfM9mE/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=VTnWsMLW40q0yd0%2FB6Kt6LVbOzU%3D)

그림의 행렬을 이와 같다. 여기서 x(첫번 째 첨자)는 행(row),  z(두번 째 첨자)는 열(cloumn)의 위치를 나타낸다.

그렇기 때문에 0(x),2(z)에 s가 들어가있는 것을 볼 수 있다.

p(px,py,pz)에 Hyz(shearing matrix)를 곱해주면, (px+s\*pz py pz)T이 나오게된다. (z에 따라 x가 변화되는 모습이다.)

Inverse(역함수) of Hxy(s)는 기존 shearing이 반대 방향으로 shearing 되는 것이기 때문에 Hxy(-s)이다.

![](https://blog.kakaocdn.net/dna/r5kHW/btsJ92TBTVP/AAAAAAAAAAAAAAAAAAAAADouB8sbqXKECtz1kn24dk5nOLILd36Oa0k6XYRetxEh/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=FCSoVRVc1YmVTDsKC9c7rjSt1tA%3D)

이렇게 Shearing의 종류를 바꿔볼 수도 있다. 이때 표기법은 z좌표(표기 되지 않은 좌표)가 아래첨자 좌표들을 바꾼다고 보면 된다. 그러니 Hxz(s) \* Hyz(t)로 볼 수도 있다. 어떻게 표기할지는 본인이 정하면 되는 문제이다.그리고 Shearing Matrix의Determinant가 1이면 부피가 보장된다.

## 

## **Concatenation of Transforms**

Concatentaion of Transform(연속되는 변환이라고 생각해도 될 것 같다.)은 순서에 의존적이다.

만약 S(Scale Matrix), R(Rotation Matrix)가 있다면, SR 연산과 RS연산은 다른 결과물을 만들어낸다.

**또한 연속된 Matrices들을 한 개의 Matrix로 묶어서 사용하면 확실하게 성능적으로 효과적이다.**

게임 화면에 수백만개의 정점이 있을 때 모든 정점에 대해서 Scale, Rotate, Translate Matrix 연산 vs 1개의 Matrix 연산 을 생각해보면 체감이 잘 될 것 같다.**C = TRS  로 한 번만 계산하고 C만을 이용해서 수백만개의 vertex에 연산을 해주면 된다.** 여기서 TRS의 순서는 바꿀 수 없다. 하지만 그룹핑은 해도 이상이 없다. (TR)S 를 하던 T(RS) 를 하던 동일하다는 말이다.

## 

## **The Rigid-Body Transform**

오브젝트의 방향과 위치만 바뀌고 형태(shape)에는 영향을 주지 않는 변환이다. 고체의 물건을 잡아오거나, 테이블 위의 펜을 옮기는 등과 같은 상황이라고 보면 된다.

**그러니 Rigid-Body Transform은 Translation과 Rotation만을 포함한 Transform(변환)이다.**

**길이, 각도, handedness를 보존하는 특징이 있다. (handedness : 왼손 좌표계, 오른손 좌표계 등 사용하는 좌표계를 의미한다.)**

![](https://blog.kakaocdn.net/dna/b2wjyO/btsKbFxrMWk/AAAAAAAAAAAAAAAAAAAAAHBUFQAuIjunawIBO7K84DhkF5L4b9cm4pEbykfznmFJ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=P5Bme8ICuPueI1jkQuKM0eEUY8E%3D)

Translation과 Rotation만 포함된 Matix, 이게 rigid-body transform matrix이다.

그리고 X의 역함수는

![](https://blog.kakaocdn.net/dna/cNc0bP/btsKcc9inGx/AAAAAAAAAAAAAAAAAAAAAA_IqisYBI3PY1Jox4VhP2kSABB9wv0SyXXoEm_tHUkC/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=RcwLJnT7Woc9IyHvjrXI7poMLMg%3D)
![](https://blog.kakaocdn.net/dna/6eXMq/btsKbhKvfEb/AAAAAAAAAAAAAAAAAAAAAN5O2pBkSroH_EIobf-VCbLIGULG4ifE6mUzhli_NMAg/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=v1gkMIPy6TZItVAyvfayiu0NvFU%3D)
![](https://blog.kakaocdn.net/dna/bsGEna/btsKb1AaxoC/AAAAAAAAAAAAAAAAAAAAAD1i-ml7fIo66LoDlaezt3fDXsFS4v7FIsdv77jaLIGu/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=DqCNSi2%2FhTOoq47eIo9ihxG0rr8%3D)

이렇게 표현할 수 있다. 여기서 내가 잘 이해가 안된 점은 R이다. R의 역함수는 반대로 회전하는 거니까 T와 같이 R(-t)아닌가? 라고 생각했다. 당연히 그게 맞고 그게 R^T인거다.

![](https://blog.kakaocdn.net/dna/comAfh/btsKblTJITP/AAAAAAAAAAAAAAAAAAAAAIv7sQZCNfb-ldhYzNsHJZG3AwhzlMRgPDzsjghvQlbN/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fx9Egs%2Bb1f7AYAmhJXopGFtg7HA%3D)

R은 orthogonal matrix(직교 행렬)이다. orthohonal matrix의 특징은 M \* M^(T) = I 라는 거다.  
근데 행렬의 특징은 M \* M^(-1) = I 이다. 그러니 M^(-1) = M^(T)가 된다.

그렇기에 R의 역함수는 R^(T) 이다.

정리하면 R의 역함수 =  R의 Transpose = R을 -세타 로 회전 이라고 볼 수 있다.

## 

## **Normal Transform**

Matrix는 points, lines, triangles 등 다른 기하학적 요소들을 변환 시킬 수 있다. 그리고 같은 Matrix로 접선 벡터도 동일하게 (따라다닐 수 있게) 변환할 수 있다. 하지만 **Normal  Vector변환에는 같은 Matrix로 적절하게 변환 할 수 없다.**

Normal Vector을 적절하게 변환하기 위해서는 수반행렬(adjoint)의 전치행렬을 사용해야한다. 수반행렬은 반드시 존재한다는 보장이 되어있지만, normalized를 해줘야한다.

**전통적인 방법으로는 역행렬의 전치행렬(Transpose)을 사용한다.** 역행렬을 만들 수 없는 상황도 있기에 환전한 역행렬을 구할 필요는 없다. 대부분의 변환은 Affine변환이다. 그렇기 때문에 w를 변경하지 않으며, 투영 변환을 수행하지 않는다.(이떄 w값이 변화한다.) 그렇기 때문에 비용이 많이 발생하는 4x4행렬 대신 3x3 Matrix 계산을 대체할 수 있다.

회전 행렬의 전치행렬은 역행렬이다. 그렇기 때문에 회전 행렬만 있을 때는 역행렬의 전치행렬은 두 번의 전치(또는 두 번의 역행렬)과 같은 의미이다. 이렇게 특정한 경우에는 원래의 변환 행렬 자체를 노멀 변환에 직접 사용할 수 있다.

마지막으로, 생성된 노멀을 완전히 재정규화하는 것(renormalized)이 항상 필요하지는 않는다. 만약  Translation과 Rotation Matrix만 존재한다면 재정규화는 할 필요가 없다.

만약 uniform scaling 연산이 포함되어 있다면 전체 scale factor를 이용해서 normalize를 해줄 수 있다.

 (5배를 했으면 1/5배를 해준다는 말)

**앞에서 말했던 것 같이 normal vector를 구할 때 좌측 상단의 3x3 Matrix만 사용해서 구할 수 있다. 단, 미리 noramlize를 해주고 구하자.( scale factor로 미리 나누고 시작하면 된다. )**

normal transform은 transform 연산을 한 이후에는 문제가 발생하지 않는다.

## 

## **Computation of Inverse**

역행렬은 많은 경우에 필요하다. (앞뒤로 변경할 때 등)

다음 세 가지 방법 중 하나를 사용하여 행렬의 역행렬을 계산할 수 있다.

1. **single matrix나 간단한 변환들이 순서대로 이루어진 행렬의 경우**

역행렬은 매개변수를  **뒤집고** 행렬 순서를 반대로 하여 쉽게 계산할 수 있습니다.

M = T(theta)R(alpha) 라면, M^-1 = R(-alpha)T(-theta)이다.

2. **직교 행렬의 역행렬**

행렬이 orthogonal matrix(직교 행렬)인 경우에 역행렬은  전치행렬이다. M^-1 = M^T

모든 회전 변환의 sequence는 결과적으로 회전이며, 따라서 어떤 회전 변환이든 직교행렬로 볼 수 있다.

3. **일반 행렬의 역행렬**

정보가 없다면

1. 수반행렬(adjoint)

2. 크래머 규칙(Cramer's rule)

3. LU 분해

4. 가우스 소거법

일반적으로 **수반행렬 방법과 크래머 규칙**이 사용된다.