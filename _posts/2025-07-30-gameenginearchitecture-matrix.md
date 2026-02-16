---
title: "[GameEngineArchitecture] Matrix"
date: 2025-07-30
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

![](https://blog.kakaocdn.net/dna/b72nLY/btsPDIIpuKk/AAAAAAAAAAAAAAAAAAAAAGRAP-BADGZDK4ltYzT273l_JGOsGbpaNvZS6HrehI5Y/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=uQdYlFndfqRBf%2FTMFAYhqzjqk28%3D)

행렬(matrix)은 m × n개의 스칼라(scalar)들로 이루어진 직사각형 배열이다.  
행렬은 **이동(translation)**, **회전(rotation)**, **스케일(scale)**과 같은 **선형 변환(linear transformation)을** 표현하는 데 매우 편리한 방식이다.

행렬 M은 일반적으로 대괄호로 둘러싸인 격자 형태로 작성되며, 각 성분은 행(row) 인덱스와 열(column) 인덱스를 갖는다.  
예를 들어, M이 3×3 행렬이라면 다음과 같이 쓸 수 있다

![](https://blog.kakaocdn.net/dna/k3eiv/btsPBruKxXE/AAAAAAAAAAAAAAAAAAAAAD7_0Z-j5Y-XH_49KOdLJH92PVXyDtjqfhRIBIWTf2dj/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=q%2F1vawOySMHNGJw4qEYodkuyM18%3D)

우리는 3×3 행렬의 행 또는 열을 **3D 벡터**라고 생각할 수 있다.

3×3 행렬의 모든 행 벡터 및 열 벡터가 **단위 크기**(unit magnitude)를 갖고, **서로 직교**한다면, (row는 row끼리, column은 column끼리 직교)  
그것을 특수 직교 행렬(special orthogonal matrix)이라고 부른다. 이는 **등방 행렬(isotropic matrix)** 또는 직교 정규 행렬(orthonormal matrix)이라고도 한다**.**  
**이러한 행렬은 회전(rotation)을 표현한다.**

**=> 회전 == orthonormal matrix라고 알면된다**

**특정한 조건 하에서, 4×4 행렬은 이동, 회전, 스케일 조정(scale)을 포함한 임의의 3D 변환을 표현할 수 있다.**  
**이러한 행렬을 변환 행렬(transformation matrix)\*라고 하며, 게임 엔지니어링에서 매우 유용하게 사용된다.**

행렬이 나타내는 변환은 행렬 곱셈을 통해 **점이나 벡터에 적용**된다.

### **Affine Matrix (****아핀 행렬)**

아핀 행렬은 **직선의 평행성**과 **상대적인 거리 비율**은 유지하되, **절대 길이**나 **각도**는 유지하지 않는 4×4 변환 행렬이다.  
회전, 이동, 스케일, 쉬어(shear)와 같은 연산을 조합한 행렬은 모두 아핀 행렬이다.

## 

## **Matrix Multiplication (****행렬 곱셈****)**

두 행렬 A와 B의 곱을 P = AB로 나타낸다.  
만약 A와 B가 변환 행렬이라면, 곱 P는 **두 변환을 연속으로 수행하는 새로운 변환 행렬**이 된다.

예를 들어, A가 스케일 행렬이고 B가 회전 행렬이라면, P는 **스케일 후 회전**을 적용하는 행렬이 된다.

**여러 변환을 사전에 하나의 행렬로 결합**해두면, 많은 벡터에 대해 **변환을 매우 효율적으로 적용**할 수 있기 때문에 게임을 제작할 때 유용하게 사용된다.

행렬 곱을 계산할 때는,

A 행렬의 **행 벡터(row)** 들과 B 행렬의 **열 벡터(column)** 들 간의  
내적(dot product)을 이용한다.

![](https://blog.kakaocdn.net/dna/benpR2/btsPDUBRnCS/AAAAAAAAAAAAAAAAAAAAAOxIGCXrGQrN720IHPMZujH88-sL-XZMR_V7C3espYVa/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xZfmZLqP%2B61I%2Fm2X1ToCl94y32M%3D)

각 내적의 결과가 결과 행렬 P의 한 성분이 된다.

두 행렬의 inner dimensions이 같을 경우에만 곱셈이 가능하다.

**즉, A가 n1 × m1, B가 n2 × m2일 때,**

**m1과 n2가 동일해야지 곱셈을 할 수 있다.**

**비가환성 (Non-Commutativity)**

행렬 곱은 교환 법칙(commutative property)이 **성립하지 않는다.**

![](https://blog.kakaocdn.net/dna/dbc73F/btsPDETBcJB/AAAAAAAAAAAAAAAAAAAAAPA3CsaX7aS9SPt840VegQpCWdlfiG99Aeo_gfy9B2-a/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=OJhJcbL07CB5Sj86ksuVxUY0rgQ%3D)

**행렬 곱셈의 순서**는 매우 중요하며, 이후 내용에서 추가 설명하겠다.

행렬 곱셈은 흔히 concatenation이라고도 불린다.  
여러 개의 변환 행렬을 곱한 결과는, **각 변환들을 곱한 순서대로 연결한 전체 변환**을 수행하는 **하나의 행렬이기 때문이다**.

### 

### **Representing Points and Vectors as Matrices**

점과 벡터는 **행 벡터(row matrix, 1×n)** **또는 열 벡터(column matrix, n×1)로 표현할 수 있다.**

![](https://blog.kakaocdn.net/dna/bngywT/btsPDNbOrPh/AAAAAAAAAAAAAAAAAAAAANrjK3uu8H7UyzWQqxpdZ8SFG8H6hIo9KI6BMRslKBmi/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=bZDrIk%2FLOYsN6j%2FPuWkqPjWeNPM%3D)

행 벡터와 열 벡터 중 어떤 형식을 사용할지는 **완전히 임의적 선택**이다. 다만, 어떤 것을 사용하느냐에 따라 **행렬 곱셈의 순서**가 달라진다.

행렬 곱셈에서는 두 행렬의 내부 차원(inner dimensions)이 일치해야 하므로 다음 규칙이 적용된다:

**1×n 행 벡터와 n×n 행렬을 곱하려면**, 벡터는 **행렬의 왼쪽**에 위치해야 한다.

![](https://blog.kakaocdn.net/dna/zvY6D/btsPCqaR7KN/AAAAAAAAAAAAAAAAAAAAAAfIVwbE7s6l4ZWLzkb1uJ9yK6bXfKQH7P5YQr_zFPeI/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GmmWlgx%2FPwR9YRX6dfArdALcddA%3D)

**n×n 행렬과 n×1 열 벡터를 곱하려면**, 벡터는 **행렬의 오른쪽**에 위치해야 한다.

![](https://blog.kakaocdn.net/dna/ddTIwG/btsPBJoqP24/AAAAAAAAAAAAAAAAAAAAAF4VFPoCioWqjr8Km8uPKiwB9qIVy1QtABXInjyc4Nu5/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=YwwhVTRb7af3zHqwTKcAoxNegmw%3D)

### 

행렬 A, B, C가 어떤 벡터 v에 차례대로 적용된다고 하면

**행 벡터(row vector)를 사용할 경우**, 변환은 **왼쪽에서 오른쪽으로 적용**된다.

![](https://blog.kakaocdn.net/dna/NNaqX/btsPCK75cpv/AAAAAAAAAAAAAAAAAAAAAHc0krv1LuolNa3tau9j2xXmCNef_6XD_a3G-G_cR9jZ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=8SHQLe%2FLmGVcWB3X642lLsQuDCs%3D)

**열 벡터(column vector)를 사용할 경우**, 변환은 **오른쪽에서 왼쪽으로 적용**된다.

![](https://blog.kakaocdn.net/dna/bI0hSI/btsPCoxnRd4/AAAAAAAAAAAAAAAAAAAAAEnA8FGji0gBNNh9P47wTrsXJTBTaicFl8m_rGgKJT8u/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=cpPGnvXcseoCxpUud2x7m%2F1zwfE%3D)

이 책에서는 **행 벡터(row vector)** 방식을 채택한다.

하지만, **당신이 사용하는 게임 엔진이나 다른 책, 논문, 웹사이트**가 어떤 방식을 따르는지 **반드시 확인**해야 한다.  
일반적으로는 **행렬 곱에서 벡터가 왼쪽에 있으면 행 벡터 방식**, **오른쪽에 있으면 열 벡터 방식을 사용한다고 판단할 수 있다.**

(만약 열 벡터 방식을 쓴다면, 이 책에서 나오는 모든 행렬은 전치(transpose) 해서 사용해야 한다.)

### 

### **항등 행렬 (Identity Matrix)**

항등 행렬은 **어떤 행렬과 곱하더라도 원래의 행렬을 그대로 반환**하는 특성을 가진다.  
항등 행렬은 보통 I로 표기한다.

항등 행렬은 **대각선**

**성분이 모두 1**, **그 외의 성분은 모두 0인 정방 행렬(square matrix)이다:**

![](https://blog.kakaocdn.net/dna/LFuJE/btsPDETBNDk/AAAAAAAAAAAAAAAAAAAAAP_hh8weoIYdpM0nOMAWWQhKMA5m6VCOT0alZP2U4ftg/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=0XgsReRCRWIo7j1p%2BdblW5emCfU%3D)

### 

### **행렬의 역행렬 (Matrix Inversion)**

어떤 행렬 **A의 역행렬은, A의 변환 효과를 되돌리는 행렬이다. 이를 A^-1로 표기한다.**

예를 들어, A가 객체를 **z축 기준으로 37도 회전시킨다면, A^-1은 z축 기준으로 –37도 회전**시킨다.  
또한, A가 객체의 크기를 **2배로 스케일했다면, A^-1은 절반 크기로 스케일 다운**한다.

행렬과 그 역행렬을 곱하면 항상 **항등 행렬**이 된다.

![](https://blog.kakaocdn.net/dna/239Pn/btsPDUPo8VI/AAAAAAAAAAAAAAAAAAAAAL2OGwgE7FgawHVjh67-850O7utHUhl5z3zul1DSy0FO/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3ZaUSVvY%2F36WISEfozETCss7kmc%3D)

모든 행렬이 역행렬을 가지는 것은 아니지만,  
**회전, 이동, 스케일, 쉬어(shear)의 조합인 아핀 행렬(Affine Matrix)은 항상 역행렬을 가진다.**

역행렬을 계산할 때는 보통 가우스 소거법(Gaussian Elimination)이나 LU 분해(Lower-Upper Decomposition) 등의 방법이 사용된다.

또한, **여러 행렬을 곱한 결과의 역행렬**은, **각 행렬의 역행렬을 역순으로 곱한 것**과 같다:

![](https://blog.kakaocdn.net/dna/bZVfl2/btsPB2nSMb6/AAAAAAAAAAAAAAAAAAAAAArORHy-CggIgJThXUR5bKYjCA4PTv1s0X055sEyxhZt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=17pFPQZ9FMXdL4Za%2BP6wwNt75OU%3D)

**Transpose (전치)**

행렬 M의 전치(transpose)는 M^t으로 표기되며,

![](https://blog.kakaocdn.net/dna/N28ed/btsPB0XTLPl/AAAAAAAAAAAAAAAAAAAAAPsIlYn7sOehpAdBqOM5SiNxf1xjSYEKLkb9nVeBzNZ7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=IVjRlAeA35pmczkZ4u70Rc1uSxw%3D)

 행(row)은 열(column)이 되고, **열은 행이 된다**:

![](https://blog.kakaocdn.net/dna/cZvufD/btsPCIPXpHg/AAAAAAAAAAAAAAAAAAAAADsba322oa6ohkoNqLoN1JaPB0GDiTJqpL20Sq93LPlx/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=jq8SNn%2BnGxXO8%2BsJb8km6Ovf8H8%3D)

직교 정규 행렬(= 회전 행렬)의 역행렬은 전치와 같다.  
즉, R⁻^-1 = R^t

**전치 연산은 역행렬 계산보다 훨씬 계산 비용이 적기 때문에 매우 유용한 개념이다.**

어떤 라이브러리는 열 벡터 방식, 다른 라이브러리는 행 벡터 방식을 사용하므로,  
행렬을 전치하여 변환해야 한다.

역행렬과 마찬가지로, **여러 행렬의 곱에 대한 전치**는,  
**각 행렬을 전치한 결과를 역순으로 곱한 것**과 같다.

![](https://blog.kakaocdn.net/dna/bmSzmV/btsPBkJcZVD/AAAAAAAAAAAAAAAAAAAAAOHb805qUaEn3pMhT8TZMQMsoTorEgbxSAPNxbKfyVRF/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=e7knBeb3Q4RavYVPVm6oRR31bvs%3D)

### **Homogeneous Coordinates (동차 좌표계)**

대수학에서, **2×2 행렬**이 2차원 회전(rotation)을 표현할 수 있다는 것을 배운 적이 있을 것이다.  
어떤 벡터 r을 각도 ϕ만큼 회전시키려면 (방향은 반시계 방향), 다음과 같이 쓸 수 있다:

![](https://blog.kakaocdn.net/dna/5BaXy/btsPDUBS9Yc/AAAAAAAAAAAAAAAAAAAAAA3suT8F4U6VglI-JYXmYpZApcOoG0r1Olx4MgmzBw4Y/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=BKGPH5d%2BMJ7F1lxsM2M%2FeniGrQs%3D)

3차원에서의 회전도 마찬가지로 **3×3 행렬**로 표현할 수 있다는 것은 아마 놀랍지 않을 것이다.  
위의 2D 회전 예시는 사실 **z축을 기준으로 하는 3차원 회전**의 특별한 경우에 해당한다.  
따라서 다음과 같이 쓸 수 있다.

![](https://blog.kakaocdn.net/dna/nxZOl/btsPCJaiflt/AAAAAAAAAAAAAAAAAAAAALrpH38nUEEyKED7YjTPMri8EMfdGRz5HXGVW2D8YcIH/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=RrjfZYwdeV1bEiztwhWW98KZeUU%3D)

그럼 이동(translation)도 표현할 수 있을까?

**안타깝게도 안된다..**

어떤 점 r에 대해 이동 벡터 t를 적용하려면, 각 성분을 **단순히 더해야 한다**:

![](https://blog.kakaocdn.net/dna/wk4vi/btsPB0DwFQo/AAAAAAAAAAAAAAAAAAAAAE18oD8s4Ur-kFfhiMfwrxQiGQpbC3C1xt7F-Sw3bOf6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=L77wy89PvoQNwiN%2BRL2CejrrD8s%3D)

**3×3 행렬만으로는** r+ t 같은 결과를 만들 수 있는 방법이 존재하지 않는다.

그렇다면 어떤 형태의 4×4 행렬이 이동을 표현할 수 있을까?

우리는 회전을 제외한 **순수한 이동만** 원하므로, 상단 3×3 영역에는 항등 행렬(identity)을 넣고, 이동 벡터 t 의 성분을 **마지막 행**에 배치한다.

![](https://blog.kakaocdn.net/dna/cR01Zv/btsPB0wJ8cP/AAAAAAAAAAAAAAAAAAAAANAwEEoHJ7PWVqv86Qs3EvKY2KQfDreKUhOipokEYTE9/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GaHbcTrpdg8bWkhzYHUuwk8Z%2F8A%3D)

벡터 r는 [rₓ, rᵧ, r𝓏, w]의 4D 벡터로 확장하고, 이때 w = 1로 설정한다.

![](https://blog.kakaocdn.net/dna/edFytB/btsPDGqncfA/AAAAAAAAAAAAAAAAAAAAAGqqivxPkHy93I2uto6UvUDjP5mMSjwW6gOIkLA3k9wF/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=to%2B8XYqll6NbwL%2BCSjSMC3pfM6I%3D)

이 경우, r과 이 4×4 행렬을 곱하면 다음 결과가 나온다

즉, 정확히 원하는 **이동 변환**이 수행된다.

![](https://blog.kakaocdn.net/dna/cjWDr9/btsPBjcsJx9/AAAAAAAAAAAAAAAAAAAAAJhmbbyB6786SRFUJZVqAMNbqiJ0xDlSPRw1N290Q5Lt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=7aePcWBelyLRNKX5m2BuBratU1U%3D)

이와 같이 **3차원 점이나 벡터를 4차원으로 확장하여 표현하는 방식**을 **동차 좌표(homogeneous coordinates)라고 부른다.**

동차 좌표에서의 점(point)은 항상 w = 1을 갖는다.  
**대부분의 게임 엔진에서 수행되는 3D 행렬 연산은 4×4 변환 행렬과 4성분 벡터(homogeneous vector)를 기반으로 이루어진다.**

### 

### **방향 벡터(Directional Vector)의 변환**

수학적으로 점(위치 벡터)과 방향 벡터(direction vector)는 변환 시 **약간 다르게 다뤄진다**.

점(point)은 **이동 + 회전 + 스케일** 모두 영향을 받는다.

**방향 벡터**는 **이동 변환의 영향을 받지 않는다.**

**왜냐하면, 방향 벡터는 방향만을 나타내는 정보이므로,**  
**이동을 적용하게 되면 그 방향 벡터의 크기(magnitude)가 변형되어 의도와 달라지기 때문이다.**

이러한 이유로 동차좌표계에서 점과 벡터의 w값은 달라진다.

**점**은 w = 1

**방향 벡터**는 w = 0

![](https://blog.kakaocdn.net/dna/uPw3X/btsPEEZPGeN/AAAAAAAAAAAAAAAAAAAAAC5jczDzGy_gPORmYs4-_zXTUWQl1ZVQw1_EmQ80pcUl/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=gR52WNiR4DJ7n28V13HqrJmb4tQ%3D)

즉, w = 0이기 때문에 **이동 벡터 t의 영향은 사라지고**, 오직 회전/스케일만 작용하게 된다.

동차 좌표계에서 [x, y, z, w]는 일반 3D 좌표 [x/w, y/w, z/w]로 변환할 수 있다:

![](https://blog.kakaocdn.net/dna/kUSun/btsPCjCYIIb/AAAAAAAAAAAAAAAAAAAAAKq7o_Hz4azyN3Ag9RNAAIDXK8Cu3vH9D1t5WC3mnx6b/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=FuxoiW%2FYs38m019P%2FbM9%2BA7cuZ8%3D)

그래서 우리는 점(point)의 w = 1로 설정하는데, 이는 **3D 좌표에 아무런 영향을 주지 않기 때문**이다.

반면, **방향 벡터는 w = 0**이므로 이 값을 나누면 무한대가 발생한다.

이는 수학적으로도 방향 벡터를 **4차원 공간에서 무한대에 위치한 점처럼 취급**한다는 의미다.

이러한 점은 **회전은 가능하지만 이동은 불가능하다.**

왜냐하면, 아무리 이동을 시도해도, 무한대에 있는 점은 움직이지 않기 때문이다.

결과적으로, **3차원 공간의 방향 벡터**는 **4차원 동차 좌표 공간에서는 무한대에 있는 점**처럼 작용한다.

### **Atomic Transformation Matrices(****기본 변환 행렬****)**

**모든 아핀 변환 행렬(affine transformation matrix)은 다음과 같은 pure transformation들의 4×4 행렬을 연쇄 곱셈(concatenation)으로 조합하여 만들 수 있다:**

1.이동 (translation)

2. 회전 (rotation)

3. 스케일 (scale)

4. 쉬어 (shear) <= 게임에서는 드물게 사용되므로 여기선 생략

아핀 4×4 변환 행렬은 다음과 같이 4개의 구성 요소로 나눌 수 있다

![](https://blog.kakaocdn.net/dna/bmJ25n/btsPB31mrfD/AAAAAAAAAAAAAAAAAAAAAKGFQ9MODzUa9L3B-X5X6zoM7zF9aXyfen1TVri8XZc1/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KHLgxHRqH8uoxHSjazc5o4%2FWNls%3D)

U3x3: 회전과/또는 스케일을 포함한 상단 3×3 행렬

t1x3: 이동 벡터(translation vector)

03x1: 영벡터(3×1)

1: 우측 하단의 스칼라

이런 식으로 분해된 행렬에 점 [r 1]을 곱하면 다음 결과가 된다

![](https://blog.kakaocdn.net/dna/cGBArU/btsPB3NQAWu/AAAAAAAAAAAAAAAAAAAAABO71cJas7boh0xXiE886zis6hNRCG5676ERuq__43TM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=MOydQSIebrbEEubo4NLHeBxwwvg%3D)

회전/스케일 후 이동이 순서대로 적용된다.

### 

### **Translation (이동 변환)**

다음 행렬은 점 r을 **벡터 t = [tx, ty, tz]만큼 이동**시킨다.

![](https://blog.kakaocdn.net/dna/mMVKY/btsPCMkyQtC/AAAAAAAAAAAAAAAAAAAAAD8tNwF14yd67j5tE83I0m-0AR_CZtMiISmLfwXHfQjE/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=4i3ffumBotsLXQ4wMg03q%2FqdWRc%3D)

아래와 같이 축약해서 표기할 수 있다.

![](https://blog.kakaocdn.net/dna/sYYJ1/btsPBluEZ9D/AAAAAAAAAAAAAAAAAAAAABy9xyVK_6Dx-F0dgptOymeEkwL7nXqLhs4-aSMrFp_n/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=k5XeQVX7fB7X3N5B4qv9Lv0TE1c%3D)

### 

### **Rotation(****회전 변환****)**

모든 **회전 행렬**은 다음과 같은 형태를 가진다.

![](https://blog.kakaocdn.net/dna/b6IYIn/btsPDGcP2OH/AAAAAAAAAAAAAAAAAAAAAE6aEBOyHV0H5sqc3rjL5bDqdKzJ07GYv2_rxeK8WOYM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Kgc5iUdNZ6V2hMTrfd7%2FsBzDOcs%3D)

R은 상단 3×3에 회전각의 사인(sin)과 코사인(cos)으로 구성된다. (회전각은 **라디안 단위**로 측정됨)

#### x축 기준 회전 (rotate about x-axis)

![](https://blog.kakaocdn.net/dna/dHtKNX/btsPCTjBZxJ/AAAAAAAAAAAAAAAAAAAAAKhQyunnlglOOvEo89ihmUfLYEIPbQPrUzaANkcQPJh2/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2BaBdHzgQxlMV2T1O68rhvP3jxbQ%3D)

#### y축 기준 회전 (rotate about y-axis)

![](https://blog.kakaocdn.net/dna/ROD94/btsPCLso1Vm/AAAAAAAAAAAAAAAAAAAAAENdoQjzytm0htj5fr-ZS-Q-_yFtJPMQ9GkYdW8scVYO/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=NKZpXRS2V4lL7ZXYmQ1WsXhc%2BKc%3D)

행렬은 **x/z가 뒤바뀌므로 다른 회전들에 비해 전치된 형태**처럼 보인다.

#### z축 기준 회전 (rotate about z-axis):

![](https://blog.kakaocdn.net/dna/d5PV8W/btsPBJPuIR5/AAAAAAAAAAAAAAAAAAAAAI_pacFB-7z-V2E9nENmPuTU64swK1zXeuBao9JvpDNM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=DKs35tzggcJ4bB4cViLqPUromBs%3D)

### **Scale(****스케일 변환****)**

다음 행렬은 r만큼 각 축 방향으로 스케일링한다:.

![](https://blog.kakaocdn.net/dna/bAcn0J/btsPDWGvPXn/AAAAAAAAAAAAAAAAAAAAAOzv9YP_H6_AwnA4uSim_G7NhUY-uUuWvspL6RoO1rfs/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xQh%2BJ7aQG9sHEde9xzhtrOtOLrE%3D)

#### 

많은 게임 엔진에서는 **충돌 체크의 단순화 및 성능 최적화**를 위해,  
**렌더링 모델이나 충돌체에는 오직 균일 스케일만 허용**하도록 제한한다.

### 

### **4×3 행렬 (4×3 Matrices)**

모든 아핀 4×4 행렬의 **오른쪽 마지막 열**은 항상 다음과 같다.

![](https://blog.kakaocdn.net/dna/cI4uiQ/btsPDNXgi91/AAAAAAAAAAAAAAAAAAAAANH1tmusYgetFrwq85GIYGkTayDmc7EJbnpDJA14lTO2/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=gOFKUqD%2FzL1faUG8tCm62TzxDgE%3D)

ini이처럼 항상 일정한 값을 가지므로, **게임 프로그래머들은 이 마지막 열을 생략**하고

**메모리를 절약**하기 위해 **4×3 행렬**을 자주 사용한다. **게임 수학 라이브러리**에서 4×3 아핀 행렬을 자주 보게 될 것이다.