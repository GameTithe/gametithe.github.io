---
title: "[GameEngineArchitecture] Points & Vector"
date: 2025-07-30
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

게임은 실시간으로 컴퓨터에서 시뮬레이션되는 가상 세계의 수학적 모델이다.

따라서 수학은 게임 산업에서 우리가 하는 모든 일에 깊숙이 스며들어 있다. 게임 프로그래머는 삼각함수, 대수학, 통계학, 미적분학 등 사실상 거의 모든 수학 분야를 활용한다.

그러나 게임 프로그래머로서 여러분이 가장 많이 다루게 될 수학은 **3D 벡터와 행렬 (3차원 선형대수학)** 이다.

이 하나의 수학 분야조차 매우 폭넓고 깊이가 있어서, 단 한 개의 장에서 그것을 깊이 있게 다루는 것은 불가능하다.

여기서는 일반적인 게임 프로그래머에게 필요한 수학적인 도구들을 소개하는데 집중할 것이다. 그 과정에서 혼란스러운 개념들과 규칙들을 머릿속에서 정리하는 데 도움이 될 만한 몇 가지 팁과 요령도 제공할 예정이다.

3D 게임 수학을 깊이 있게 다루는 훌륭한 참고서로는 Eric Lengyel의 책 (Mathematics for 3D Game Programming and Computer Graphics)을 강력히 추천한다. 실시간 충돌 감지에 관한 Christer Ericson의 책(Real-Time Collision Detection)의 3장 또한 훌륭한 자료다.

### 

### **Solving 3D Problems in 2D**

**우리가 다음 장에서 배우게 될 많은 수학적 연산들은 2D와 3D에서 동일하게 잘 작동한다.**  
3D 벡터 문제를 2D로 생각하고 그림을 그려서 풀 수 있다는 뜻이기에 굉장히 좋은 소식이다.(2D는 훨씬 더 다루기 쉽다!)

하지만 **2D와 3D의 동등성은 항상 성립하는 것은 아니다.**  
예를 들어, **외적(Cross Product)은 3차원에서만 정의되고,** 어떤 문제들은 세 개의 차원을 모두 고려해야만 의미가 있다.

그럼에도 불구하고, **문제를 2차원 버전으로 먼저 생각해보는 것은 거의 항상 도움이 된다.**

이 책에서는 2D와 3D의 구분이 중요하지 않은 경우에는 **2차원 도표**를 사용할 것이다.

### 

### **Point and Vector**

현대 3D 게임의 대다수는 가상 세계 안의 3차원 객체들로 구성되어 있다.  
게임 엔진은 이러한 모든 객체의 위치, 방향, 크기를 추적하고, 게임 세계에서 그것들을 애니메이션화하고, **스크린 공간으로 변환해서 화면에 렌더링**해야 한다.

**게임에서는 3D 객체들이 거의 항상 삼각형들로 구성되며,** **그 정점(vertex) 들은 점(Point)으로 표현된다.**  
따라서 전체 객체를 게임 엔진에서 표현하는 방법을 배우기 전에, 우선 **점(Point)**과 **벡터(Vector)** 를 살펴보자.

### 

### **Point & Cartesisan Coordinate**

기술적으로 말하면, **점(Point)** **은 n차원 공간에서의 위치를 뜻한다.**

**데카르트 좌표계(Cartesian Coordinate System) 는 게임 프로그래머가 가장 일반적으로 사용하는 좌표계다.**  
이 좌표계는 서로 수직인 2개 또는 3개의 축을 사용하여 2D 또는 3D 공간상의 위치를 지정한다.

**원통 좌표계 (Cylindrical Coordinates)**  
이 시스템은 수직 높이(height) 축 h, 중심으로부터 바깥쪽으로 향하는 반지름 축 r, 그리고 각도 θ(세타)를 사용한다.

**구면 좌표계 (Spherical Coordinates)**  
이 시스템은 **상승각 φ(phi)**, **방향각 θ(theta)**, 그리고 **거리 r** 을 사용한다.

