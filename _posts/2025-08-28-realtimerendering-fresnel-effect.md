---
title: "[RealTimeRendering] Fresnel Effect"
date: 2025-08-28
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

## 

## **Illumination (조명)**

전역 조명은 BRDF가 끝난 이후의 장에서 따로 다룬다.

이 장과 다음 장에서는 각 표면 지점에서 반사 방정식을 사용해 local illumination(로컬 조명)에 초점을 맞춘다.

로컬 조명 알고리즘에서는 Li(l)L\_i(l)Li​(l)이 주어진 것으로 간주되며 따로 계산할 필요가 없다.

현실적인 장면에서 Li(l)은 모든 방향으로부터의 0이 아닌 휘도를 포함한다.

실제 세계의 광원은 점 광원이 아닌 **면 광원**이다.

이 장에서는 논의를 집중하기 위해 Li(l)을 **방향성 및 점 광원**으로만 제한된 형태로 사용하고, 보다 일반적인 조명 환경은 이후 장에서 따로 다루겠다.

방향성/점 광원은 물리적으로 정확한 모델은 아니지만, 물리적 광원을 근사한 것으로 유도할 수 있다. 이러한 유도는, 관련 오차를 이해한 상태로 이 광원들을 물리 기반 렌더링 프레임워크에 편입할 수 있게 해준다는 점에서 중요하다.

작고 멀리 있는 한 면 광원을 생각하자.

그 중심을 가리키는 벡터를 lc​라 하고,

광원의 색 clight​는, 광원을 향해 마주 보는(n=lc​) White Lambertian Surfacee으로부터 반사된 휘도로 정의한다.

이 정의들 하에서, clight를 유지하면서 광원의 크기를 0으로 수축시키면 적분을 단일 BRDF로 단순화할 수 있다.

(계산 비용이 크게 낮아진다)

