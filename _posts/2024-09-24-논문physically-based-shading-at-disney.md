---
title: "[논문]Physically Based Shading at Disney"
date: 2024-09-24
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

**논문을 읽고, 아는 내용과 섞어서 나중에 기억을 상기하기 위해 정리한 글입니다.   
공부하면서 정리하다보니 오류가 있을 수 있습니다. 오류를 발견하면 댓글로 공유 부탁드려요!**

**(아래에 세타l, v, h, d 가 나올 것이다.**

**그것이 의미하는 바는   
세타l : l의 입사각, **세타v : v의 입사각,****

******세타h : half vector 와 normal vector의 사이각, **세타d: light vector 와 half vector의 사이가******)**

## **The microfacet model (미세면 모델)**

미세면(microfacet) 모델을 사용하여 BRDF(Bidirectional Reflectance Distribution Function)를 정의한다.

미세면(microfacet)은 표면 반사가 빛 벡터(l)와 뷰 벡터(v) 사이에서 일어날 수 있다면, 

반드시 표면의 한부분 또는 미세면(microfacet)에서 두 벡터의 중간 방향으로 정렬된 벡터를 가져야한다.

그것이 half vector이다.

아래의 그림을 보면 이해가 쉬울 것이다.

![](https://blog.kakaocdn.net/dna/bvXbz3/btsJH09dXRD/AAAAAAAAAAAAAAAAAAAAANn_wTJFUVHkCeSMIcImp4goXHQMn4DrEYkv2rixaAAa/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=P%2BsTl9sqUOXEwiYjNOs1pwPNgdo%3D)

식으로 나타내면 다음과 같다 h = (l + v) / |l + v|

등방성(isotropic) 재료에 대한 일반적인 미세면 모델은 아래의 식을 가진다.

![](https://blog.kakaocdn.net/dna/CHCU4/btsJIlrLK5k/AAAAAAAAAAAAAAAAAAAAALCSb9FI1Iyiq8Sp-RlsE2XhuUnnBN3iQQH2MqK7pxs0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=2JWYGfB7HIKy9clcjxnM4aBtEFE%3D)

( isotropic과 anisotropic 이 있다. BRDF라고 하면 보통 isotropic brdf를 의미하는 것 같다.

isotropic은 모든 방향으로 동일하게 빛을 반사시킨다는 의미이다. 더 효율적이여서 많이 쓴다고 한다. 하지만 결, brush느낌을 내기 위해서는 anisotropic brdf를 사용한다고 하는데, 이건 따로 조사해봐야 될 것 같다.)

diffuse모델로는 Lambert diffuse 모델이 자주 쓰이고, 상수 값으로 나타내어진다.

(Lambert diffuse 모델은 모든 방향으로 균일하게 반사된다는 가정이 있다. 때문에 빛의 입사각과 상관없이 동일하게 여겨지고, 그래서 상수로도 쓰인다.)

스페큘러(specular, 반사) 항의 경우:

* **D**는 미세면 분포 함수로, 스페큘러 피크의 모양을 결정합니다.
  + 미세면 부포 함수라는 말은 half vector가 얼마나 많이 분포되어있냐로 이해해도 괜찮을 것 같다.
* **F**는 프레넬 반사 계수(Fresnel reflection coefficient)입니다.
* **G**는 grometric(기하학적 감쇠) 또는 shadow factor(그림자 효과)를 나타냅니다.

물리적으로 타당한 대부분의 모델들은 microfacet(미세면) 형태로 구체적으로 설명되지 않더라도, 여전히 microfacet 모델로 해석될 수 있다. 왜냐하면 그런 모델들도 distribution function(D), Fresnel factor(F), 그리고 geometric shadowing factor(G)로 고려될 수 있는 요소들을 가지고 있기 때문이다.

microfacet 모델과 다른 모델 간의 유일한 차이는 microfacet 유도 과정에서 나오는

![](https://blog.kakaocdn.net/dna/cSiniv/btsJIkGnK09/AAAAAAAAAAAAAAAAAAAAAPgaetrRrDTF-3knabU3xmoYabIiBPTsm49aH0GUmj0u/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=0LdRW7ecM71EgPm6EuZp2x72sDM%3D)

을 포함하냐 안하냐 차이이다.

이 식을 포함하지 않는 모델의 경우

![](https://blog.kakaocdn.net/dna/6rnLk/btsJHzYAxpQ/AAAAAAAAAAAAAAAAAAAAABi2C1a2MopacpYE-5w-IzB_uWGkwSFc25dkdHYRCvLD/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=yFMnlOpKiIz%2B0jD932YUIJdUkP8%3D)

위 식을 D , F 함수를 먼저 분리하고 곱해주면 implied shadowing factor를 포함 시킬 수 있다.

이제 아래서 부터 Specular 요소들을 알아볼 것이다.

여기서 헷갈리면 안되는게

일단 기본이 Diffuse + Specular인데 Diffuse는 Lambert 함수로 끝났다.

이제 Specular만 보면 되는 것이다.

## **Specular D**

microfacet  distribution function(미세면 분포 함수) D(h)는 측정된 재료의 retroreflective을 통해 관찰될 수 있다.

(빛이 어디서 왔든지 그 빛이 들어온 방향으로 다시 돌아가는 특성을 retroreflection이라고 한다.)

![](https://blog.kakaocdn.net/dna/yT2ve/btsJGKmfa1n/AAAAAAAAAAAAAAAAAAAAAB5XPc1Wvg6cqz_nJr5hiBK7Z-jL-AdNmgDOyKOevEh9/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ydzuUp8zjxTzf6HipkJpy%2BhKVSk%3D)

반짝이는 부분을 의미한는 것 같다.

peak의 높이에 따라 두 그룹으로 나눈다. 여기서 peak는 표면의 거칠기를 의미한다. (거칠기가 높으면, peak도 높다.)'

peak가 제일 높았던 쇠 재질은 peak가 400이 넘는다.  peak가 평탄할 수록 diffuse reflectance가 나타난다.

* **거칠기가 낮을수록 (매끄러운 표면일수록) 피크가 더 높다.**
* **거칠기가 높을수록 피크가 낮아지고 넓게 퍼진다.**

![](https://blog.kakaocdn.net/dna/bZVc8Q/btsJGhx65FD/AAAAAAAAAAAAAAAAAAAAAA4iR0dB1P0Duqv6NIeHXparEXGnPa2V_p1DE1ccJAjl/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=eAjHtdkLd3sHeFw%2BzgJbUFZX%2FRE%3D)

x축은 세타H

![](https://blog.kakaocdn.net/dna/bbngjH/btsJHzEgsnt/AAAAAAAAAAAAAAAAAAAAAK4p3RhBPNCzM1ShHqbCVuAKExynNwijc3pJDgG3Y5vl/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=lYMU5vNFciHslxwBYRkRB0aCqzA%3D)

y축은 specular peak이다.

검정이 왼쪽 빛, 빨강이 가운데, 파랑이 오른쪽 빛 같다.

specular tail이 가장 긴 것이 왼쪽이기 떄문에

제일 왼쪽 모델이 merl에서 만든 쇠 재질인데, specular tail을 가장 잘 표현했다고 말하고있다.

2번는 GGX, 3번 째는 Beckman 모델이다.

## **Specular F**

![](https://blog.kakaocdn.net/dna/l7kDs/btsJHpBHq8A/AAAAAAAAAAAAAAAAAAAAAERfD4SLnZsujjywt4e3ZR6avc1QvcIPNe8v_d0UtuR9/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=TPoVWar4wg3Zc5%2Fomr66GPqyEUo%3D)

Y축은 Specular 계수라고 봐도 될 것 같다. ( PBR을 구현할 때 specular와 diffuse 비율을 fresnel모델로 구했던 기억이난다..)

논문에서도 Fresnel reflection factor(프레넬 반사 계수) 라고 말한다.

프레넬 반사 계수 F는 light vector와 view vector와의 각도가 커질 수록 증가합니다. 이론적으로 모든 매끄러운 표면은 grazing incidence(매우 얕은 입사각)에서 100% 반사를 보입니다. (단, maxinum 90도 입니다.)

거친 표면의 경우 100% 반사는 달성되지 않지만, 반사율은 증가합니다.

많은 곡선들이 grazing angle에 가까워질수록 프레넬 효과로 예측된 것보다 더 가파른 증가를 보인다는 것입니다.

이 관찰은 Torrance-Sparrow(1967) 미세면 모델의 동기가 되었습니다.

![](https://blog.kakaocdn.net/dna/bzVliQ/btsJGOPsix4/AAAAAAAAAAAAAAAAAAAAAKaY8fDpXnEow6vsk_sEBqaNExDwUY8hoXycDqjomrlU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=oxNEk3EPnsQS8aeCabxVEj%2BkI1E%3D)

이 식 때문에 미세면 모델에서 무한대로 발산할 수 있습니다. ( cos이 0일 때, 90도)

그러나 현실에서나 렌더링 모델에서나 문제가 되지 않는 이유는 shadowing effects of the microsurface(미세면의 그림자 효과)때문입니다.

G 요소는 빛 벡터의 그림자와 시선 벡터의 마스킹을 나타내며, grazing 반사율을 제어합니다.

G 요소가 그림자를 나타내지만, G와 위식 (   1/(4cosθlcosθv)   )의 조합은 결과적으로 프레넬 효과를 effectively amplies (증폭)시킵니다.

( effectively amplies(증폭) : 90도에 가까워 질 때 급격히 증가하는 부분, 단 무한대로가는 것은 막아줌)

## 

## **Specular G**

![](https://blog.kakaocdn.net/dna/bfKNL2/btsJI3lhC4h/AAAAAAAAAAAAAAAAAAAAAHi-k-4wxKKiYrHUKzov-IVvRbK1M0YUGN2SiXuIkLZ6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=uM3oDqfcXfxnBNbUoroe8aM0Jp4%3D)

좌측 그래프가 Smooth한 재질, 우측이 Rough한 재질이다.

G를 분리해서 보는 것은 어렵지만, abledo를 통해서 간접적으로 확인할 수 있다.

albedo는 총 입사 에너지 중 반사된 비율이다. 넓은 의미로는 표면의 색이고 모든 파장에 대해서 1보다 작아야한다. (반사 비율이니까)

표와 같이 albedo는 70도 까지는 일정하다.

smooth한 재질은 올라가다가 꺽이고, rough한 재질은 쭉 올라간다.

![](https://blog.kakaocdn.net/dna/bmPPKS/btsJKi9mtDc/AAAAAAAAAAAAAAAAAAAAAP3hqCEdVl8w4vSjYnS7C_R36cZ1dGGHhDS6LCVQmdvK/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=YhWH%2B348h71%2FTHcIPKwR3yb8Bl0%3D)

**Specular G를 제거한 표이다.**

**G가 없을 때 각도가 커질 수록 과하게 반응한다.**

![](https://blog.kakaocdn.net/dna/rPARj/btsJIQl9tPH/AAAAAAAAAAAAAAAAAAAAAOW5wuZvYIO8caCkup12vBaYynxnU5OkyxxKA-2AMJPV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=x17RelqRHn%2FtItJKZkFSc0KN4Og%3D)

지금까지 알려진 BRDF를 썼을 때

1번 비대칭적인 speculat

2번 갑자기 값이 뛰어버림

3번 천을 렌더링할 때 그림자가 갑자기 생김

4번 나무 결이 안나타남

이러한 문제점들이 있다.

## **Disney principled BRDF**

**원칙**

1. 실제 물리적인 인자보다 직관이 중요하다.

2. 인자는 적을 수록 좋다.

3. 인자는 가능한 0~1범위가 좋다.

4. 하지만 의미가 있다면 범위를 넘어도 괜찮다.

5. 모든 인자들의 조합이 가능한 견고하고 그럴듯해야 한다.

**인자**

1. baseColor

2. subsurface

3. metalic

4. specular

5. specularTint : artist들을 위한 색 controller

6. roughness

7. anisotropic

8. sheen: an additional grazing component, primarily intended for cloth (grazing component: 평행하게 입사할 때, 그 각도에서 발생하는 반사현상 )

9. sheenTint

10. clearcoat

11. clearcoatGloss

![](https://blog.kakaocdn.net/dna/cJaybf/btsJKk7bLQz/AAAAAAAAAAAAAAAAAAAAAFtwTroQzMJuF9NVzHk1Eja1DRwryzyD_CVFeQzFLRqH/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wZvYWwh4NfiBV7Hy0I6ztqyUo3I%3D)

## 

## **Diffuse model details**

몇몇 모델은 아래 식과 같은 diffuse Fresnel factor를 사용한다.

![](https://blog.kakaocdn.net/dna/di6wcE/btsJHVBJ7aK/AAAAAAAAAAAAAAAAAAAAAIT6MOWV4hvJfUmWS7XNHnLIOUIfjZqRee2V-NtUSyBa/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fFGCXXdXnk38IIdIR%2BXXvH7TMw8%3D)

F(세타)는 Fresnel 반사 인자이다.

Lamert모델로 Diffuse를 구현하면 가장자리가 어둡게 만들어진다. 밝게하기 위해서 Fresnel factor를 추가해도 이미 어두운 빛을 반사하기 때문에 더 어둡게 표현된다.

경험을 바탕으로 smooth한 표면은 Fresnel 그림자를, rough한 표면은 하이라이트를 넣어서 새로운 모델을 개발했습니다.

아티스트들이 좋아하고, 더 그럴 듯하게 보이고 , 물리기반이다.

또한

diffuse Fresnel factor에서 나타나는 굴절 요소는 무시하고 입사된 diffuse에는 손실이 없다고 가정한다.

이를 통해서 우리가 입사되는 diffuse색을 직접 정할 수 있다.

우리는 Schlick Fresnel approximation을 사용하고, grazing retroreflection에서 특정 roughness에서 0이 되지 않도록 반응을 수정한다.

우리의 diffuse식은 아래와 같다.

![](https://blog.kakaocdn.net/dna/mpUGm/btsJHTKHkwO/AAAAAAAAAAAAAAAAAAAAAN3zo5pGyntE9CxHdSjmsOEoiB66Eh5GU-iITlJWE6kV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=OGswnAbCy1wEzqTVui78ZQ1L%2FIU%3D)
![](https://blog.kakaocdn.net/dna/dgcWE1/btsJLHBfSjm/AAAAAAAAAAAAAAAAAAAAAD1_a1lt8LT-_1jPVRz3x4zaG7sKxdGi0LDCntdCpVrn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Mjry2WSlqhbroSuWlBRsSHk2Lqs%3D)

Schlick Fresnel approximation 식

이 모델은 smooth한 재질에서의 grazing angle에서 diffuse 반사를 줄여주고, (너무 밝았던 것을 감소시켜준다는 말)

rough한 표면에서는 반사를 증가시켜준다. (어두웠던 부분은 밝게 해주었다.)

이것은 시각적으로 더 만족스러운 결과를 만든다.

![](https://blog.kakaocdn.net/dna/yVUml/btsJKdojjZK/AAAAAAAAAAAAAAAAAAAAAGI1lPH1OJhMit6rkufZX8sz0YS1Tph9JI2MHKpbJFZ0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=MC4SK7bUtf7QF32sh0RmkIyAmq4%3D)

## **Specular D details**

가장 유명한 모델로, specular tail이 가장 긴 GGX가 있다. 하지만 특정한 많은 재질에서 충분히 길어지지 않는 문제가 있다.(specular tail이)

그리고 GTR이라는 모델이 있다.(Trowbridge-Reitz라고도 불림) 이 모델은 지수가 1인데도 긴 specular tail을 가지고 있다.

![](https://blog.kakaocdn.net/dna/Fk67U/btsJKGQ74fm/AAAAAAAAAAAAAAAAAAAAAEAzFoscOP7LQbnhbLoHfkYoS1ep2cWcHnG3WeRSYqIy/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xesG4i6lDiJ7tMTinxluVLAMnig%3D)

(c는 상수, a는 거칠기 (0~1))

![](https://blog.kakaocdn.net/dna/b6nUkN/btsJLx6Ejut/AAAAAAAAAAAAAAAAAAAAAKJ8brvITQZUJtqb2KhWomFPVF35Tyjylx9GThnUuF2R/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=IIglCWLudQBvyl%2F93FpsFFg5XoU%3D)

r이 2인데도 GGX와 같은 specular tail을 갖는 것을 볼 수 있다.

우리는 메인으로는 r=2인 GTR모델을 사용하고있고, 두번째 모델로는(secondary)는 r=1를 사용하고 있다.

메인은 anisotropix과  metalic을 나타낸다.

두번째 모델은 isotropic과 non-metalic을 나타낸다.

또한 거친 모델을 나타낼 때는 a = roughness ^ 2을 해주면 거칠기를 선형적으로 잘 변화시켜준다.

(오히려 제곱을 해주지 않으면 않으면 smooth 와 rough 사이에서는 항상 rough쪽으로 나타났고, 반짝거리는 재질을 만드는데는 매우 작고 직관적이지 않은 값들 필요했다.)

## **Specular F** **details**

![](https://blog.kakaocdn.net/dna/SGWdd/btsJK441Rnr/AAAAAAAAAAAAAAAAAAAAAPhZS6sJHWZtETWUIoUxgihPgvem8bq_x9dTtRu88Xoa/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FmK5Vj0yobDuntedjnQQfoKR850%3D)
![](https://blog.kakaocdn.net/dna/ymSeX/btsJJVIaD37/AAAAAAAAAAAAAAAAAAAAAE4nfj-U78syg5PtQkI1kBulk8B6zQEJUuCpiy_lp4Bv/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Em0Tmi2xpu6wgc7df0wmjiFuWkw%3D)

첫번째 : Schilck Fresnel approximation / 두번째 :  Full Fresnel 

우리는 Schilck Fresnel approximation을 이용해서 는 full Fresnel 식이랑 비교했을 때 많이 간단하지만 충분한 값을 얻는 것이 목표다.

( Schilck Fresnel approximation이 full Fresnel식을 간단하게 한 식이다.)

F0을 이렇게 설정하면 이런 색을 볼 수 있다.

![](https://blog.kakaocdn.net/dna/cTNXc1/btsJKHvENQf/AAAAAAAAAAAAAAAAAAAAAJZhQwWKcLrItYC_PNbiDVC71GqlIrBfPUO5nt5QNNhX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ioIhROD7yGnkkYa9DH8PBpBR%2FLw%3D)

`2`

## 

## **Specular G**

우리 모델에서는 하이브리드로 사용한다.

우리는 G를 GGX(Walter의)를 사용한다. 그리고 너무 밝은 표면에서는 거칠기를 추가하기 위해 Smith Shadowing factor 를 사용한다. (그래서 하이브리드라고 했나보다.)

![](https://blog.kakaocdn.net/dna/nMeq4/btsJJP2vFMo/AAAAAAAAAAAAAAAAAAAAAFTeAteqLxX9k7Ac1EDHV6pZOx7hibpMuMJHN8Xv0WtH/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3qa6ukrtYmiODNfpGZn8E94LVsc%3D)

0.5는 거칠기를 조정하기 위해 더해준다.

clearcoat는 GGX만 사용한다. ( smith shadowing factor를 더해주지 X)

(clearcoatsms표면에 추가되는 투명한 코팅층으로, 주로 자동차 페인팅이나 고급 재료에 사용된다.)