![](https://blog.kakaocdn.net/dna/bbB53m/btsPDV8i5xC/AAAAAAAAAAAAAAAAAAAAAOYaK1Br3TZ3K1g5xVMT3R1VWFQRTortqot1jGWKI8d7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=g5bvDd9AvKe6evwSLQkKPPhrU78%3D)![](https://blog.kakaocdn.net/dna/7yXOI/btsPB0Da542/AAAAAAAAAAAAAAAAAAAAACPtJPeOIQwmViiUiHu36VYCKPHfbpjFVC6Wjjzy3vBz/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Km5IRs2%2F7Dt8a1ExgCgGj%2B3HjaA%3D)![](https://blog.kakaocdn.net/dna/csjLu4/btsPDHWHLly/AAAAAAAAAAAAAAAAAAAAAOvwywWWuQAtV95HFMX5Z3mmelG_WxvbXPgop8dtaf09/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=SCvNB%2Fk0YveIMI9mmxP3KgyZ7Pg%3D)

데카르트 좌표계는 게임 프로그래밍에서 가장 널리 사용되는 시스템이긴하지만, 문제에 가장 잘 맞는 좌표계를 선택하는 것이 중요하다.

나는 게임을 제작할 때 전리품이 몸 주위를 **나선형(spiral)** 으로 회전하며 점점 가까워지다가 사라지도록 만들고 싶었다.

그래서 전리품의 위치를 캐릭터 현재 위치를 기준으로 한 **원통 좌표계**로 표현했다.  
그리고 전리품에 대해 다음과 같은 애니메이션을 적용했다:

1. 일정한 **각속도 θ**

2. 반지름 축 r을 따라 **안쪽으로 향하는 작은 선형 속도**

3. 수직축 h를 따라 **천천히 상승하는 속도**

이처럼 단순한 애니메이션이었지만 아주 그럴듯하게 보였으며,  
데카르트 좌표계보다 원통 좌표계를 사용하는 편이 훨씬 구현하기 쉬웠다.

### 

### **왼손 좌표계 vs 오른속 좌표계**

3차원 데카르트 좌표계에서는, 서로 수직인 세 축을 배열할 때 **두 가지 선택지로**

**오른손 좌표계(Right-Handed, RH)** 와 **왼손 좌표계(Left-Handed, LH)가 있다.**

![](https://blog.kakaocdn.net/dna/kWBHQ/btsPDVgaOXO/AAAAAAAAAAAAAAAAAAAAALPEmS8Cj2Ig0b4M2QEQctB-VsPnrLc6L6uszuIb98FN/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=u2OmlAJFi1iVzN7r41i1XIxWaHM%3D)

오른손 좌표계에서는, **엄지를 양의 z축 방향으로 뻗고 손가락을 z축을 따라 감아 쥐었을 때**,  
손가락은 **x축에서 y축 방향으로** 감긴다.

왼손 좌표계에서는, **왼손을** 똑같이 사용하면 같은 관계가 성립한다.

**유일한 차이점은**, **세 축 중 하나의 방향이 반대라는 것**뿐이다.

좌표계를 왼손 좌표계에서 오른손 좌표계로, 또는 그 반대로 **변환하는 것은 아주 쉽다**.  
세 축 중 **하나의 방향만 반대로 뒤집고**, 나머지 두 축은 그대로 두면 된다.

중요한 점은, **수학적인 규칙 자체는 좌표계에 따라 바뀌지 않는다**는 것이다.

왼손/오른손 좌표계에 대한 규약은 **시각화에만 적용되는 것이지, 수학적 본질에는 영향을 주지 않는다.**  
(다만 실제 시뮬레이션에서 **외적(Cross Product)** 을 다룰 때는 방향성이 중요해지는데,  
그 이유는 외적 결과가 **벡터(vector)** 가 아니라 **의사벡터(pseudovector)** 이기 때문이다.

**3D 그래픽스 프로그래머**들은 일반적으로 **왼손 좌표계**를 사용한다.  
이때 축 배치는 다음과 같다

y축: 위쪽

x축: 오른쪽

z축: **사용자를 기준으로 멀어지는 방향** (즉, **가상 카메라가 향하는 방향**)

이 좌표계를 사용하면, **z값이 커질수록 장면 속으로 깊게 들어간다는 의미**가 된다.  
즉, **카메라로부터 점점 멀어지는 방향**이 된다.(**깊이 정보로 가려짐(z-버퍼링, depth occlusion)** 을 처리할 때 정확히 필요한 좌표 체계이다.)

## 

## **Vectors**

**벡터(Vector)**란, **크기(magnitude)** 와 **방향(direction)** 을 모두 가지는 n차원 공간 속의 양(quantitiy)이다.

이와는 달리, **스칼라(Scalar)**는 **크기만을 가지는 실수값이고, 방향은 없다.**

보통 스칼라는 italics(ex. v)로 표기하고, 벡터는 **볼드체**(ex. **v**)로 표기한다.

3차원 벡터는 점과 마찬가지로 **세 개의 스칼라 (x, y, z)** 로 표현될 수 있다.  
하지만 **점(point)** 과 **벡터(vector)** 의 차이는 존재한다.

기술적으로 **벡터는 어떤 기준point 으로부터의 오프셋(offset)** 이다.  
**즉, 벡터는 공간 어디로든 자유롭게 이동 가능하며, 크기와 방향만 보존되면 그 자체로 동일한 벡터다.**

벡터는 **점(Point)** 을 표현할 수도 있다.  
이 경우 벡터의 **꼬리를 좌표계의 원점(origin)** 에 고정시키면 된다.  
이런 벡터를 **위치 벡터(position vector)** 또는 **반지름 벡터(radius vector)** 라고 한다.

즉, 벡터 (x, y, z)를 위치 벡터로 해석할 수도 있고, 방향 벡터로 해석할 수도 있다.

단, **위치 벡터는 항상 원점에서 시작된다는 제약이 있다는 점을 기억하자.**

이러한 이유로, 수학적으로 **점과 벡터는 약간 다르게 취급된다.**

정리하면

**점(Point)** 은 절대적이고,

**벡터(Vector)** 는 상대적이다.

이후 설명할 **동차 좌표(homogeneous coordinate)** 변환 시 방향과 점을 구분하지 않으면,  
**행렬 연산에서 버그가 발생할 수 있다.**

## 

## **Cartesian Basis Vectors**

세 개의 **서로 수직이고 길이가 1인 단위 벡터**(orthogonal unit vectors => orthonormal (orthogonal + normlized) )를 정의하는 것은 유용할 때가 있다. 이 단위 벡터들은 데카르트(Cartesian) 좌표계의 세 주요 축에 각각 대응하며,

x축 방향의 단위 벡터는 보통 **i**,

y축 방향은 **j**,

z축 방향은 **k**로 불린다.

이 **i, j, k 벡터**들을 **데카르트 기저 벡터(Cartesian basis vectors)** 라고 부르기도 한다.

모든 점이나 벡터는 이들 **단위 기저 벡터에 실수(scalar)를 곱한 값의 합**으로 표현할 수 있다.

![](https://blog.kakaocdn.net/dna/pFkKV/btsPDJNKikV/AAAAAAAAAAAAAAAAAAAAAAvV-OXbrmD5n4YnCcFtZhZDqJZRgz8o3ITm_zrwC7XY/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=TSg5XsUL%2BplqSzkcyODsYOmtN0w%3D)

## 

## **Vector Operations**

스칼라에 대해 수행할 수 있는 대부분의 수학 연산들은 벡터에도 적용할 수 있다.  
또한, 벡터에만 적용되는 **특수한 연산들**도 존재한다.

### 

### **Multiplication by a Scalar**

벡터 **a**에 대해 **스칼라 s를 곱한다**는 것은,  
벡터 **a**의 **각 성분을 s배** 하는 것을 의미한다.

![](https://blog.kakaocdn.net/dna/bB0xYx/btsPDGwMBlr/AAAAAAAAAAAAAAAAAAAAAGV16otzy3DUaQzNQxso7se0MnOl0Gq3tr68hUPwdhlU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GyzpQSYFNbPdLCFQbpCFa%2FHsRvc%3D)

스칼라 곱은 벡터의 **방향은 유지하면서 크기를 변화시킨다.**

Scale Factor가 각 축마다 서로 다를 수도 있다. 이런 경우를 비균일 스케일(non-uniform scale) 이라고 하며,  
해당 연산은 스케일 벡터 s 와 대상 벡터의 성분별 곱(Component-wise Product) 으로 표현된다. (Hadamard product (하다마드 곱) 게임 산업에서는 이 연산이 거의 사용되지 않는다.

**스케일 벡터 s**는 본질적으로 3×3 **대각 스케일 행렬(diagonal scaling matrix)** 을 **간결하게 표현한 것**일 뿐이다.  
따라서 식 아래와 같은 행렬 곱셈 형태로도 다시 쓸 수 있다

![](https://blog.kakaocdn.net/dna/cdSogC/btsPBokevTx/AAAAAAAAAAAAAAAAAAAAAH3wVL0Ae8j2awokUws-jTkqVU_pZgn20KIhzOss1upn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=5k4X62OHV8sTuqtEBrv3L%2BAhxI0%3D)

### **Addition and Subtraction**

두 벡터 **a**와 **b**를 더한다는 것은, 각 성분끼리 더한 새로운 벡터를 만드는 것이다

```
a + b = (ax + bx, ay + by, az + bz)
```

벡터의 뺄셈 a - b는 b의 방향을 반대로 뒤집고, 더하는 것과 같다

```
a - b = (ax - bx, ay - by, az - bz)
```

![](https://blog.kakaocdn.net/dna/dPpTMx/btsPBnFBEW2/AAAAAAAAAAAAAAAAAAAAAB6wJj-cv9yFdumILoIctZpZcUFXWP7jQ9RrDL5MRRfi/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FSYt2x5Z%2FkXh83KI8wn0HLhchz4%3D)

#### 

#### 

**방향 벡터끼리는 자유롭게 덧셈/뺄셈**이 가능하다.  
하지만, **점(Point)끼리는 수학적으로 덧셈이 정의되지 않는다.**

벡터+ 벡터 = 벡터

벡터  – 벡터 = 벡터

점 + 벡터 = 점

점 – 점 = 벡터

점 + 점 = 의미 없음 (nonsence)

**(외울게 아니라 점: 1 벡터: 0 로 생각하면 편하다.** 왜 그런지는 아마 설명해주지 않을까..싶슴다.)

### 

### **Magnitude**

벡터의 **크기(magnitude)** 는, 그 벡터의 길이를 나타내는 **스칼라 값**이다.  
2D나 3D 공간에서 **직접 측정될 수 있는 길이**다. 크기는 벡터 기호의 **양쪽에 세로 막대(| |)** 를 붙여서 나타낸다:

```
|a|
```

크기는 **피타고라스의 정리**를 통해 계산할 수 있다.

```
|a| = sqrt(ax + ay^2 + az^2)
```

## 

## **Vector Operations in Action**

지금까지 배운 벡터 연산만으로도 현실의 게임 문제들을 충분히 해결할 수 있다.  
문제를 풀기 위해 우리는 **덧셈, 뺄셈, 스케일링, 크기 계산** 등의 연산을 사용하여, 이미 알고 있는 정보로부터 **새로운 데이터**를 만들 수 있다.

예를 들어, AI 캐릭터의 **현재 위치 벡터** P1와 **현재 속도 벡터** v를 알고 있다고 하자.

이때, 프레임 간 시간 간격 delta Time만큼 시간이 지났을 때,  
다음 프레임에서의 위치 P2는 아래와 같이 계산할 수 있다

```
P2 = P1 + v * delatTime
```

이 식은 **Explicit Euler Integration**이라 불리는 공식이다.

또 다른 예로, 두 개의 구가 서로 겹쳐져 있는지를 판별한다고 하자.

각 구의 중심점을 C1, C2라고 할 때,

이 둘 사이의 **방향 벡터**는 다음과 같이 구할 수 있다:

```
d = C2 - C1
```

이 벡터의 **크기(|d|)** 는 두 구의 중심 간의 거리이다.  
만약 이 거리가 두 반지름의 합보다 작다면, 두 구는 **겹치고 있는 것이다**.

즉, 다음 조건을 체크하면 된다

```
if (|d| < r1 + r2)
{
	//충돌입니두
}
```

![](https://blog.kakaocdn.net/dna/tQ6CN/btsPB4yS0nb/AAAAAAAAAAAAAAAAAAAAACvqhMK79z6EMGhBwz-8wGs9VJ03MXrOAZll8vi40K3H/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=U6Ckq%2FDRKMpjf%2FCX6%2BmWxhbUXfk%3D)

다만, 대부분의 컴퓨터에서 **제곱근 연산은 비용이 크다.**  
따라서 게임 프로그래머는 **가능한 경우 항상 제곱 크기(squared magnitude)** 를 사용하는 습관을 들여야 한다.

벡터 a의 제곱 크기는 다음과 같다

![](https://blog.kakaocdn.net/dna/b2nU4u/btsPBF0qono/AAAAAAAAAAAAAAAAAAAAAJObu4jsrbkZkglICKWZ1KsZECthzS8aLWj9IqR7IM11/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=It4rwO5GDch6dOE7HIGxqQZDcX4%3D)

제곱 크기를 사용할 수 있는 경우는

1. 두 벡터 중 **어느 쪽이 더 긴지 비교할 때**

2. 어떤 벡터의 크기를 **다른 제곱된 스칼라 값과 비교할 때**

즉, 위의 구 충돌 테스트에서 우리는 다음과 같이 계산해야 한다:

```
|d|^2 < (r1 + r2)^2
```

고성능 소프트웨어를 작성할 때에는 **꼭 필요한 경우가 아니라면 제곱근을 절대 사용하지 말자.**

## **Normalization and Unit Vectors**

**단위 벡터(Unit Vector)** 는 **크기(길이)가 1인 벡터**이다.  
단위 벡터는 3D 수학과 게임 프로그래밍에서 매우 유용하다.

길이가 |v|인 임의의 벡터 v가 주어졌을 때, 이 벡터와 같은 방향을 가지면서 **길이가 1인 벡터 u** 를 얻고 싶다면,

벡터 v를 그 **크기의 역수로 곱해주면 된다.**

이 과정을 **정규화(Normalization)** 라고 부른다.

![](https://blog.kakaocdn.net/dna/bmVIrg/btsPDsepWN5/AAAAAAAAAAAAAAAAAAAAALr6c2GCGNiWBKLn9NQp6F2u6TtwBDyzvC5NfAtW96gb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=oh0oijNkREZJcbiTk6Y3GlT%2FajY%3D)

## **Normal Vectors**

어떤 벡터가 **어떤 표면에 수직(perpendicular)** 하다면,  
그 벡터는 그 **표면의 법선(normal)** 이라고 말한다.

**법선 벡터(normal vector)** 는 게임과 컴퓨터 그래픽스에서 매우 유용하다.  
아래와 같은 예시가 있다

1. 평면은 한 점과 하나의 법선 벡터로 정의할 수 있다.

2. 3D 그래픽스에서는 조명 계산 시 사용 ( 우리에게 보여지는 조명의 밝기가 normal 방향에 따라 다름 )

법선 벡터는 보통 **단위 벡터**로 쓰이지만, **반드시 단위 벡터일 필요는 없다.**

여기서 중요한 점은, **정규화(normalization)** 와 **법선 벡터(normal vector)** 라는 용어를 혼동하지 않는 것이다.

**정규화된 벡터(normalized vector)**  
크기가 1인 어떤 벡터

**법선 벡터(normal vector)**  
어떤 표면에 수직인 벡터 (단위 벡터일 수도 있고 아닐 수도 있음)

## **Dot Product(내적)과 Projection(투영)**

벡터는 서로 곱할 수 있지만, **스칼라와 달리 곱의 종류가 다양**하다.  
게임 프로그래밍에서는 아래 **두 가지 곱**이 가장 자주 사용된다.

**1. 내적(dot product):** 스칼라 곱, 또는 내적(inner product)

**2. 외적(cross produt):** 벡터 곱, 또는 외적(outer product)

### 

### **Dot Product**

두 벡터의 내적은 **스칼라(scalar)** 를 반환하며, 두 벡터의 **각 성분을 곱한 후 모두 더하여** 계산한다:

![](https://blog.kakaocdn.net/dna/m4fIL/btsPB8urHFf/AAAAAAAAAAAAAAAAAAAAAP1Js-arq8rqaltqAMc-46n099ae6xOLWjbKXQhOAJiC/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Y7MeS9GfpDCMJa1RtAburz3qbk4%3D)

또한 내적은 다음과 같은 삼각 함수 표현으로도 쓸 수 있다:

![](https://blog.kakaocdn.net/dna/84Uma/btsPDWGaA4W/AAAAAAAAAAAAAAAAAAAAAMyVCAFO_iltlUPOYHJ6ZPy8xjqaGwWx4oD1rnypF7kS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ulZ65HaSxnJje7FrM37M2P9Ejdo%3D)

여기서 θ는 두 벡터 사이의 각도이다.

내적의 성질

**교환법칙,** **분배법칙**이 성립한다:

![](https://blog.kakaocdn.net/dna/bncFaQ/btsPDsMhfc2/AAAAAAAAAAAAAAAAAAAAAFyytvh0RGFofRc70_jE4UiSOHp7uD2HDY1xJGaEWpbH/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=n8yXE2XKaNS2%2F4iR5sjEKMdHahY%3D)

**스칼라 곱과의 결합도 가능하다**

![](https://blog.kakaocdn.net/dna/kFOnU/btsPBK1EgV0/AAAAAAAAAAAAAAAAAAAAADRhZnhqTu8e3uXVZwyIBm54SotaH1wp71rqJ6NSgqzr/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xlZCAfj0Nk3MbSgPe%2FN8O6NXg7I%3D)

## **Vector Projection**

벡터 u가 **단위 벡터**(즉, |u| = 1)라면,  
**dot(a, u)**은 벡터 a가 **벡터 u의 방향을 갖는 무한 직선 위에 투영된 길이**를 나타낸다.

![](https://blog.kakaocdn.net/dna/d6gkfu/btsPDWGqwNg/AAAAAAAAAAAAAAAAAAAAAFsOQcrKDVG2u8Yr54D2Oy_NeW7lfhP-wd-FZR3N4taP/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=eExYO5zr7gD4BMaSfYaBdWFVI0I%3D)

이러한 투영 개념은 **2D, 3D 모두에서 동일하게 적용**되며,  
**3차원 문제 해결에 매우 널리 유용하게 사용**된다.

(최근에 충격량 계산할 일이 있었는데, 그 때도 이 개념을 사용했다.

s1(구), s2(구)가 충돌할 때, 충격량으로 속도를 바꿔주는데 충격량을 normal vector로 투영하고 속도를 변경해주었다.)

### 

### **Magnitude as a Dot Product**

벡터의 **제곱된 크기(squared magnitude)**는 **자기 자신과 내적**하면 얻을 수 있다

![](https://blog.kakaocdn.net/dna/uUHZZ/btsPC6vX5bq/AAAAAAAAAAAAAAAAAAAAAJyxQtXsV3V1UFPKBXUI2C-9ydl10yJ_Vy4EVTfBD8wX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=sN%2Fedyghu6WYYfxOFEwdgDllm3Q%3D)

그 후, **제곱근**을 취하면 **벡터의 크기**를 구할 수 있다.

![](https://blog.kakaocdn.net/dna/bHF8nm/btsPB191GDF/AAAAAAAAAAAAAAAAAAAAACqyJRSaroUx4ZamtthEmwmEbkxFmfCybGlYMuiEWDmN/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fNcC%2FNxOTAFULe5a5dxgF5jp2H0%3D)

이것이 가능한 이유는, 두 벡터가 동일할 경우  
**벡터 간 각도 θ가 0도이며 cos(0) = 1**이기 때문이다

### 

### **Dot Product Tests**

**내적(dot product)** 은 두 벡터가 다음 조건을 만족하는지를 판별할 때 매우 유용하다:

**1. 일직선(collinear)인지**

**2. 수직(perpendicular)인지**

**3. 같은 방향인지**

**4. 반대 방향인지**

아래는 게임 프로그래머가 자주 사용하는 내적 테스트들이다.

![](https://blog.kakaocdn.net/dna/L71N8/btsPCVanEhG/AAAAAAAAAAAAAAAAAAAAAEHsyhkM5WO0j9mHMELr6f-SZn3AO3iGEYx5ZSyKgmrg/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=0L7insXcD64MyX4HrEPT6P9Ih8I%3D)

**아래 a,b  vector는 모두 단위 벡터이다.**

**일직선 (Collinear)**

dot(a, b) = |a||b| => 두 벡터 사이 각도 = 0도 => 1

**반대 방향의 일직선 (Collinear but opposite)**  
dot(a, b) = -|a||b| => 두 벡터 사이 각도 = 180도 =>  -1

**수직 (Perpendicular)**  
dot(a, b) =>90도 => 0

**같은 방향 (Same Direction)**

dot(a, b) => 각도 < 90도 => 양수

**반대 방향 (Opposite Direction)**  
dot(a, b) < 0 => 각도 > 90도 => 음수

## 

## **Some Other Applications of the Dot Product**

내적은 게임 프로그래밍에서 매우 다양한 용도로 활용된다.  
아래는 대표적인 예시들이다.

### 

### 적이 플레이어의 앞에 있는지 뒤에 있는지 판별하기

플레이어 캐릭터의 위치를 P1  
적(enemy)의 위치를 E라고 하자.

두 위치 벡터의 차  
v = E - P  => **플레이어에서 적까지의 벡터**

플레이어가 **바라보는 방향 벡터**를 f라고 하면,

**(모델 - 월드 행렬(model-to-world matrix)** 로부터 추출할 수 있다.)

이제 dot(v, f) 를 계산하면 다음을 판단할 수 있다.

d = dot(v, f)일 때

1. d > 0 => 적이 **플레이어 앞에 있음**

2. d < 0 => 적이 **플레이어 뒤에 있음**

### 

### **점이 어떤 평면보다 위에 있는지 아래에 있는지 판단하기**

이건 예를 들어 **달 착륙 게임(moon-landing game)** 같은 데서 유용할 수 있다.

![](https://blog.kakaocdn.net/dna/bE34Mt/btsPB884B8t/AAAAAAAAAAAAAAAAAAAAAMOewc5LdjkQjmAgaQHLpqsLgzTcqqbPxee0dpL0gO3X/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=CdQjaOIPXliNhfTvJdj1CKiLIbM%3D)

평면은 두 가지로 정의된다

1. 평면 위의 한 점 Q

2. 평면에 수직인 **단위 벡터 n** (법선 벡터)

![](https://blog.kakaocdn.net/dna/cD1jcd/btsPDoDedxX/AAAAAAAAAAAAAAAAAAAAADVR4mBj-6XluCN0-QU69E_t8dzJfXyvY5HA6bkHbHFt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1a5s1046LZmYV1c2o2ESpNU3WdQ%3D)

평면 위의 점 Q에서 특정한 점 P로 향하는 벡터 v를 구한다. =>  v = ( P - Q)

이제 v를 **법선 벡터 n 방향으로 투영**하면, 이 값은 곧 **점 P가 평면 위에서 떨어진 수직 거리(h)** 가 된다.

## 

## **Cross Product(외적)**

**외적(Cross Product)** 은 **벡터 곱** 또는 **벡터 외적**이라고도 불리며, 두 벡터를 곱했을 때 **두 벡터 모두에 수직인 새로운 벡터**를 반환한다.

**외적 연산은 오직 3차원 공간에서만 정의된다.**

![](https://blog.kakaocdn.net/dna/bbBw30/btsPDtErXgd/AAAAAAAAAAAAAAAAAAAAAG4NmL-AwVr_eYCtMkE3xe9DO85oGhLTO2Vl9Cl3B0I_/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ixvqW4qm%2F3B87wPj1SDykJw%2BiyQ%3D)

벡터 a, b의 외적 계산은 아래와 같다.

![](https://blog.kakaocdn.net/dna/zAsnR/btsPBHYe23D/AAAAAAAAAAAAAAAAAAAAAD9tIvpG9T2JHYEsGz7F1MTes3HREHC_HwBiUp-3X_WL/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=trlqeKOTneUSsL1%2FijTsmASnkNk%3D)

### 

### **Magnitude of the Cross Product(외적의 크기)**

외적 벡터의 **크기**는,  
두 벡터의 크기와 그 사이의 각도 θ의 **sin**값을 곱한 것과 같다.

![](https://blog.kakaocdn.net/dna/BgNUG/btsPB4r8HR6/AAAAAAAAAAAAAAAAAAAAAMbz1ZtoWGvNUOJCT4ofn6467TdeWNmj5lEzWw-coWLu/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GF7uq1F9itx4qWgwrLNZyeHHVqI%3D)

(내적과 매우 유사하지만, **cos** 대신 **sin**을 사용한다.)

외적의 크기는,  
벡터 a, b를 두 변으로 하는 **평행사변형(parallelogram)** 의 **넓이**와 같다.

![](https://blog.kakaocdn.net/dna/cvjqIw/btsPD09Dk54/AAAAAAAAAAAAAAAAAAAAAOUtfAMRxUaBK2nuAFgU2IsyrXhpEgeE3uleVlV05s48/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Co5qKjnoimG7duEC1CEIEW4N4Nw%3D)

따라서 세 꼭짓점이 V₁, V₂, V₃로 주어진 **삼각형의 넓이**는 다음과 같이 계산할 수 있다:

![](https://blog.kakaocdn.net/dna/dKkK8X/btsPBh6K2Eg/AAAAAAAAAAAAAAAAAAAAAEc-7Mp-OTyP2UBcxM2FBqprPNhRchCvT6KnVPrqk3d1/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=YzNhv%2BTZsYQSISDGcepeRDlZUFk%3D)

즉, 삼각형의 두 변을 외적하고, 그 크기를 절반으로 나누면 된다.

### 

### **Direction of the Cross Product(외적의 방향)**

**오른손 좌표계(Right-Handed Coordinate System)** 에서는  
**오른손 법칙(Right-Hand Rule)** 을 사용해 외적의 방향을 판단한다.

손가락을 벡터 a에서 b로 회전시키는 방향으로 감아쥐면,

**엄지가 외적 a × b의 방향**을 가리킨다.

반대로, **왼손 좌표계(Left-Handed Coordinate System)** 를 사용할 경우, **왼손 법칙(Left-Hand Rule)** 을 따라야 하며, 따라서 **외적의 방향도 좌표계에 따라 바뀐다.**

처음에는 다소 이상하게 느껴질 수 있다.  
하지만 중요한 것은, **좌표계의 손잡이(handedness)** 는 **수학 계산 자체에는 영향을 주지 않으며**,  
**단지 시각적 해석** 즉, 숫자들이 3D 공간에서 어떻게 보이는지를 **우리의 머릿속 이미지**만 바꾸는 것이다.

예를 들어, 오른손 좌표계를 왼손 좌표계로 전환할 때

모든 **점**과 **벡터**의 수치는 그대로 유지되지만, **축 중 하나(z축 등)** 의 방향만 반전된다.

이로 인해 우리가 보는 모든 3D 시각화는 **그 축을 기준으로 대칭(미러링)** 된다.

결론적으로, **너무 깊이 걱정할 필요는 없다.** 그저 **오른손 좌표계에서는 오른손 법칙**, **왼손 좌표계에서는 왼손 법칙**을 사용해 **외적의 방향을 시각화**하면 된다.

### 

### **Properties of the Cross Product (외적의 성질)**

**비교환성 (Not Commutative)**

![](https://blog.kakaocdn.net/dna/XW3Ai/btsPCJOEG2f/AAAAAAAAAAAAAAAAAAAAAKuwK4QucE_Eul4QGUbA5rUXf96s89Ial40w3WjyrIXW/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=oFjqhkGgd%2F8HJPBcusWanW7a1JI%3D)

**반교환성 (Anti-Commutative)**

![](https://blog.kakaocdn.net/dna/cMM6xb/btsPAZyjsq1/AAAAAAAAAAAAAAAAAAAAAN7M4k4BzeWMGZAl6w3oV6F3CtnyHQ154WC8mCJIH7Lf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=WpsfMNlPRFiBdQS9TJZibdvZ0F4%3D)

**분배법칙 (Distributive over Addition)**

![](https://blog.kakaocdn.net/dna/uSLgL/btsPC5w6YRF/AAAAAAAAAAAAAAAAAAAAAF5zBgVrO-Uof-kWwCupD47OZZk4GNIzmOGdbkhKqepb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nhXNE6WOAK%2FbQgA0U0NyS%2FTCdss%3D)

**스칼라 곱과의 결합**

![](https://blog.kakaocdn.net/dna/d7qsgN/btsPCLlmzD5/AAAAAAAAAAAAAAAAAAAAAJc4O7CEHGTZWNgPj1rM4iLsuiZ6O3VptLuzsX6y0CCI/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=jE5Gmx8vAzr6PT8ICGVZ6XY7agc%3D)

### 

기본 단위 벡터 i, j, k의 외적은 다음과 같다

![](https://blog.kakaocdn.net/dna/31H5w/btsPDMX5XqU/AAAAAAAAAAAAAAAAAAAAALonPgnLSnW9qLi_frqdcJ5btsSY1OuVFPix5gMQ8WTK/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xOYHXeEoJSwOZl6AWfJPXvnYKU8%3D)

이 세 외적 공식은 **각 카르테시안 축을 기준으로 한 양의 방향(X =>Y => Z 순을 의미) 회전**을 정의한다.

**z축 기준 회전:** x => y 방향

**x축 기준 회전:** y => z 방향

**y축 기준 회전:** z => x 방향

특히 **y축 회전**은 알파벳 순서상 역방향(z  => x)임을 주의하자.  
이것은 이후 **y축 회전 행렬이 x, z 회전 행렬과 비교해 반대로 보이는 이유**를 설명하는 힌트가 된다.

## 

## **The Cross Product in Action**

**외적(Cross Product)** 은 게임에서 다양한 용도로 사용된다.  
가장 흔한 용도 중 하나는, **두 벡터에 모두 수직인 벡터를 구하는 것**이다.

어떤 오브젝트의 **로컬 단위 기저 벡터들** (i\_local, j\_local, k\_local)을 알고 있다면,  
그 오브젝트의 **회전 상태(orientation)** 를 나타내는 행렬을 쉽게 만들 수 있다.

이제, 만약 우리가 k\_local 벡터만 알고 있다고 가정하자. (객체가 바라보고 있는 방향)

이 오브젝트가 k\_local 축을 기준으로 **회전(roll)** 하지 않았다고 가정하면,  
 i\_local 벡터는 k\_local 과 j\_world의 cross product로 구할 수 있다.

**로컬 x축(i\_local) 계산**

```
i_local = normalize(j_world × k_local)
```

**로컬 y축(j\_local) 계산**

```
j_local = k_local × i_local
```

이와 거의 유사한 방식으로,  
**삼각형이나 평면의 법선 벡터(normal vector)** 도 계산할 수 있다.

평면 위의 세 점 P₁, P₂, P₃가 주어졌을 때

```
n = normalize((P₂ - P₁) × (P₃ - P₁))
```

외적은 **물리 시뮬레이션**에서도 사용된다.  
예를 들어, 어떤 오브젝트에 **힘(force)** 이 **중심이 아닌 지점에 작용할 때**,  
이 힘은 회전 운동을 유발한다.

이 회전력을 **토크(torque)** 라고 하며, 아래처럼 계산된다

F: 힘

r: 질량 중심으로부터 힘이 작용된 점까지의 벡터

```
N = r × F
```

## 

## Pseudovectors and Exterior Algebra(의사벡터와 외부 대수)

**외적은 진짜 벡터를 반환하지 않는다.**  
사실 외적은 **의사벡터(pseudovector)** 라는 특수한 수학 객체를 생성한다.

벡터와 의사벡터의 차이는 꽤 **미묘**하다.  
사실상 **게임 프로그래밍에서 자주 쓰이는 변환들인 이동(translation), 회전(rotation), 스케일(scaling)**에서는  
둘 사이의 차이를 **거의 구분할 수 없다.**

하지만 **좌표계를 반사(reflection)** 할 때  
(예: 왼손 좌표계를 오른손 좌표계로 바꿀 때),  
**의사벡터의 특이한 성질**이 드러난다.

일반 벡터는 단순히 **거울상(mirror image)** 으로 변환된다.

**의사벡터는** 거울상이 되면서 **방향도 뒤집힌다.**

## 

## **Linear Interpolation of Points and Vectors (****점과 벡터의 선형 보간)**

게임에서는 종종, **두 개의 주어진 벡터 사이에 존재하는 중간 벡터**를 구해야 하는 상황이 생긴다.

예를 들어, 어떤 오브젝트를 **점 A에서 점 B로 2초 동안 부드럽게 애니메이션**하고 싶다고 해보자.  
프레임 레이트가 30fps라면, A와 B 사이의 **중간 위치를 60개** 계산해야 할 것이다.

**선형 보간(Linear Interpolation)** 은  
두 점 사이의 **중간 위치(intermediate point)** 를 찾아주는  
간단한 수학 연산이다.

이 연산은 일반적으로 **LERP**라고 줄여 부른다.  
LERP 연산은 다음과 같이 정의된다 (t는 0 이상 1 이하의 값이다)

```
LERP(A, B, t) = (1 – t) * A + t * B
```

기하학적으로, L = LERP(A, B, t) 는 점 A에서 점 B로 향하는 선분 위에서 t만큼 진행한 **지점의 위치 벡터**이다.

수학적으로 보면, LERP는 **두 입력 벡터의 가중 평균(weighted average)** 이다.  
이때 사용되는 가중치는 각각 (1 – t) 와 t이다.

중요한 점은,

**이 가중치들의 합은 항상 1**이 된다는 것이다.  
이는 모든 가중 평균에서 일반적으로 요구되는 특성이기도 하다.

![](https://blog.kakaocdn.net/dna/AMxKc/btsPDsMwWO2/AAAAAAAAAAAAAAAAAAAAANOadK9UFEfpuKaKEzs3h1Kg54ku4flayftDFTb_sffD/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=x%2F2X2XyJMbFwizvHPZqu3Tx%2BYAI%3D)

위 그림은 점 A와 B 사이에서 보간 인자 t = 0.4일 때의 선형 보간(LERP)을 보여준다.