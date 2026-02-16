---
title: "[RealTimeRendering] BRDF"
date: 2025-08-28
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### 

### **BRDF**

궁극적으로, 물리 기반 렌더링은 어떤 view ray 집합을 따라 **카메라에 들어오는 radiance(휘도)를 계산**하는 것이다.

주어진 뷰 레이에 대해 우리가 계산해야 하는 값은 **Li(c, v)** 이다.

**c** 는 카메라 위치, **v** 는 뷰 레이 방향 (카메라를 향하는 방향) 이다.

렌더링에서 장면은 일반적으로 매질로 채워진 객체들의 집합으로 모델링된다

.

이 장에서는 참여 매질이 없다고 가정하고, 카메라에 들어오는 radiance(휘도)는 카메라 방향으로 가장 가까운 물체 표면에서 방출되는 것으로 가정한다.

![](https://blog.kakaocdn.net/dna/quLQX/btsP8GXwN43/AAAAAAAAAAAAAAAAAAAAAA4gLvnmKLuavlyan9wZNCEWEVe-8vDyoCJJu7Ea3tA6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=gw%2B79n9AX51UMmAMOIIgCYHhy%2BE%3D)

카메마로 들어오는 빛(radiance) = 물체에서 반사되는 빛(radiance)

여기서 p 는 뷰 레이가 가장 가까운 객체 표면과 교차하는 점이다.

우리의 새로운 목표는 Lo(p, v) 를 계산하는 것이다.

이 장에서는 transparency(투명성)과 global subsurface scattering은 배제하고, **로컬 반사 현상**에 집중한다.

Lo의 의미는 현재 음영 처리 중인 점에 도달한 빛이 다시 바깥으로 반사되는 현상이다.

여기에는 표면 반사뿐만 아니라 local subsurface scattering도 포함되며, 입사광 방향 **l**과 **v**에만 의존한다.

이러한 로컬 반사는 **BRDF(bidirectional reflectance distribution function)**로 정량화할 수 있으며, 이를 **f(l, v)** 로 표기한다.

incoming 방향과 outgoing 방향은 각각 2 degree of freedom을 가진다.

자주 쓰이는 매개화 방식은 두 개의 각도를 이용하는 것이다. 표면 법선 n 에 대한 고도(θ)와, n을 기준으로 한 방위각(φ)이다.

일반적으로 BRDF는 네 개의 스칼라 변수의 함수이다. ( l, v, θ, φ 이렇게 총 4개)

![](https://blog.kakaocdn.net/dna/cHpxoW/btsP76oF1EW/AAAAAAAAAAAAAAAAAAAAAIr9tZtAFzmOweb0khDTUlHtEq-Ahc1zjjIBaFywrmO8/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=NX%2FpAqcU4%2B5A4HZ1pw2ycFIWx3c%3D)

특수 경우로 **Isotropic BRDF(등방성 BRDF)**가 있다.

더보기

이런 BRDF는 incoming과 outgoing 방향을 표면 법선을 중심으로 회전시켜도, 두 방향 사이의 상대 각도만 같다면 BRDF의 값이 변하지 않는다. (=> 모든 방향으로 동일하게 반사시킨다는 의미)

isotropic BRDF(등방성 BRDF)는 세 개의 스칼라 변수의 함수이며,

빛과 카메라 사이의 단일 각도 φ(방위각) 만 필요하다. 이는 균일한 등방성 재질을 턴테이블에 올려 회전시켜도, 고정된 조명과 카메라 하에서는 어느 각도에서나 똑같이 보인다는 뜻이다.

(=> 등방성이면 φ(방위각)도 필요없는거 아님? diffuse 계산할 때는 필요가 없다고 볼 수있지만, specular를 계산하기 위해서 상대 φ(방위각)을 알아야하기 때문에 인자로 넘겨줘야한다.

위의 예시는 θi, θo를 고정으로하는 예시여서 θ는 인자로 안받고 있는것이다.)

주어진 파장의 입사광은 같은 파장에서 반사될 때 두 가지 방식으로 모델링할 수 있다. (형광이나 인광과 같은 현상은 무시)

1. 파장을 BRDF의 추가 입력 변수로 다루거나

**2.BRDF가 스펙트럼 분포 값을 반환하도록 하는 것 (=>BRDF함수가 rgb 값을 반환하는 것)**

실시간 렌더링에서는 항상 두 번째 방식이 쓰인다.

실시간 렌더러는 스펙트럼 분포를 RGB 삼원값으로 표현하기 때문에, 이는 단순히 BRDF가 **RGB 값**을 반환한다는 뜻이다.

### 

### **BRDF수식**

Lo​(p,v)를 계산하기 위해, 우리는 BRDF( f(l,v) )를 반사 방정식(reflectance equation)에 포함시킨다.

![](https://blog.kakaocdn.net/dna/CgD48/btsP8DNrAWy/AAAAAAAAAAAAAAAAAAAAACowpJycvDH_cfVHoUM5mxcUTppLe5RR5a-0UITT8R6c/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FsTpNGRVNL%2BN4O5XEETch0Z0gLY%3D)

위 식을 간단히 설명하면,  Li 를 통해 incoming되는 빛의 세기 BRDF식을 곱해서 outgoing을 연산해준다, (dot(n, l)로 각도에 따른 세기를 조절한다.)

적분 기호의 첨자 l∈Ω는, 적분이 표면의 법선 n을 중심으로 한 단위 반구 위에 놓인 입사 방향 벡터 l에 대해 수행된다는 것을 의미한다.

여기서는 적분을 하고 있기 때문에 반구 위 대한 전체 입사 방향을 계산하다.

다시 한 번 정리하면, **outgoing radiance(반사 방정식)는 incoming radiance(입사 휘도)에 BRDF를 곱하고 dot(n,l) 을 곱한 값을 반구 위에서 적분한 것과 같다**는 사실을 보여준다.

(BRDF는 incoming방향 빛이 outgoing 방향으로 얼마나 반사되는 지에 대한 분포임을 기억하자)

편의상, 이어지는 식에서는 p(표면 위치)를 생략해서표기하겠다.

![](https://blog.kakaocdn.net/dna/Dgac3/btsP9ac7qUD/AAAAAAAAAAAAAAAAAAAAAEjM7Xui53hwGcXTdfJ-OvLzhxi4Sie7THdBx5wNrvm7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=o8QFbEUaB4je07fsjBgz%2FzAiZM0%3D)

반구를 적분할 때는, spherical coordinates(구면 좌표계) ϕ, θ를 사용한다.

이때 미소 입체각 dl은 다음과 같이 된다.

![](https://blog.kakaocdn.net/dna/pUJm3/btsP6WgcFuo/AAAAAAAAAAAAAAAAAAAAAG55-YYLzbiEdjk0pmbszbLxBVKwzfR2hxy41womFtVi/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=0tLes42eemZQJVfOP%2BBHiZAdlG8%3D)

정확한 원리는 아니지만, 직관적으로 이해해 보자면 아래와 같다.

dϕ: 원 둘레 방향(수평)으로 얼마나 회전했는지.

dθ: 위아래(극 방향)으로 얼마나 움직였는지.

sin⁡θ: polar angle이 커질 수록, 반구의 둘레가 커짐 그 값을 보정해주는 역할

이 파라미터화를 사용하면, dot(n, l) = cosθ\_i 라는 사실을 이용해서

아래와 같은 이중 적분(double integral) 형태를 얻을 수 있다.

(위에서 구한 dl 을 치환해준다. 그에 때라 θ, ϕ의 적분으로 바꿔줘야하니 double integral이 되는데, θ는 반구니까 pi/2이고, ϕ는 구의 둘레니까 2pi로 적분해준다.)

더보기

로컬 프레임에서 n=(0,0,1), l(θ,ϕ)=(sin⁡θcos⁡ϕ, sin⁡θsin⁡ϕ, cos⁡θ)

그래서 n⋅l=cos⁡θl가 된다.

![](https://blog.kakaocdn.net/dna/bkcrvm/btsP9aEdwXH/AAAAAAAAAAAAAAAAAAAAAGORf6I7gi5ufloP2AySG_-cUWpiZEzBTK4bIp0P-h1O/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1756652399&allow_ip=&allow_referer=&signature=Gt2dV8L9a3BJ1VtyIi0yqhZ51dM%3D)

θi, ϕi, θo, ϕo 에 대한 그림

더보기

![](https://blog.kakaocdn.net/dna/qjPJr/btsP9Igwhix/AAAAAAAAAAAAAAAAAAAAAJYyJpp8Ep0KaBQxCLqLcpOxZVxxLekYCSZNJXstX9lt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ck1aBj6YrRoUl1wXg6DghCfkN2c%3D)

때로는 θi,θo 대신 elevation angle(고도각)의 코사인 값을 변수로 사용하는 것이 편리하다.  
μi=cos⁡θi,  μo=cos⁡θo 

![](https://blog.kakaocdn.net/dna/bukSJo/btsP8dIrq7o/AAAAAAAAAAAAAAAAAAAAAEDSPc7oJczWLo4p7baR_o11eJq6HeBxfbJxCIfMNWbE/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3rfuwkQZ6LS0bdNpsm9kq%2FEBPCo%3D)
![](https://blog.kakaocdn.net/dna/AaTpm/btsP6GkxlHa/AAAAAAAAAAAAAAAAAAAAAKQP9r2KqUGvJNs0gYkl-PcuULjMF0ot-liMjWs2h_MR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=60sBC%2Bix42GocIirvCvZwwQAknc%3D)

이 파라미터화를 사용하면 dl은 아래 처럼되고

![](https://blog.kakaocdn.net/dna/YThzf/btsP9G36Glt/AAAAAAAAAAAAAAAAAAAAANOdWMrOj_7ysMUNSIdLNiBb70AvwDxqAp0-WA9S1Drv/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=OHmSXt1aabyzy8oNpYgTus2sB%2FU%3D)

최종식은 아래와 같이 표기할 수 있다.

![](https://blog.kakaocdn.net/dna/Z9Rq7/btsP688tGgt/AAAAAAAAAAAAAAAAAAAAAKtEOaGenGdbt1KkkT5tKseuQcq_jVXF4arSiIlRauIn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=4NCxs1QoEI1DB%2BTOABfFS7CmbM4%3D)

BRDF는 **입사 방향과 시선 방향이 모두 표면 위에 있을 때만 정의된다**.

즉, 광선이 표면 아래로 들어가는 경우는, BRDF에 0을 곱하거나 애초에 계산하지 않도록 하여 피할 수 있다.

하지만 시선 방향이 표면 아래에 있는 경우( dot(n,v) < 0,z  코사인 때문에 음수가 나온다. )는 어떻게 해야 할까?

음수면 빛을 어떻게 뺐어가기라도 할거야?

그래서 dot product를 할 때 max( dot(n,v), 0.0f) 를 해서 clamping해주는 것을 잊지말자

( Frostbite 엔진은dot(n, v)의 절댓값에 아주 작은 값(0.000001)을 더해 divide by zero를 피하도록 구현했다.

또 다른 방법은 soft clamp로, n과 v의 각도가 90°를 넘어가면 점차적으로 0으로 수렴하게 만드는 방법도 존재한다.)

물리 법칙은 어떤 BRDF에도 두 가지 제약을 부과한다.

**1. Helmholtz reciprocity(헬름홀츠 상호성)로, 입력과 출력 각도를 서로 바꾸어도 함수값이 동일해야 한다는 의미이다.**

![](https://blog.kakaocdn.net/dna/k5CtK/btsP98lLfTI/AAAAAAAAAAAAAAAAAAAAAK123New5Xq8MYK14cwVZjB5Y9jNCUjF1xz28U93l6G1/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=IKdzd3Tm6WXnDjXdBzW08AmI%2Bhk%3D)

상호성을 엄밀히 요구하는 bidirectional path tracing을 제외하면,

실무에서 사용하는 BRDF들은 대부분 Helmholtz reciprocity를 위반하더라도 눈에 띄는 아티팩트 없이 잘 동작한다.

( 그럼에도 reciprocity(상호성)은 BRDF가 물리적으로 그럴듯한지 판단할 때 유용한 도구다.)

**2. conservation of energy(에너지 보존)이다.**

**incoming 에너지**가 **outgoing 에너지**보다 커질 수 없다. (발광물체 제외)

실시간 렌더링에서는 정확한(엄밀한) 에너지 보존까지는 필요 없지만, 근사적인 에너지 보존이 중요하다.

에너지 보존을 크게 위반하는 BRDF는 렌더링된 표면이 과도하게 밝아져 비현실적으로 보일 수 있다.

**directional-hemispherical reflectance은** R(l)은 BRDF와 관련된 함수로,

BRDF가 에너지 보존을 얼마나 만족하는지 측정하는 데 쓰인다.

주어진 하나의 **incoming 방향**으로부터 들어온 빛이 표면 법선 주변의 반구 내 **모든 outgoing 방향**으로 얼마나 반사되는지를 측정한다.

![](https://blog.kakaocdn.net/dna/t5kIx/btsP5FlMMDO/AAAAAAAAAAAAAAAAAAAAAEsbVbBy1KGuQLVnnVc2-ZiVJYvCbcNZ6dfNSSOeSKn0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hQfBsf00iaZV%2FMmsik1JQ%2BE491o%3D)![](https://blog.kakaocdn.net/dna/cLH5Ka/btsP80ocPBq/AAAAAAAAAAAAAAAAAAAAACiYwu7mgKA8VZ5I1le8bZ7ohA3Ou-5sL9e0EcZhhNdZ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2Faq2cxQXylkPonQnsPRhh%2Baoiiw%3D)

왼쪽: directional-hemispherical reflectacne/ 오른쪽: hemisphereical-directional reflectance => 동일한 의미니 원하는 식 사용

에너지 보존의 결과로,

R(l)의 값은 항상 [0,1]범위에 있어야 한다.

값이 0이면 모든 입사광이 흡수되거나 소실되는 경우이고, 1이면 모든 빛이 반사되는 경우다.

주의할 점은, BRDF는 분포함수이기 때문에 위치에 따라서 값이 크고, 작을 수 있다.

**에너지 보존을 만족하기 위해서는  모든 l에 대해서 R(l)이 1을 넘지 않아야 한다.**

### 

### **Lambertian BRDF**

가장 단순한 BRDF는 Lambertian(램버시안)이며, 상수 값을 갖는다.

**Lambertian BRDF의 이 상수 반사율을 cdiff(diffuse color) 또는 ρ (albedo, 알베도)**라고 부르는데,

Lambertian은 단순함에도 불구하고, 실시간 렌더링에서 local subsurface scattering을 표현하는 데 자주 사용된다. (이후 내용에서 다루는 더 정확한 모델들이 점차 대체하고 있다.)

이 장에서는 subsurface scattering과 연계를 강조하기 위해 이를 ρss(subsurface albedo)라 부르겠다.

(ρsss는 이후 장에서 자세히 다루겠다.)

람베르시안 표면의 bidirectional-hemisphereical reflectance(R)도 상수다.

![](https://blog.kakaocdn.net/dna/20pv6/btsP7fGManP/AAAAAAAAAAAAAAAAAAAAAGK3yu-0i3ku9f0bp9_GZv6QBVnTKVkNbbdDIBeWN4yG/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=7nE%2FbQFQ7Kmsbv4xIr9BwVI09fM%3D)![](https://blog.kakaocdn.net/dna/QNMiN/btsP6fNTJBx/AAAAAAAAAAAAAAAAAAAAAFRuB0lOw7bZO1QQOAV5IDYI274Itk0pBHbDwvtfv-Vu/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=NQcsJaRJmM5mMJiIfNtXbd1nKL8%3D)

R(l)은 주어진 입사 방향에서 전체로 얼마나 반사되는가(=알베도)인데,

물리적으로 이 값이 ρ여야 한다.

![](https://blog.kakaocdn.net/dna/HJGKX/btsP6U3P0jX/AAAAAAAAAAAAAAAAAAAAADlbSygsr6jDql6wie_hld8uld4Wgk_XNfT0uZt11bQk/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=erq7xm5y1x9Fba41%2BqbpMWtNop4%3D)

그렇기 떄문에 f(l, v)가 pss / pi 값을 갖는다.

BRDF를 이해하는 한 가지 방법은, 입사 방향을 고정한 채 시각화하는 것이다.

아래의 그림은 잘 안보이지만 우측에서 좌측으로 들어오는 초록색 ray가 입사광선이다.

![](https://blog.kakaocdn.net/dna/cYPSXF/btsP7aZGmpC/AAAAAAAAAAAAAAAAAAAAAF5Oe0HfBCVZEbUWoP0t4LGjYk7dZkyrEjGV6pLZ5Doq/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=k0yVElTN0hDiiUySQzCp8iz%2BvU0%3D)

상단: labert, blinn phong, cook-torrance 순서 / 하단: Ward, HapkeLommel-Seeliger, Lommel-Seeliger 순

**주어진 입사 방향에 대해, 모든 outgoing 방향에 대한 BRDF 값을 표시한다.**