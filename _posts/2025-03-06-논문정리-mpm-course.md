---
title: "[논문정리] MPM Course"
date: 2025-03-06
toc: true
categories:
  - "Tistory"
tags:
  - "MPM"
---

너무 양이 많아서 필요한 부분만 읽으면 계속 업데이트할 예정입니다...ㅎ

### 

### **5. Kinematics Theory**

MPM에서 particle(입자)는 개별적인 입자, 분자, 원자, 작은 구가 아니다. MPM 입자는 연속적인 material이다.

연속체(continuum bodies), 연속체 역학(continuum mechanics)에 대해 이야기할 때, 우리를 연속체 가정(continuum assumption)을 채택하겠습니다. 이 말은 material(고체 액체 가스 등)을 논할 때 연속체라고 생각하겠다는 것입니다.

연속체 가정(continuum assumption)은 광범위한 고체, 액체를 시뮬레이션 가능하게 해줍니다. (ex 탄성체, 근육, 살, 천, 머리카락, 액체, 눈, 진흙 등등)

연속체는 밀도, 속도, 힘의 위치 같은 quantities를 위치를 정의하는 연속 함수(continuous function of position) 로 정의합니다.

### **5-1 Continum Motion**

### **5-2 Deformation**

우리는 **X(material coordinate, Lagrangian Coordinate)와 x(world coordinate, Eulerian Coordinate)를 가지고 있고, 각각 Ω0과 Ωt에 속한다.  x = ϕ(X,t). 이렇게 표기도 가능하다.**

자코비안(Jacobian)의 ϕ(변형맵)는 여러가지로 유용하다. 변형맵의 자코비안을 F로 나타내고, 아래 식으로 정리가 가능하다.

