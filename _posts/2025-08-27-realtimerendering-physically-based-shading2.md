---
title: "[RealTimeRendering] Physically Based Shading(2)"
date: 2025-08-27
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### 

### **Surfaces**

광학적 관점에서, **물체의 Surface는** **서로 다른 굴절률 값을 가진 두 부피를 구분하는 2차원 경계면이다**.

빛 파동이 어떤 표면에 부딪히면, **두 가지 요소**가 결과에 중요한 영향을 준다:

1. 표면의 양쪽에 있는 **물질의 종류** (즉, 두 쪽의 굴절률 n1과 n2)

=> 바깥쪽(빛이 처음 들어오는 쪽)의 굴절률을 **n1**,

=> 안쪽(빛이 통과해서 들어가는 쪽)의 굴절률을 **n2**라고 하자.

2. **표면의 기하학적 모양** (평면인지, 울퉁불퉁한지 등)

이 절에서는 먼저 **물질의 종류**에만 집중하고, 표면의 모양은 가장 단순한 경우인 **완전히 평평한 면**이라고 가정한다.

이전 절에서 우리는, **빛이 어떤 물질의 성분이나 밀도의 불연속성(즉, 굴절률의 변화)**을 만나면 Scattering된다는 것을 배웠습니다.

=> particle(cluster)의 크기 차이로 인한 Scattering, homogenous/nonhomogenous media에서의 scattering

여기서 **두 매질을 나누는 평면 표면**은 이런 불연속성의 한 예이며, 특별한 방식으로 빛을 산란시킨다.

그 이유는 **경계 조건(boundary conditions)** 때문인데, 다음과 같은 규칙이 있다

1. 표면에 평행한 전기장/자기장 성분은 표면 양쪽에서 연속적이어야 한다.

즉, **전기장/자기장 벡터를 표면에 투영한 값(= 평행 성분)** 이 표면의 양쪽에서 동일해야 한다는 뜻이다.

2. 표면에 수직인 전기장/자기장 성분은 매질에 따라 변할 수 있다.

이 조건은 몇 가지 중요한 결과를 낳습니다.

### 

### 1. Scattered wave(산란파)의 위상 제한

표면(경계면과 평행하는 방향)에서 생기는 모든 산란파는 **입사파(incident wave)** 와 위상이 **같거나(0°)** **정반대(180°)** 여야 한다.

다시 말해, 산란파의 파동 꼭대기(peak)는 입사파의 꼭대기나 바닥(trough)와 정확히 맞물려야 한다.

이 조건 덕분에, 경계면에서의 산란파가 나아갈 수 있는 방향은 **단 두 가지뿐이다**:

**1. 앞쪽으로 진행하는 파동** => 이것이 **굴절(transmitted wave)**

**2. 뒤쪽으로 되돌아가는 파동** => 이것이 **반사(reflected wave)**

### 

### 2. Scattered wave(산란파)의 주파수 유지

산란파는 반드시 입사파와 **같은 주파수(frequency)** 를 가져야 한다.

여기서는 이해를 돕기 위해 **단일 파장(=단색광, monochromatic wave)** 만 고려하고 있지만,

실제로는 일반적인 파동도 **단색 성분으로 분해해서 각각 적용하면 같은 원리가 적용된다.**

### 

### 3. Snell's Law (스넬의 법칙)

빛 파동이 한 매질에서 다른 매질로 이동할 때, phase velocity(파동이 매질을 통해 이동하는 속도)는 굴절률의 상대적 비율(n1/n2)에 비례하여 변한다.

주파수는 고정되어 있으므로, 파장도 (n1/n2)에 비례하여 변한다.