![](https://blog.kakaocdn.net/dna/sHiFR/btsP8jPIqjB/AAAAAAAAAAAAAAAAAAAAAO92FVtwK44rUCi6wZhYTqF9SVKc7jFqwzkzI9PSsATs/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=QJv6AIAcAMzludccPk3nOIOUyc8%3D)

(+의 의미는 0이하의 값을 갖지 않도록 clamping해준다는 의미)

pi가 등장한 이유

더보기

Clight는 아래와 같이 얻어질 것이데,

![](https://blog.kakaocdn.net/dna/QRy3I/btsP81A2yzw/AAAAAAAAAAAAAAAAAAAAAFXR1J5ATbE4Kw5qDbe4MKPdkzzvfaWzceNvWGltgWdb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=adPzN2n1cuBXQTsV0BCF%2BDqQm9k%3D)

이를 반사 방정식에 대입하면 pi가 생긴다

![](https://blog.kakaocdn.net/dna/cNqd1B/btsP8upXN9n/AAAAAAAAAAAAAAAAAAAAAJNJHhK5ogXFAuV6mdn-SUOLolM8DO_ZdaPSfzunU3GR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=PucYvvE%2BfbwHnqBnM8YbBRpA3d8%3D)

## 

## **Fresnel Reflectance**

처음 논의했던 **평탄한 표면에서의 반사**부터 시작한다.

두 물질 사이의 **평면 경계면**과 빛의 상호작용은  **프레넬 방정식**을 따릅니다.

프레넬 방정식은 **geometrical optics**가정 하에서 **평탄한** **경계면을 요구합니다**.

이 말의 의미는 표면에는 빛의 파장 1배에서 100배 크기 사이에서 불규칙성이 없다는 가정입니다.

(이보다 작은 불규칙성은 빛에 영향을 주지 않고, 더 큰 불규칙성은 사실상 표면을 기울이는 효과만 있을 뿐 **국소적 평탄성**에는 영향을 주지 않는다.)

![](https://blog.kakaocdn.net/dna/b0aCqK/btsP6asy9yN/AAAAAAAAAAAAAAAAAAAAAI48XPfIveIE_JXtA1SB6Rbd4TjlsennC3Y9oPQuuMbT/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=L1VR%2BRXNVezCLI%2BRPtW3n%2FpdETA%3D)

평탄한 표면에 입사한 빛은 **반사 성분(reflected part)**과 **굴절 성분(refracted part)**로 나뉩니다.

반사된 빛의 방향(벡터 ri​)은 입사 방향 l과 동일한 각도 θi로 표면 법선 n에 대해 대칭을 이룹니다.

반사 벡터 ri​는 n과 l을 활용해서 계산할 수 있습니다.

![](https://blog.kakaocdn.net/dna/b2Pkjg/btsQa6ohWoG/AAAAAAAAAAAAAAAAAAAAANm0kAUqk0WlGzowfQmjAgMDO5YImDjP6Usg2Ua-BNrq/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=OTTLy37E3o5n7%2FYzEZYxHqZMpBk%3D)

반사되는 빛의 양(입사광 대비 비율)은 **프레넬 반사율** F로 기술되며, 이는 입사각 θi에 의존한다.

반사와 굴절은 경계면 양쪽 물질의 굴절률(refractive index)에 의해 영향을 받는다.

프레넬 방정식은 F가 θi​, n1, n2에 어떻게 의존하는지 기술한다.

방정식 자체는 다소 복잡하므로 여기서는 이를 직접 제시하기보다는, **핵심적인 특성들**을 서술하는 방식으로 설명하겠다.

### 

### **External Reflection**

external reflection

n1 < n2 인 경우를 의미한다.

=> 빛이 굴절률이 더 낮은 쪽, 큰 쪽으로 이동할 때. 대부분 n1은 공기이며, 굴절률은 약 1.003 정도이다. 단순화를 위해 n1 = 1이라고 가정하자

internal reflection

물체에서 공기 쪽으로 가는 경우이고, 다음 주제로 다루겠다.

**특정 물질에 대해, 프레넬 방정식(Fresnel equations)은 입사광의 각도에만 의존하는 반사 함수 F(θi)를 정의한다고 해석할 수 있다.**

렌더링에서는 이 값을 **RGB 벡터**로 처리한다.   
(원칙적으로 F(θi)의 값은 가시광선 스펙트럼 전반에 걸쳐 연속적으로 변한다.)

F(θi) 함수는 다음과 같은 특성을 가진다.

**1. θi = 0도 일 때 (빛이 표면에 수직으로 들어올 때, normal incidence)**

F(θi)는 물질의 특성 값을 가게된다. 이 값 F0은 물질의 특징적인 specular color로 생각할 수 있다.

반사를 거의 안한다는 의미

**2. θi가 증가하고 빛이 점점 더 비스듬히(glancing angles) 표면에 닿을수록,**

F(θi)의 값은 점점 증가하며, θi = 90도일 때 모든 파장에서(흰색) 1에 도달한다.

반사율이 1이라는 의미

![](https://blog.kakaocdn.net/dna/8QRp4/btsQafTNnWK/AAAAAAAAAAAAAAAAAAAAAA7Vtz4B6V9W3MXiW5MmUrjuaClv5vFEm1zQr1vdjUo7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=0bp094LfS%2BpDWazwYFyS4zGZgXo%3D)

유리, 구리, 알룰미늄 순이다.

위의 그림은 여러 물질에 대해 F(θi) 함수를 다양한 방식으로 시각화한 것이다.

곡선들은 매우 비선형적이며, θi = 75도 정도까지는 거의 변하지 않다가 이후 급격히 1로 올라간다.

(알루미늄은 특이하게 1로 가기 직전에 약간 하락하는 모습을 보인다.)

거울 반사의 경우, outgoing 각도는 입사각과 동일하다.

=> 입사하는 빛이 표면에 비스듬히 닿는다면, 반사도 같은 각도로 발생한다는 의미이다.

빛의 값 θi가 90도에 가까울수록, 즉 비스듬히 들어올수록 눈에도 비스듬히 보인다.

이 때문에 반사율 증가 현상은 주로 물체의 가장자리에서 관찰된다.

또한 반사율 증가가 가장 강하게 일어나는 표면 부분은 실제 화면에서 차지하는 픽셀 수는 상대적으로 적다.

![](https://blog.kakaocdn.net/dna/INOK5/btsP98AFYYZ/AAAAAAAAAAAAAAAAAAAAAL-ekIfk7AFRVfp2XyAkcv_SeP0yMmgwnmZMnlGRjc5c/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=0M%2Ferx51YE69w1UI6H6Co44wLkA%3D)

표면부분에 가까워질 때쯤 값이 급상승

이 시점부터는, 프레넬 함수를 F(θi) 대신 F(n, l)로 표기하는데, 이는 관련된 벡터들을 강조하기 위함이다.

θi는 n과 l 벡터 사이의 각도임을 기억하라.

(Fresnel 함수가 BRDF의 일부로 포함될 때는, 표면 법선 n 대신 다른 벡터가 대체되는 경우가 자주 있는데, 이후 내용에서 다루겠다.)

프레넬 방정식은 복잡할 뿐만 아니라, 직접 렌더링에 사용하는 데 어려움이 있다.

가시광선 스펙트럼 전반에서 굴절률 값을 샘플링해야 하고, 이 값들은 복소수일 수도 있다.

![](https://blog.kakaocdn.net/dna/brATlY/btsP99l4Afc/AAAAAAAAAAAAAAAAAAAAAEcv8fXPbB1uWL4DfNTGAjks2N1XbZQLjqOHKF0WWbkv/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=K1D%2FEb61r4erWPgYpwfPYOHbZ8w%3D)

각도에 따른 반사율

위 그림의 곡선들은 물질의 특징적 스펙큘러 색 F0에 기반한 더 단순한 접근을 제안한다.

Schlick은 Fresnel 반사율에 대한 근사식을 제시했다.

![](https://blog.kakaocdn.net/dna/rPcO7/btsP99zBftX/AAAAAAAAAAAAAAAAAAAAANS1vgHpEKOxx5SoTQ6-YG9jopxNjgNNkKsBkW1zrKHh/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=SPbVLNbWaN2f3MkQl%2FNkdaYZcNA%3D)

이 함수는 F0와 흰색 사이의 RGB 보간으로 볼 수 있다. 단순하지만 근사치는 꽤 정확하다.

![](https://blog.kakaocdn.net/dna/nT0yV/btsQbaLikCt/AAAAAAAAAAAAAAAAAAAAAPUbEVKTm6Q15JApO1TMTiGvrrYlQKx2L2QVMyudcTvM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=WO5Kjf3Tb0v4l8dXYNEf%2FuvVVeI%3D)

위의 그림은 실제 Fresnel 값(실선)과, 근사한 Schilk Fresnel 값(점선)을 비교한 그래프이다.

큰차이 없이 잘 근사하고 있음을 볼 수 있다. 하단에 있는 그래프는 1.0에 도달하기 전에 값이 하락했다가 증가해서, 근사값과 차이가 꽤 발생한다.

하지만 그래프 아래 색 막대로 실제 색을 비교해보면 큰 차이가 없음을 알 수 있다.

( 이런 사소한 오차도 허용할 수 없는 환경이라면, Gulbrandsen이 제안한 다른 근사식을 사용할 수 있지만, Schlick의 방법보다.

오히려 더 단순하게 만드는 방법은 Schlick 근사의 마지막 항의 거듭제곱 지수를 5가 아닌 다른 값으로 바꾸는 것이다.)

Schlick 근사를 사용할 때, **F0는 프레넬 반사율을 제어하는 유일한 파라미터입니다**.

F0는 [0, 1] 범위의 유효 값을 가지며, 실제 물질들에 대한 F0기준 값이 많이 존재합니다. 굴절률로부터도 F0를 계산할 수 있습니다.

n1 = 1이라고 가정하고(공기 굴절률), . n2를 n으로 표현하면 F0을 구하는 간단한 식을 얻을 수 있습니다.

![](https://blog.kakaocdn.net/dna/bGwGgc/btsP9MRYSJt/AAAAAAAAAAAAAAAAAAAAAF-SIcjB4oOcALUBQMvSUSivtex-BUAxlu0iKiZSXeGU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=p%2FQAHPs33XhVtxWiIxt9ui8e%2Bh4%3D)

일부 응용에서는 Schlick근사의 더 일반화된 형태가 사용됩니다.

![](https://blog.kakaocdn.net/dna/6emhc/btsP8MkGLMA/AAAAAAAAAAAAAAAAAAAAAL94TP797erISPdjB8SwCnj0zGDYSLDMbdBQHr6giEF1/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fwoyeecufUU2ACFZ4ps79l8ZzmQ%3D)

이 식은 θi = 90도 에서 Fresnel 곡선이 전환되는 색상(F90)과 그 전환의 sharpness을 제어할 수 있습니다.

( 지수를 수정하면 특정 물질에 더 잘 맞출 수 있습니다. 또한 F90을 흰색이 아닌 다른 색으로 설정하면, 미세한 먼지로 덮인 표면처럼 프레넬 방정식만으로는 잘 설명되지 않는 물질을 더 잘 표현할 수 있습니다.)

### 

### **Typical Fresnel Reflectance Values**

물질은 광학적 성질에 따라 크게 세 그룹으로 나눌 수 있다.

**1. 절연체(dielectrics)**: 비전도체

**2. 금속(metals)**: 전도체

**3. 반도체(semiconductors)**: 절연체와 금속 사이의 특성을 가짐

#### 

#### 절연체의 프레넬 반사율 값 (Fresnel Reflectance Values for Dielectrics)

일상에서 마주치는 대부분의 물질은 절연체이다. (유리, 피부, 나무, 머리카락, 가죽, 플라스틱, 돌, 콘크리트 등

물 또한 절연체에 속한다. 이는 다소 놀라울 수 있는데, 일상적으로 물은 전기를 통한다고 알려져 있기 때문이다. 그러나 이러한 전도성은 다양한 불순물에 기인한다.)

절연체는 보통 F0 값이 낮으며(보통 0.06 이하).

이러한 낮은 법선 입사(normal incidence) 반사율 때문에, 절연체에서 **프레넬 효과**가 특히 두드러지게 보인다.

=> F0값이 낮다는 것은 대부분의 빛이 표면을 통과한다는 의미, 내부에선 산란/흡수된다.

또한 절연체의 광학적 성질은 가시 스펙트럼에서 거의 변하지 않으므로, 반사율은 무채색으로 나타난다.

![](https://blog.kakaocdn.net/dna/bCdCJ2/btsQa3ZUVZk/AAAAAAAAAAAAAAAAAAAAAK3YZ37d6sF4LIFDvy3aDDqol8j37LAKmPHyN-WkbMH3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=psAHAQyoc2C8ZJUQJIBo8h8Nv7U%3D)

위의 표는 여러 일반적인 절연체의 F0 값을 보여준다.

F0을 RGB가 아니라 스칼라 값으로 표시하는 이유는 각 채널 간 차이가 미미하기 때문이다.

(표에 없고, 알 수 없는 절연체의 기본값으로 0.04를 사용하는 것이 합리적이다. 이는 대부분의 일반적인 물질과 크게 다르지 않다.)

#### 

#### 금속의 프레넬 반사율 값 (Fresnel Reflectance Values for Metals)

금속은 F0 값은 높다(대부분 **0.5 이상)**

일부 금속은 가시 스펙트럼에서 광학적 성질이 변하므로, 유색 반사율(colored reflectance)을 보인다.

![](https://blog.kakaocdn.net/dna/bkqjuk/btsQaaLYWT0/AAAAAAAAAAAAAAAAAAAAANItOSMozx1PoDldfXKSJ03CbnbMIH9nRnr2IAu8l7QB/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=qZmgSNVJtkPUhSapODuXZ7QxwDI%3D)

위의 표는  여러 금속의 F0 값을 보여주며, 밝기(lightness) 순으로 정렬되어 있다.

금속은 유색 반사율을 가지므로 RGB 값으로 표현된다.

특히 금(gold)의 F0 값은 독특하다. 빨강 채널 값이 1을 약간 넘어서고, 파랑 채널 값은 특히 낮다(표에서 유일하게 0.5 이하).

( 금속은 내부로 투과된 빛을 곧바로 흡수하므로, subsurface scattering이나 transparency을 보이지 않는다.

금속의 모든 가시 색은 F0에서 나타난다. )

#### 

#### 반도체의 프레넬 반사율 값 (Fresnel Reflectance Values for Semiconductors)

예상할 수 있듯이, 반도체의 F0 값은 가장 밝은 절연체와 가장 어두운 금속 사이에 위치한다.

![](https://blog.kakaocdn.net/dna/bfDRNh/btsP89mv0lN/AAAAAAAAAAAAAAAAAAAAAPAxYXPQ8EXYE5wwpFUDoS_H-e2L-BjFJ7RK5LVZ-rH7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=VRuRb7SAk%2BS%2FJMsKTs37eB3yc8U%3D)

그러나 실제로 이런 물질을 렌더링할 필요는 드물다. (온 세상이 다이아몬드, 실리콘 덩어리는 아니니..)

의도적으로 특이하거나 비현실적인 재질을 표현하려는 경우가 아니라면, **0.2 ~ 0.45 사이의 F0 값은 피하는 것이 좋다**,

#### 

#### 물속에서의 프레넬 반사율 값 (Fresnel Reflectance Values in Water)

지금까지 외부 반사에서는 표면이 공기에 둘러싸여 있다고 가정했다. 그러나 그렇지 않으면 반사율이 달라질 것이다.

(우리가 n1을 1이라고 가정하고 식을 만들었으니까)

n1이 공기가 아니라면 식을 아래와 같이 수정해야된다.

![](https://blog.kakaocdn.net/dna/b3QnOk/btsQa6hYlBx/AAAAAAAAAAAAAAAAAAAAAECR7SQrmWjpEjNFqX5MhZG8tm6VBowrT4DwB3RWDpAr/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=dbIaJlB%2BDe72CVBUmRbNV%2B3UGfE%3D)

주로 수중 장면을 렌더링할 때 자주 나타난다.

#### 

#### **Parameterizing Fresnel Values**

자주 사용되는 파라미터화 방식은 **스펙큘러 색 F0**와 **확산 색 ρss**를 조합하는 것이다.

이 방식은 다음과 같은 관찰에 기반한다.

1. 금속은 diffuse color이 없고,

2. 절연체는 F0 값이 제한된 범위를 가진다.

**이 파라미터화는 RGB 표면 색(c\_surf)와 스칼라 파라미터 m(metallic, metalness)을 포함한다.**

**1. m = 1일 때, F0 = c\_surf, ρss = 검정**

**2. m = 0일 때, F0 = 절연체 값(상수 또는 별도 파라미터로 제어), ρss = c\_surf**

렌더링 애플리케이션들이 F0와 ρss 대신 metalness 파라미터화를 사용하는 이유는 **사용 편의성과 텍스처/G-buffer 저장소 절약** 때문이다.

**하지만 metalness 방식에는 단점도 있다.**

1. 색이 있는 F0 값을 가진 코팅된 절연체(coated dielectrics) 같은 재질은 표현할 수 없다.

2. 금속과 절연체 경계에서 아티팩트가 생길 수 있다.

### 

### **Internal Reflection**

외부 반사가 렌더링에서 더 자주 나타나지만, 내부 반사 또한 중요한 경우가 있다.

internal reflection는 **n1 > n2**일 때 발생한다.

=> 빛이 투명한 물체의 내부를 이동하다가 물체의 표면을 **“안쪽에서”** 만나게 될 때 발생한다

![](https://blog.kakaocdn.net/dna/dWmYN6/btsQabRHJUI/AAAAAAAAAAAAAAAAAAAAAARVCgTK39529VlhiBRSIExkrRUFeVQQ46ix7kWm8weZ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1lcowVnkVUk1lRenNR2EyHpoOBU%3D)

스넬의 법칙(Snell’s law)의 **internal reflection의** 경우 아래와 같다.

![](https://blog.kakaocdn.net/dna/cP6rqT/btsQaUB4EWD/AAAAAAAAAAAAAAAAAAAAAJcHJvQqLiNXpwMLC7aofQjUqqrNMHvfar_DJrkIbgB2/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=5hxm1DL9LX3lAauC0YCYRIudlFA%3D)

​

θt와 θi는 모두 0도에서 90도 사이이므로,

결국 **θt > θi**임을 의미하는 것과 같다.

아래의 그림은 externla reflection이다. 두개의 그림을 비교해보면 차이가 느껴질 것이다.

![](https://blog.kakaocdn.net/dna/4okcS/btsP94ZzRFq/AAAAAAAAAAAAAAAAAAAAAGgX8DGG6wPgI8yBB2rDBahcUUwhKMrSKP1Ccec-HtLF/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=whO1dyQ5HMRRzzrbdrnm65j6iXc%3D)

**external reflection의 경우,**

모든 상황에서 sin⁡θi 보다 작은 sin⁡θt 값이 존재한다.

**하지만 internal reflection에서는 그렇지 않다**.

θi 값이 어떤 임계각 θc보다 크면, 스넬의 법칙은 sin⁡θt ​> 1를 만족해야 되는 상황이 발생하는데, 이는 불가능한 식이다.

실제로는 이때 θt 자체가 존재하지 않게되는 것이다.

**θi > θc일 때는 투과가 일어나지 않고, 모든 입사광이 반사된다.** 이 현상을 total internal reflection라고 부른다.

Fresnel 방정식은 대칭적이다.

즉, 입사 벡터와 굴절 벡터를 바꾸어도 반사율은 동일하다.

Snell's Law와 결합하면, internal reflection의 F(θi) 곡선은 external reflection의 곡선을 “압축한(compressed)” 형태임을 알 수 있다.

F0 값은 두 경우에서 동일하지만,

내부 반사 곡선은 90도가 아니라 임계각 θc에서 완전 반사(값=1, 반사율이 1에 도달)에 도달한다.

![](https://blog.kakaocdn.net/dna/eF75xX/btsP8E8fJS2/AAAAAAAAAAAAAAAAAAAAAEZrydFsoax4MmVCWsYgD1SdZ7VcGWpBc4YF3ndfDd2H/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=2uN64cYzuYe7wCIhc5Xl7gVwDUg%3D)

평균적으로 internal reflection의 경우 반사율이 더 높다는 것도 알 수 있다.

internal reflection은 절연체(dielectrics)에서만 발생한다. (금속과 반도체는 내부로 전파된 빛을 빠르게 흡수하기 때문)

더보기

절연체는 자유전자가 거의 없다. => 빛이 잘 돌아댕김

금속은 자유전자가 많다 => 빛이 대부분 반사 + 흡수

절연체는 굴절률이 실수이므로, 굴절률이나 F0로부터 임계각을 계산하는 것은 단순하다.

![](https://blog.kakaocdn.net/dna/bk7uIy/btsP9brbiLL/AAAAAAAAAAAAAAAAAAAAAEQIGI3V_PXIxECFnec5DHCEXFH24Xo6OkYjHfNKjeax/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=QcFLVeAYpGqu30g3GuAn6yaFs0g%3D)

Schlick 근사는 external reflection에 대해서는 정확하다.

internal reflection에도 적용할 수 있는데, 이때는 입사각 θi 대신 굴절각 θt를 대입해야 한다.

식을 보면서 설명하면

![](https://blog.kakaocdn.net/dna/cd2slN/btsP8YevCYN/AAAAAAAAAAAAAAAAAAAAAGmbXvf5s26RYwdfwk_EJJDGFxgQGWZ4WY3EHYx5FdB3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Avh%2BvsMlEPoCntgi6LKR%2FRkvzlg%3D)

dot(n, l)이 cos θi 를 의미하는 것이니, 입사각을 사용하고 있다고 말할 수 있는 것이고,

이를 θt로 바꿔줘야한다는 것이다.

더보기

만약 굴절 방향 벡터 t가 이미 계산되어 있다면, 이를 사용해 θt를 얻을 수 있다.

그렇지 않다면 스넬의 법칙을 사용해 θi로부터 θt를 계산할 수 있지만, 이는 계산 비용이 크고 굴절률 값이 필요하다. 또한 굴절률은 상황에 따라 사용 불가능할 수도 있다.

양이 많았기 때문에 전체적인 정리 

더보기

## 1. Fresnel Equcation

빛이 **두 매질의 경계면**에서 만날 때, 일부는 **반사(reflection)** 되고 일부는 **굴절(transmission)** 된다.

이때 반사되는 양은 **입사각 θi**와 **두 매질의 굴절률 (n1, n2)의 차이**에 의해 결정된다

![](https://blog.kakaocdn.net/dna/cXOWky/btsQabRG5Ev/AAAAAAAAAAAAAAAAAAAAAOWIcxFuU4MSASRaqp9jxDEqCcmuWtcwPuuW-E5mBEP-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ItUfl50cCwa2l4ZGKerM2pmQrKE%3D)
![](https://blog.kakaocdn.net/dna/bR7GT0/btsQafmfIv4/AAAAAAAAAAAAAAAAAAAAALojtkaiY8rluFBSs_7LcqtTUX87BJG2WOsuexa6QmVR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=mi8rqL1fgnITCF6AoWC4S97lNsQ%3D)

이를 수학적으로 기술한 것이 **Fresnel 방정식이다.**

## 

## 2. F0(Normal Incidence Reflectance)

θi=0도일 때 반사율을 **F0**라고 한다. (입사 각도가 0도일 때)

![](https://blog.kakaocdn.net/dna/3J9fV/btsP8Md4gJj/AAAAAAAAAAAAAAAAAAAAAB_kLlPowMmb9ju0ZF8jmHCpYyTpwcti1c_FJxAn8bcf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=2sCiiXlEqO4mpqAUMD%2FvClycFo0%3D)

대부분 성립한다. ( ray가 공기에서 시작할 때 )

굴절률 차이가 작으면 F0이 작아진다 => 대부분 투과

굴절률 차이가 크면 F0 커진다 =>정면에서도 강한 반사

## 

## 3. Fresnel Effect (입사각 의존성)

F(θi)는 각도에 따라 변하는 함수이다.

입사각에 따라서 F(θi) 값이 변화된다

0도일 때 => F0

90도 일 때 =>1에 가까워짐

표면은 정면에서는 반짝임이 약하지만, 가장자리에서 강하게 반짝인다.

이것을 Fresnel Effect라고 부른다.

## 

## 4. 절연체 vs 금속

**절연체 (Dielectrics)**

F0 값이 낮다. (대부분0.02~0.06), Fresnel 효과가 두드러진다.

무채색 반사가 나타난다.

색은 subsurface scattering, diffuse albedo에서 발생한다.

**금속 (Metals)**

F0 값이 크고, F0자체가 RGB값이다(0.5이상)

정면에서도 강한 반짝임, Fresnel 효과는 있지만 기본 반사가 이미 강한 상태이다.

내부 투과가 없고, 들어온 빛은 즉시 흡수된다.

모든 가시 색은 표면 반사에서 결정되며, 유색 반사율을 띈다.