![](https://blog.kakaocdn.net/dna/bu9NNo/btsMAYVnOEy/AAAAAAAAAAAAAAAAAAAAALnK3PRRsuX1qV9Svq0mBAXU8dCtsnhmcXbZsnVWxGRy/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KvL7c4o2rEr3Ok6tFdasyw5uj8E%3D)

**F(Jacobian of the deformation map)은 deformation gradient라고 불린다.** 보통 2x2, 3x3 행렬로 표현된다.

아래식의 deformation map에 대한 deformation gradient는 단위 행렬이다. 변화가 없다는 뜻

![](https://blog.kakaocdn.net/dna/4aSlm/btsMBWPXhyS/AAAAAAAAAAAAAAAAAAAAAKpGu9sb9bRXKI4j9rc5oVAU-Tgc9jrU4JBnFJX5ug9b/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=OpvzbxLUkXGuAoJ322vscpHxFiY%3D)

아래식의 deformation map에 대한 deformation gradient는  F = R이다.

![](https://blog.kakaocdn.net/dna/c4A5mW/btsMBCdaT6S/AAAAAAAAAAAAAAAAAAAAAEU0iOfOSGJQUsWxW0dVMwKtjHcZszaAckY2LDSfsoFV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FNjWaroXNLs421Xvs6t38mDGeNE%3D)

위의 두개의 식 모두 강체 변환(rigid transformation)만 수행되고, 실제 변환(deform)된 것이 없음을 알 수 있다.

### 

### **그래서 deformation gradient가 뭔데!**

직관적인 의미는 F(deformation gradient)는 지역적으로(material point 수준에서) 물질이 얼마나 변형(deformation) 되었는지를 나타내는 것이다.

아래의 식을 보면 더 직관적으로 다가올 것이다.

시뮬레이션 직전의 material point에 X0, X1이 포함되어 있고,

시뮬레이션 이후 각 점은 x0,x1로 변형된다.

그리고 F는 그 변화율이다.

![](https://blog.kakaocdn.net/dna/zEL6R/btsMAKXdjGM/AAAAAAAAAAAAAAAAAAAAAM21l2cm-Io05F_GNDpS_5c1vUsqqplChFbzVN3EQ_w6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xHi5CyNh93esINuIuKcoO29q14k%3D)

### **determinant F ( denoted with J, J라고 부르며,,)**

J는 미소 부피(체적) 변화( infinitesimal volume change )를 나타낸다.

J는 시간 t에서 변형된 물질의 미소 부피(체적)가 원래 부피(체적) 대비 얼마나 변했는지를 나타낸다. ( ratio )

![](https://blog.kakaocdn.net/dna/B4qAT/btsMzu8HTf6/AAAAAAAAAAAAAAAAAAAAAF7O6jXggEiEzX6N4aKtwC_dX7QF5fSCPj-yZPtYeMFZ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ENwFJv8IFl4sQ9%2BKCKozOcEsVVc%3D)

J ==  1 일 때, **변화가 없음 ( rotation, translation은 가능 )**

J > 1 일 때 , **체적 증가**

J < 1 일 때, **체적 감소**

J == 0 일 때, **체적이 0이 됨( 물리적으로는 불가능하지만, 수치적으로 가능 )**

J < 0 일 때,  **2D로 예를 들면 뒤집히는 경우? 라고 볼 수 있다. (invertible elasticity 로 해결가능)**

### **Push Forward and Pull Back**

지금까지는 물리량을 (X,t)로 표현했고, 이건 **Langrangian(라그랑주) 관점이다.**

그리고 이 함수를 **bijective 함수로 가정했다. ( bijective(전단사): 중복없이 일대일로 대응되는 함수 )**

또한 **Smooth한 함수라고 가정하면**

**Ω0(초기 상태)와 Ωt(현재 상태)는 **위상 동형(homeomorphic)** 또는 **미분 동형(diffeomorphic)** 관계를 가지게 된다.**

위의 가정들은 동일한 시간에 동일한 위치를 차짖하는 두 개의 material points가 존재하지 않는다는 의미이다.

이러한 가정하에 위치 함수는 다음과 같이 정의된다. ( 역함수가 존재한다는 것을 의미 )

ϕ는 position mapping이다.

![](https://blog.kakaocdn.net/dna/bRALbV/btsMBlCIewG/AAAAAAAAAAAAAAAAAAAAAHhXZkKP9smIwMUwKGcEoYVBN_EILnJV0wCtnnsb3QgS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=l5Wu1TV0RY4%2FxnTteBdtXBBbmJ8%3D)

**이제 한 공간에 정의된 함수는 change of variables( 변수 변환 ) 통해 다른 공간에서도 정의가 가능하다.**

### **5-3 Push Forward(Eulerian) & Pull Back(Lagrangian)**

한 좌표계에서 다른 좌표계로 변환될 때의 method이다.

**Push Forward: **Ω0 -> Qt로 변환****

( G:  Ω0 -> Qt )

![](https://blog.kakaocdn.net/dna/XO11Y/btsMAkR8pql/AAAAAAAAAAAAAAAAAAAAAM-bgePXIkHuvNpJFMjzMq0KsgtDN0QxfUCeZPgOLkMd/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=5HI0k064JPYRJaS4rsCMfcsccbc%3D)

****Pull Back: ****Ωt -> Q0 으로 변환********

( G:  Ω0 -> Qt )

![](https://blog.kakaocdn.net/dna/bV60Mu/btsMBAGrNvI/AAAAAAAAAAAAAAAAAAAAAGvh2ZTsPbqGW5T07CIKaEvuvgErm8kH9Jm6Rbbrexmw/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ddAxdhjsZ8AHRtnMgd9TDJf2S3M%3D)

### **속도 가속도 변환**

라그랑지안 속도와 가속도는 다음과 같이 정의된다.

![](https://blog.kakaocdn.net/dna/H0TRP/btsMCY860WV/AAAAAAAAAAAAAAAAAAAAAE8PCtHKmglbyNvQ20ST-nJkG177PTxQGpaUFHI9nnHk/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=IB8K6rTv8izXAXVG97llR9079is%3D)

여기에 push forward를 적용하여 eulerian 속도, 가속도를 구할 수 있다.

![](https://blog.kakaocdn.net/dna/bDRo2H/btsMDghcxlx/AAAAAAAAAAAAAAAAAAAAAAlRosRYeCHfnuW-2Tu9GulQh2NfP-08WbDcrzgEETGV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=TsmVGniJ90VFK7u3xah8fzalq18%3D)

반대로, 오일러 속도와 가속도를 pull pack하면 아래와 같다.

![](https://blog.kakaocdn.net/dna/nXMKO/btsMB8j9x2s/AAAAAAAAAAAAAAAAAAAAAJIu4B77RSdS-AH4y8owhrb-z1RB9fsjbk3tatbQ3MiL/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=dgnGKGZnPdoSZynAydxN6Hrqrw0%3D)

푸시 포워드를 적용하여 오일러 관점에서 표현하면 아래와 같이 표현할 수 있다.

![](https://blog.kakaocdn.net/dna/pUWUp/btsMCY864e9/AAAAAAAAAAAAAAAAAAAAALsolkGtHFg7ZgrQWH9uOHMoHnWDK-nLaoI1IUoaDPQf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=uwIxqVRAq%2FNAkE4e2lR5ELX3OCY%3D)

### **5.4 Material Derivative**

위의 식처럼 오일러 속도 v(x,t) 와 a(x,t)사이의 관계는 단순히 시간에 대한 편미분만으로 표현되지 않는다. 하지만 이 관계는 매우 자주 등장하며, 이를 **물질 미분(Material Derivative)** 이라고 한다.

물질 미분은 다음과 같이 정의된.

![](https://blog.kakaocdn.net/dna/brnlGY/btsMDHyOIxS/AAAAAAAAAAAAAAAAAAAAACo0ccN0z9UwSu-Eo_eTTb8eBi5b5vT5_EULtCXXJ8ry/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=QZqAZcAL13lZ%2FtnkqBt6e5batSs%3D)

### **6. HyperElasticity (탄성체)**

여기서 우리는 응력(stress)이 변형(or deformation gradient)과의 연관성을 consititutive relationship(구성 관계)을 통해서 설명할 것이다.

응력(stress)이란

물체의 전체 영역에 정의되는 filed이다. 여러 표현법이 있다. **예를 들어 Cauchy stress가 있다.**

이산화된 stress는 작은 행렬(tensor)이다.

물체가 변형될 때, **응력(stress)과 변형률 간의 관계를 정의하는 구성 모델**이 필요하다.

**hyperelastic material은** 변형에 대한 **potential energy를 통해 정의된다.**

**potential energy는 초기 상태에서 병형이 되면 증가한다.**

여기서는 elastic material과 plastic model을 다룬다.

### **First Piola-Kirchoff Stress**

**일반적인 고체**에서는 **응력-변형률 관계를 deformation gradient(F) 와 first piola-kirchoff stree(P)**로 표현하는 것이 자연스럽다.

hyperelastic material은 stress energy density funcition(응력 에너지 밀도 함수)에서  
피올라 키르초프 응력(Piola-kirchoff)이 도출될 수 있다.

𝜓: 에너지 밀도 함수

F: deformation gradient

P: piola kirchoff

![](https://blog.kakaocdn.net/dna/dOvQiz/btsMB4VA0UB/AAAAAAAAAAAAAAAAAAAAANx2XfAGQc7ldROGWGi9rCWVsyJc3f2tDgmXk-pohg8C/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=CLeogIYoiTwSH%2FjBeUy7%2BV2wkxw%3D)

**공학적으로는 Cauchy stress(코시 응력, σ)가 더 일반적으로 사용된다.**

아래와 같은 관계식을 나타낸다.

![](https://blog.kakaocdn.net/dna/cEUIP9/btsMBUluE21/AAAAAAAAAAAAAAAAAAAAAEFXV9P5uO3eD8GdRgEASI6eKDl3rrsBlqffCi6Qdq4w/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=E4AYn3icrqUY3Dy13B507GMMMTQ%3D)

-right Caucht-Freeni tensor

-polar decomposition

은 필요할 때 다시 정리하러 올게욤

### 

### **Neo-Hookean**

Neo-Hookean(네오-후크)은 탄성 재료의 큰 변형을 예측하는 가장 일반적인 비선형 초탄성 모델 중 하나이다.

이 모델의 energy density function(Ψ)은 아래와 같다.

![](https://blog.kakaocdn.net/dna/cbnr9f/btsMB8wTXI5/AAAAAAAAAAAAAAAAAAAAABRBryuEtu4svu2e8arQYn8y2RmbdkokDAYM_L_W4L0A/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=c8G%2FTeygI5BKCKmOsbt9vBvtSeE%3D)

**μ와 λ는** 

**Young’s modulus E** 와 **포아송 비(Poisson’s ratio)****ν**와 다음 관계를 가진다.

![](https://blog.kakaocdn.net/dna/czKEIB/btsMBGub0Ud/AAAAAAAAAAAAAAAAAAAAAAGHDFQ6JvIrP7ipDEy_o-DhlNxA3mppyet4amJNjRon/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Ii9Cxe47t4O%2BwtnrtO8e20%2BFP3M%3D)

만약

**F(defomration gradient)가 회전만 있다면, Ψ(F) = 0이 된다.**

**Ψ(F)는 inverted가 아닌이상 0보다 크다**

**에너지 밀도 함수는 초탄성 재료를 설명하기에 적절**하다.

힘을 계산하기 위해서는 **P를 F의 함수로 도출**해야 한다.

Neo-Hookean는 좌측으로 구할 수 있는데, 식을 정리하면 우측으로 된다.

![](https://blog.kakaocdn.net/dna/brHvxt/btsMEmn9j0X/AAAAAAAAAAAAAAAAAAAAALOOdoxeo7fB_dNUXNAO9SF5lmaoqC7lxN4BUFKTpHEs/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=CsswwKhzu9lqW0zFCy6l4XSAvVc%3D)![](https://blog.kakaocdn.net/dna/ctBgix/btsMA5uqF5H/AAAAAAAAAAAAAAAAAAAAAGlphk3YSivWPeL3XXko8PSR_CUmEtBt2LObSja3OEKt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=gp9h6Iazl%2B30kyiPPGK6x7JtC5Q%3D)

### **10.1 APIC( Affine Particle in Cell)**

**APIC(Affine Particle-In-Cell) 입자를 격자로 변환할 때 추천되는 방법이다.**

Particle에서 Grid로 변환하는 방법이다.

![](https://blog.kakaocdn.net/dna/cmxG4O/btsMD3br6rw/AAAAAAAAAAAAAAAAAAAAAPOnQccywBSgHj3mzlO5wd-PEP87Ch6OT_1AzURfGUaP/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=XrF0XWSUwMhYoY0Aj28u8l4CRDY%3D)

**B는 질량, 위치, 속도와 같은 것이 저장된 matrix이다.**

**D는 아래와 같이 정의된다.**

![](https://blog.kakaocdn.net/dna/bMsowk/btsMDJYVvFG/AAAAAAAAAAAAAAAAAAAAAEXxj4FMwWiE6DTXRapX_xVpvAJjJbvInFvuUgHskQNT/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=MkOvnBexVhPvjl4sNzEJdJw6%2Fg0%3D)

그리고 변환 과정에서 Affine motion이 보존된다.

**Affine motion(linear + tranlation)**

코드로 구현할 때 아래 항을 C로 구현했다.

![](https://blog.kakaocdn.net/dna/briSJw/btsMFlXyGJ0/AAAAAAAAAAAAAAAAAAAAAJM06vCUezbN85QN9EUsMpZRMo44nJyVo2ICaL0ENLyR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=WYL3R8DP3yvwmcxOe7mKFin8ZEg%3D)

B는 아래와 같이 구현했다.

![](https://blog.kakaocdn.net/dna/llc7u/btsMEMIaYh0/AAAAAAAAAAAAAAAAAAAAABoRPNMyj5jJlee7CB9JITXsifdHpcrTCDxgxzDmmfE2/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hhtFWpdqK5vxzOcKgAVIH5sEBZE%3D)

```
                    weighted_velocity = grid[c_idx].vel * weight 
                    term = weighted_velocity.outer_product(cell_dist.xy)
```