![](https://blog.kakaocdn.net/dna/6wJ17/btsP6RMqPMi/AAAAAAAAAAAAAAAAAAAAAA4Y8MGbMsdyrErzPW-yzE-WidHsgfh-NCcDZzgh-NWe/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=u7IDyjtXHTRW3sjcO0laITX33I8%3D)

![](https://blog.kakaocdn.net/dna/zwNVr/btsP6dWxqip/AAAAAAAAAAAAAAAAAAAAAAidyLKW0fRF9t-41hBvlieTa0ke-tS-pPeLf7Nz6rj3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=66xqK3Dm%2FnkwjA8mFiIOFQG3r%2BE%3D)

빛 파동이 굴절률 n1n1n1 과 n2n2n2 를 구분하는 평면 표면에 부딪히는 모습.

굴절은 종종 유리나 수정과 같은 투명한 물질과 연관되어 생각되지만, 불투명한 물체의 표면에서도 발생한다.

불투명한 물체에서 굴절이 발생하면, 빛은 물체 내부에서 산란과 흡수를 겪는다.

위의 **표면 굴절 현상(반사 + 굴절)은 굴절률의 급격한 변화**가 필요하며, 이는 파장 한개 보다 작은 거리에서 발생한다.

굴절률이 더 **점진적으로 변화하는 경우에는 빛이 나뉘지 않고, 대신 경로가 곡선으로 휘어진다**.

이러한 효과는 공기 밀도가 온도에 따라 변할 때 흔히 볼 수 있는데, 열 왜곡 현상이 그 예이다.

![](https://blog.kakaocdn.net/dna/dogoJ2/btsP8LRXQyy/AAAAAAAAAAAAAAAAAAAAAPGjWk3bRAa4mrcY8EGsPTRwKHkcOyAq09YstaJXgsGb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wGFv735YFCWEsYedesdg4ysjEyM%3D)

잘 정의된 경계를 가진 물체라도, 동일한 굴절률을 가진 물질 속에 잠겨 있다면 가시적인 표면을 가지지 않게 된다.

(굴절률의 변화가 없으면, 반사와 굴절은 발생할 수 없기 때문에 우리가 눈으로 체감할 수 없다는 의미)

아래의 그림이 그 예시이다.

![](https://blog.kakaocdn.net/dna/cI1EzN/btsP8hRhnOb/AAAAAAAAAAAAAAAAAAAAAAE2G9FVlVob-ZcFsRqZKZsqnxzTfYmy_QrdsOrf-GuW/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Q2ong0A2%2BoDNcSDILjgcrsAFOhc%3D)

### 

### **Geometry**

이제 또 다른 중요한 요인인 기하학을 다뤄보자.

엄밀히 말하면, 완벽하게 평평한 표면이 존재하는 것은 불가능하다. 모든 표면은 어떤 종류의 불규칙성을 가지고 있다.

**그러나 파장보다 훨씬 작은 표면 불규칙성은 빛에 아무런 영향을 주지 않으며,**

**파장보다 훨씬 큰 표면 불규칙성은 국소적인 평탄성에 영향을 주지 않고 단순히 표면의 기울기를 바꾸는 효과만 가진다.**

**(너무 작아도 무시, 너무 크면 방향을 변화시킴)**

오직 크기가 파장의 1배에서 100배 정도 범위에 있는 불규칙성만이 회절(diffraction)이라 불리는 현상을 통해 표면이 평면과 다르게 동작하게 만든다.

**렌더링에서 우리는 보통 간섭과 회절 같은 파동 효과를 무시하는 geometrical optics(기하광학)를 사용합니다.**

**=>모든 표면의 불규칙성이 빛의 파장보다 훨씬 작거나 훨씬 크다고 가정하는 것.**

geometrical optics(기하광학)에서는 빛을 파동이 아니라 광선으로 모델링합니다.

빛의 광선이 표면과 교차하는 지점에서, 그 표면은 국소적으로 볼 때 평평한 평면으로 취급됩니다.

**이 시점부터 당분간 geometrical optics 영역을 유지하겠습니다.**

앞서 언급했듯이, 파장보다 훨씬 큰 표면 불규칙성은 표면의 국소적인 방향을 변화시킨다. (기울기가 변화했기 때문에)

이러한 불규칙성이 개별적으로 렌더링하기에는 너무 작은 경우(즉, 픽셀보다 작은 경우)를 microgeometry라고 부릅니다.

반사와 굴절의 방향은 표면 법선에 의존합니다. microgeometry의 효과는 표면의 서로 다른 지점에서 법선을 변화시켜, 반사 및 굴절된 빛의 방향도 변화시키는 것입니다.

![](https://blog.kakaocdn.net/dna/CCE5S/btsP7yZ3TJI/AAAAAAAAAAAAAAAAAAAAAAyLoKSS4S2SPQZRCfv7DESNDPB1EPa-hBrqkxV3_idV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wMbZLMe6xXpP4QzCIy7r3JAax6c%3D)

각각의 특정 표면 지점은 단 하나의 방향으로만 빛을 반사하지만, 각 픽셀은 다양한 방향으로 빛을 반사하는 여러 표면 지점을 포함하게 되는 것입니다.

렌더링에서, microgeometry를 하나 하나 명시적으로 모델링하기보다는, 이를 통계적으로 처리하고 표면이 무작위로 분포된 미세 구조 법선(mircrostructrue normal)을 가진 것으로 본다.

그 결과, 표면은 빛을 (굴절과 반사를 모두) 연속적인 방향 퍼짐으로 반사하는 것으로 모델링된다.

=> 정리하자면

표면의 microgeomtry를 하나하나 계산하는게 아니라, 기울기 분포를 다뤄서, 표면이 빛을 여러 방향으로 퍼뜨리는 것처럼 표현한다.(=표면의 거칠기)

제가 구현할 때를 생각해보면, 눈에 빛이 들어오는 비율을 계산해서( ex, dot(l, v)) 빛의 세기를 조절했던 것 같습니다.

![](https://blog.kakaocdn.net/dna/2sniW/btsP8fMJSc7/AAAAAAAAAAAAAAAAAAAAAJOgpb91RZUP2ML91TrZNUmpn6oltoWrbLITGTCrBmJt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nzg8xWkIsWkOK3CJCyXYtA%2BK7us%3D)

### 

### **Subsurface Scattering**

굴절된 빛은 물체의 내부 부피와 계속 상호작용한다. 굴절된 빛은 재료를 통과하면서 흡수를 겪는다.

이 예에서는 긴 파장은 대부분의 흡수가 일어나서, 짧은 파장의 파란빛이 남았다.

또한 빛은 재료 내부의 입자들로부터 산란된다. 결국, 굴절된 빛 일부가 다시 표면 밖으로 산란되어 나오게 되며,

그림에서 표면을 다양한 방향으로 빠져나가는 파란 화살표로 표시되어 있다.

![](https://blog.kakaocdn.net/dna/bzb9Ue/btsP8FRQ0t4/AAAAAAAAAAAAAAAAAAAAAOxqOHln6hLojngmGBBMbbnoOinz7nv9lWZFUcwcaxsV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=c92%2BrF3K19DNr6l5iQ4b8ZCu%2FS8%3D)

산란된 이 빛은 입사 지점으로부터 다양한 거리에서 표면을 빠져나온다.   
entry-exit 거리의 분포는 재료 속 산란 입자의 밀도와 특성에 따라 달라진다. 이 거리와 셰이딩 스케일(픽셀 크기)의 관계가 중요합니다.

만약 entry-exit 거리가 필셀 크기에 비해 매우 작다면,

셰이딩할 때 subsurface scattering을 고려하지 않아도 된다.(특정 지점에서 나가는 빛은 같은 지점으로 들어오는 빛에만 의존하게 된다.)

![](https://blog.kakaocdn.net/dna/pa9kn/btsP9BIhgyB/AAAAAAAAAAAAAAAAAAAAAD9j_8MnTQuxRh-szzfRrou6G8rE6ZB1UJgkMBS1uwxx/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ioJmYmUoTeZvhI8knMha3J4YyxM%3D)

그러나 표면 아래 산란광은 표면 반사광과 시각적으로 상당히 다른 특성을 가지므로, 이들을 별도의 셰이딩 항으로 나누는 것이 편리하다.

**스펙큘러 항(specular term)** 은 표면 반사를 모델링하고,

**디퓨즈 항(diffuse term)** 은 로컬한 표면 아래 산란을 모델링한다.

entry-exit 거리가 셰이딩 스케일에 비해 매우 크다면, 빛이 한 지점에서 표면 속으로 들어가 다른 지점에서 빠져나오는 시각 효과를 담기 위해 특수한 렌더링 기법이 필요하다.

이러한 글로벌 표면 아래 산란 기법들은 다른 주제(책의 다른 토픽,, Physically based shading에서는 X)에서 자세히 다룬다.