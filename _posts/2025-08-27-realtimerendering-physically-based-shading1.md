---
title: "[RealTimeRendering] Physically Based Shading(1)"
date: 2025-08-27
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

NPR 부분을 읽어보려다가 PBR먼저 정리하고 가면 좋을 것 같아서

Physically Based Shading을 한 번 정리해보려고 합니다.

### 

### **Physics of Light**

빛과 물질의 상호작용은 물리 기반 셰이딩의 토대를 이룬다. 이러한 상호작용을 이해하려면 빛의 본질에 대한 기본적인 이해가 필요하다.

**물리학에서 광학은 빛을 전파의 방향에 직각인 전기장**과 **자기장을 진동시키는 횡방향(가로) 전자기파로 모델링한다**.

두 장(field)는 서로 수직이고, 비율은 고정이다.(비율은 phase velocity(위상 속도)에 해당한다.)

![](https://blog.kakaocdn.net/dna/bfqXD7/btsP6dOGPRP/AAAAAAAAAAAAAAAAAAAAAPyUIFUbd2JmriEuUbcp2oNx-p1ug6gLks836fr79zyc/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=mt%2BgvuylPqaFRF0iBLqRC5IwcjQ%3D)

그림에서는 단순한 빛의 파동을 볼 수 있다. 사실상 가장 단순한 형태로, 완벽한 sine 함수 모양이다. 이 파동은 하나의 파장만 가지며, λ(람다)로 표기한다.

또한 위의 그림은 **linearly polarized(선형 편광)**되어 있기다. 이는 공간에서 한 점을 고정했을 때, 전기장과 자기장이 각각 한 직선을 따라 앞뒤로 진동한다는 뜻이다. 하지만 이 책에서는 훨씬 더 흔히 존재하는 **unpolarized(비편광 빛)**을 다룬다

![](https://blog.kakaocdn.net/dna/cm8vyt/btsP6ToUYjJ/AAAAAAAAAAAAAAAAAAAAAArYX2WUd6J7VmH04xP1iwr8-0iLqnQ8m7Mge3-SroCS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2BfQmTGRTXYAE1mg96O0utLDcmnM%3D)

빛의 인지된 색은 파장과 밀접하게 관련된다.

빛의 색깔은 파장과 밀접한 관련이 있다. 따라서 하나의 파장만 가진 빛을 **monochromatic light(단색광)** 이라고 부른다.

실제로 우리가 접하는 대부분의 빛은 다양한 파장을 포함하는 **polychromatic light(다색광)** 이다.

파동의 위상(진폭의 꼭대기)을 기준으로 특정 지점을 시간에 따라 추적하면, 공간을 일정한 속도로 이동하는데, 이때의 속도를 **phase velocity(위상 속도)**라 한다.

(진공에서 빛의 phase velocity는 약 **초속 30만 km**, 즉 **빛의 속도(c)** 로 알려져 있다.)

빛 파동은 에너지를 운반한다. **에너지 흐름의 밀도**는 **전기장과 자기장의 크기의 곱에 비례하는데**, 이때 **두 장의 크기는 서로 비례**하므로 **결국 전기장의 크기 제곱에 비례**한다.

(물질에 더 강하게 작용하는 것은 전기장이므로, 우리는 주로 전기장에 주목한다.)

렌더링에서는 시간에 따른 평균적인 에너지 흐름에 관심을 두는데, 이는 **파동 진폭 제곱에 비례**한다. 이 평균 에너지 흐름 밀도를**irradiance(조도)** 라 하며, 보통 E로 표기한다.

빛 파동은 선형적으로 합성된다. 즉, 전체 파동은 개별 파동의 합이다. 그러나 **irradiance는 진폭 제곱에 비례하므로, 단순히 파동을 합치면 “1 + 1 = 4” 같은 역설이 생기는 것처럼 보인다.**

**그렇다면 동일한 두 파동을 합치면 조도가 네 배가 되는 것이 아닌가? 그렇다면 에너지 보존 법칙을 위반하는 것 아닐까?** 이에 대한 답은 각각 “경우에 따라 다르다”와 “아니다”이다.

![](https://blog.kakaocdn.net/dna/cn3t9N/btsP6UWt7uj/AAAAAAAAAAAAAAAAAAAAACfG8MiWjb6hBEVNDeosTnMi85JxshI_p01GyEmQvrZQ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=NDIgOBVAgT8CCOxxhHEcaWoehPo%3D)

위 그림의 왼쪽(보강간섭)과 오른쪽(상쇄간섭)을 보면 에너지 보존 법칙을 위반하는 것 처럼 보인다.

하지만 위의 그림은 국소적(어떤 한 어떤 부분만을 줌 인해서 보는 것)으로 보는 것이다.

전체 공간을 평균적으로 보면,

![](https://blog.kakaocdn.net/dna/bLBqVS/btsP5ET70OO/AAAAAAAAAAAAAAAAAAAAADVl-XJfhlMe6MU_aMLwEvQxdXKhBijop1A-OrTkte1m/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=QMNrSaJLNbDpKBgRw3o2YHDfwFE%3D)

보강으로 얻는 에너지와 상쇄로 잃는 에너지가 서로 균형을 이루기 때문에 총 에너지 합은 변하지 않고 보존된다.

**빛의 방출**

1. 빛은 물체 안의 전하가 진동할 때 방출된다.

2. 물체 안의 전하가 진동할 때, 에너지(열, 전기 에너지, 화학 에너지)의 일부가 빛 에너지로 변환되서 물체에서 방출된다.

3. 렌더링에서는 이를 light source(광원)이라고 한다.

**빛의 산란**

1. 방출된 빛은 공간을 따라 이동하다가 결국 어떤 물질과 부딪힌다.

2. 이때 빛의 **전기장**이 물질 속의 전하를 흔들어서 다시 진동시킨다.

3. 이 전하가 새로운 빛 파동을 방출한다.

이렇게 원래 빛의 에너지가 다른 방향으로 흩어지는 걸 **scattering(산란)** 이라고 한다.

**주파수 보존**

1. 산란된 빛은 보통 **원래 빛과 같은 주파수(같은 색)** 를 유지한다.

파란빛이 산란된다고 해서 그 에너지가 갑자기 빨간빛으로 바뀌지는 않는다.

(형광(fluorescence) 과 인광(phosphorescence) 같은 특수 현상이 그 예지만, 이 책에서는 이를 다루지 않는다.)

2. 빛이 여러 파장(색)을 섞어서 가진 경우라면, 각 파장은 **독립적으로 따로** 산란된다.

(파 +빨 빛이 산란될 때는, 파랑 빛대로 산란되고 빨강 빛대로 산란된다. 섞여서 산란되는게 아님)

**고립된 분자의 산란**

1. 단 하나의 분자에 빛이 부딪히면, 빛은 거의 **모든 방향으로** 산란된다.

2. 강도는 균일하지 않고, 원래 빛이 진행하던 축의 앞뒤 방향으로 더 강하다. 또한 산란율은 파장에 크게 의존한다.  
=> 짧은 파장(파란빛) 은 긴 파장(빨간빛) 보다 훨씬 강하게 산란된다.  
=> 이 원리 때문에 대기가 태양빛의 파란 부분을 많이 산란시켜 하늘이 파랗게 보인다(레일리 산란).

**다수의 분자 집합에서의 산란**

1. 실제로 렌더링이나 물리학에서는 **단일 분자**가 아니라 **많은 분자들의 집합**을 다룬다.

2. 인접한 분자들이 같은 입사광에 의해 동시에 산란하면, 파동들이 서로 **간섭 현상**을 일으킬 수 있다.

3. 따라서 집합적인 산란 현상은 단일 분자의 단순한 산란과는 달라진다.

이 책의 다음 부분에서는 이러한 다수 분자 산란의 특수 사례들을 다루게 된다.

### 

### **Particles**

**입자(particle)** 라는 용어는 단일 분자뿐 아니라 여러 분자가 뭉친 집합체도 모두 포함하는 단어이다.

ideal gas(이상기체)에서는 분자들이 서로 영향을 주지 않으므로, 분자들의 상대적 위치는 완전히 무작위이고 서로 상관관계가 없다. 이는 추상화된 모델이지만, 정상적인 대기압의 공기를 설명하기에는 꽤 적합하다.

### 

### Ideal Gas (기체 속 분자들이 따로 있는 경우)

서로 다른 분자에서 산란된 파동들 사이의 phase(위상)이 무작위적이며 끊임없이 변한다. 그 결과, 산란파들은 **incoherent** 상태가 되고, **에너지는 단순히 선형적으로 합쳐진다. (간섭이 없음)**

**=> 결국** **n개의 분자에서 산란된 총 빛 에너지는, 단일 분자가 산란한 빛의 n배**에 해당한다.

### 

### cluster로 뭉쳐있는 경우 (cluster 크기가 파장보다 작을 때, Rayleigh Scattering)

**거시적 관점으로 볼 때는** 개별 분자가 만드는 산란 자체가 매우 약해서, 멀리서 보면 산란이 잘 안 나타난다. **(대부분 투과)**

**하지만 산란이 일어날 때를 보면,**

cluster 내부의 모든 분자들이 거의 동시에 같은 phase(위상)으로 빛을 산란 시킨다.

그 집합 내의 산란파들은 서로 phase가 이 일치하여 보강 간섭(constructive interference)을 일으킨다.

=> 이때 산란된 파동의 에너지는 **제곱(n²)** 으로 합쳐진다.

### 

### cluster로 뭉쳐있는 경우 (cluster크기가 파장에 가까워 질 때, Mie Scattering)

cluster가 점점 커지면, 이제 입자 내부에서 **위상이 완벽히 맞지 않게 됨**.

간섭 효과는 점점 줄어들고, 산란 특성이 바뀐다.

=> 전방향(앞쪽)으로 산란이 강해지는 **미 산란(Mie scattering)** 으로 넘어가게된다.

정리하면

**1. Rayleigh scattering (레일리 산란)**

빛의 산란을 논할 때,  입자의 크기가 파장보다 작을 때 산란은 **보강 간섭으로 증폭된 형태**이고, 여전히 동일한 방향적 특성과 **파장 의존성을 가진다.**

이런 산란은 대기 중 입자의 경우 **레일리 산란(Rayleigh scattering)** 이라고한다.

**2. Mie scattering (미 산란)**

입자의 크기가 빛의 파장을 넘어설 정도로 커지면, 더 이상 입자 전체에서 산란파들이 위상이 일치하지 않게 된다.

그 결과 **전방향 산란(forward scattering)** 이 강해지고, **파장 의존성은 줄어들어** 가시광선 모든 파장이 거의 동일하게 산란된다.

이러한 산란을 **미 산란(Mie scattering)** 이라고 한다.

**파장 의존성이란??**

산란의 세기가 빛의 파장에 따라 얼마나 달라지는 가를 의미하는데,

**Rayleigh Scattering은 파장 의존성을 가진다 => 파장이 짧을수록 많이 산란되고, 파장이 길 수록 덜 산란된다.**

**Mie Scattering은 파장 의존성이 거의 없다 => 모든 파장이 비슷하게 산란된다 => 구름, 안개가 흰색으로 보인다.**

### 

### **Media**

빛이 homogeneous medium(균질 매질)을 통과하는 경우도 중요하다.  
homogeneous media란, 동일한 분자가 일정한 간격으로 고르게 분포한 부피 공간을 말한다.

이 간격은 반드시 결정(crystal)처럼 완벽히 규칙적일 필요는 없고, 기포나 틈이 없다면 광학적으로는 homogeneous media로 취급할 수 있다.

homogeneous media 에서는 개별 분자에서 나오는 산란파들이 정렬되어, 원래의 진행 방향을 제외한 모든 방향에서는 서로 **상쇄 간섭**을 일으킨다. 즉, 산란은 눈에 보이지 않고 사실상 억제된 것처럼 된다. (phase velocity, 진폭만 달라짐)

### 

### 굴절률과 흡수

광학적 성질인 **굴절률**(n)은 **원래 파동과 새로운 파동의 phase velocity 비율**이다.

일부 매질은 **흡수성**(absorptive) 을 가진다.

**빛 에너지 일부를 열로 바꾸어 파동의 진폭이 거리와 함께 지수적으로 줄어든다.**

이 감소율은 **감쇠 계수(attenuation index)** 라 하며, 그리스 문자 κ(카파)로 표기한다.

n과 κ는 보통 파장에 따라 달라진다. 두 값을 합쳐 **복소 굴절률(complex index of refraction)** 이라 부르는 복소수 n+iκ 로 표현한다.

![](https://blog.kakaocdn.net/dna/l5YYz/btsP8c3nXin/AAAAAAAAAAAAAAAAAAAAAIU0G0AnKP5mBcjcRLJA9MnMr3PzLFJ79ES0DX5ujzry/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=mL9%2BIB0MhwUFHWulbPg7JoD8C6E%3D)

서로 다른 흡수율을 가진 액체들 (물, 시럽, 차, 커피)

**위상 속도** 자체는 직접적으로 외관을 바꾸지 않지만, 속도의 변화는 외관에 영향을 준다. (이후에 설명할 예정)

**흡수**는 빛의 세기를 줄이고, 파장별로 다르면 색조까지 바꿀 수 있기 때문에 외관에 직접적인 영향을 준다. (위의 이미지를 보면 알 수 있다.)

### 

### Nonhomogeneous media(비균질 매질)과 Scattering

nonhomogenous media(비균질 매질)는 homogenous(균질 매질) 속에 산란 입자( 다른 종류의 분자 클러스터, 기포, 밀도 변화) 가 들어있는 경우로 볼 수 있다.

균질 매질에서 산란이 억제되는 이유는 분자들이 균일하게 배열되어 산란파가 상쇄되기 때문이다.

그러나 **비균질 매질에서는 분자 분포에 국소적 변화가 생기면 이 패턴이 깨진 산란이 발생한다**.

![](https://blog.kakaocdn.net/dna/rNubi/btsP6glmWr4/AAAAAAAAAAAAAAAAAAAAAFjI8KH2-gEgRv5Xq4vQfngF0M-kcSPrHvaFfPoaT4U5/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=M80DPDnprHu1vNldlwN8Sf8Kdcw%3D)

물, 우유가 조금 섞인 물, 10% 우유, 전지방 우유, 유백색(opalescent) 유리를 보여주며 산란 차이를 설명한다.

### 

### Scale Dependent

Scattering과 absorptive는 **스케일 의존적**이다.

작은 스케일: 방 안에서 컵에 든 물 => 산란/흡수 거의 안 보임.

큰 스케일: 바다(흡수) / 대기(산란) => 뚜렷한 효과

![](https://blog.kakaocdn.net/dna/c9o7I2/btsP8yLVXjS/AAAAAAAAAAAAAAAAAAAAADl1p_1M1sSd4plqU5H1zDN1E5iDG1GRUAu4Ty3rJ6Qf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=7vCpWzuwFwqo8y8CRtMBhzRTXiw%3D)

왼쪽: 물이 수 미터 깊어지면 빨간빛 흡수가 강하게 나타남.

오른쪽: 대기에서도 수 마일 정도 스케일이면 산란이 분명히 보임(안개·오염 없어도).