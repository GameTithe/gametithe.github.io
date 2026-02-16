---
title: "[논문 정리] The Real-time Volumetric Cloudscapes of Horizon: Zero Dawn(2) - 구름(Lighting)"
date: 2025-07-18
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

구름을 렌더링하기 위해서 첫 번째로 한 일은 modeling이 였습니다.

<https://tithingbygame.tistory.com/226>

[[논문 정리] The Real-time Volumetric Cloudscapes of Horizon: Zero Dawn(1) - 구름(모델링)

siggraph 발표 글을 정리했으니,, 논문정리 카테고리를 선택했습니다..ㅎㅎ구름 렌더링 글을 적으면서 참고한 글 주로 이 글을 봤습니다. https://www.guerrilla-games.com/read/the-real-time-volumetric-cloudscapes-of-

tithingbygame.tistory.com](https://tithingbygame.tistory.com/226)

lighting없이 modeling만 렌더링한 결과입니다. 이제 lighting을 적용해봅시다.  (지금까지 적용하던 빛도 태양과 상호작용이 없는 가짜 빛이였습니다..ㅎㅎ)

![](https://blog.kakaocdn.net/dna/yDAAM/btsPn1aEKon/AAAAAAAAAAAAAAAAAAAAAGjhLVwz-5pxBpJw9czcP6VD1Bn9zANqoxAcVEQvWCyU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3QUhUQrSpAOl2W8p72A%2BJDEtq2M%3D)

구름에 대한 빛 처리를 하기 위해서는 3가지 문제를 해결해야 합니다.

![](https://blog.kakaocdn.net/dna/bKq4Th/btsPnvXeFkd/AAAAAAAAAAAAAAAAAAAAAPVIvU3uTEDVWAygwlXEUk6EoKFCysM_6MDE641kd6Y1/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=CZ%2FK9HmCh2UVu1hxUWjwnUPcMvQ%3D)

1. 방향성이 있는 scattering(산란) or 구름이 빛나는 정도

2. 구름 뒤 태양을 바라볼 때 생기는 sliver lining

3. 태양을 등지고 구름을 바라볼 때 어둡게 보이는 것 구현

1,2번에 대한 솔루션은 이미 존재하지만 3번은 우리가 만들어야 했습니다.

![](https://blog.kakaocdn.net/dna/bfuBDz/btsPl9gPaX5/AAAAAAAAAAAAAAAAAAAAAL60FqRiK_oka8_9TaNLXZ5m9LuicNe-ZV0EMyG5wAwk/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wu50fMymt1vI3ertg%2BhIcqXgSEU%3D)

빛이 구름에 들어가게되면, 내부의 물방울과 얼음조각에 부딪히며 굴절의 시간을 가지게 됩니다.

결과적으로 영겁의 시간을 거쳐 구름 밖으로 나올 때쯤에는

산란되어서 흩어지거나, 구름에 완전히 흡수가 되거나, 다른 ray와 결합되어서 in-scattering 됩니다.

실시간이 아닌 영화 산업이면 몰라도, 게임은 다른 방법을 찾아야합니다. 

![](https://blog.kakaocdn.net/dna/ekQ4sU/btsPmc5NHAQ/AAAAAAAAAAAAAAAAAAAAAMgFsYb4KiahYqCUfuBuwfNR6Tn24IceD_8Jox6x-idk/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wkdrOnxnxOP8tAuxZUyv%2BRRbLdU%3D)

빛의 통과하는 매질의 optical thickness(광학적 두께)에 따라서 특정 지점에 도달하는 빛의 양이 달라지겠지만,

깊이에 따라 지수적으로 감사한다는 것을 확인할 수 있습니다.

그런데말입니다...

특정 지점에서 빛 에너지에 기여하는 또 다른 요소가 있습니다.

구름 내에서 빛이 산란될 때 순순히 산란되는 것이 아닌 앞, 뒤로 마구잡이로 산란이 됩니다. (랜덤이란 말은 아니구요 그냥 앞뒤로 산란한다구여) 

이런 성질 때문에 silver lining이 생기는 것입니다.

**(fog rendering할 때는 beer lambert law로 만족하더니만,**

**왜 멀리있는 구름 렌더링할 때는 beer lambert law로 만족하지 못하고 henyey greinstein model까지 추가하나 했는데, sliver lining 때문이였네!!)**

![](https://blog.kakaocdn.net/dna/bTCxwQ/btsPn1BsVe2/AAAAAAAAAAAAAAAAAAAAAAmdhvH_leMewTeyZVdkGxlEDE0In-ck-2-DGJQPJ7Dn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3Xu%2BCuC9m656U0BhZ2uckfYsFXE%3D)

물론 아까도 말했다시피, 영화였으면 산란되는 방향을 계산을 했겠죠 하지만 우리는 게임에 사용해야되기 때문에 편법을 써야만합니다.

더보기

계산하려면 해보시게나

![](https://blog.kakaocdn.net/dna/8pVHf/btsPiJCua00/AAAAAAAAAAAAAAAAAAAAAMPkLObYgs_pFsMzaHqlXqBAoqpHgNNx2LzlhcYihR6c/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=4aCTdmTM5ChNh1kmU73ZeDp4vwY%3D)

편법으로 채택된 방법(식)은 Henyey-Greenstein 모델입니다. (기존에도 구름 조명을 위해 비등방성 효과를 재현하는데 많이 사용되는 식입니다.)

좌측은 beer lambert만 적용됐고, 우측은 beer lambert + henyey-greenstein 입니다.

![](https://blog.kakaocdn.net/dna/brozYn/btsPmby1WQ6/AAAAAAAAAAAAAAAAAAAAAAuXQAN2jQGpgM0TjApUhBeXot8PsJGC4vIWX2M5BJOu/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ByROxokJnkElGSV5Mpji%2FbbsLrE%3D)

참 예쁜데,,, 근데 어두운 부분에 대한 정보가 없었고

우리는 이에 대한 사고실험을 했습니다.

![](https://blog.kakaocdn.net/dna/bRBwB8/btsPmzfjtPU/AAAAAAAAAAAAAAAAAAAAALGvglVLlcJx3RDxwllM223I2oR7W_CvTx6oTWROnQMN/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=EZl2TNZfE1du%2FLn65P1iaaqBrIc%3D)

빛의 경로에 대해서 생각을 해봤습니다.

구름 표면에 가까운 한 지점 보다는 구름 내부의 한 지점이 산란된 빛을 많이 받을 것입니다.

즉 구름은 빛을 모으는 한 집합체라고 가정할 수도 있을 것입니다.

이런 현상은 둥근 형태일 때 명백하게 나타나며, 둥글거나, 모서리 부분보다 오목하게 들어간 부분이 더 밝게 보입니다.

이런 효과를 하나하나 계산하는 방법은 영화업계에는 존재하지만, 우리는 real time rendering을 해야하기 때문에 근사 방법을 찾아야합니다.

이런 효과를 설탕가루에서 발견했습니다.

![](https://blog.kakaocdn.net/dna/cdXW8I/btsPnKUx8k8/AAAAAAAAAAAAAAAAAAAAAEFJBQtF0TY6ymrvOGgXfU7BHhGdevxH51aO5AP3g2Ny/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=8Q%2B%2F0j7ZJKTZ%2FgZXoMJ9KQgVi0w%3D)

이 효과를 이해하면 어디서나 보이기 시작합니다.

![](https://blog.kakaocdn.net/dna/bNV4RF/btsPngsMMeD/AAAAAAAAAAAAAAAAAAAAAMI_77DZzDEYBKM0vwxlv9ip_VKc1iIdEvQIqDyrgc1i/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2BcL7CQcn%2FHi7s4HGV%2FY4PpMCO1o%3D)

이런 효과를 구현하지 못한 이유는 투과율 함수가 근사치일 뿐이고 이 현상을 고려하지 않았습니다.

구름 표면은 항상 받는 빛에너지와 동일한 에너지를 가집니다. ( 깊이에 따른 통계적 확률로 생각합시다. )

구름 깊숙이 들어갈 수록 in-scattering의 잠재량이 증가하여 더 많은 빛이 눈에 도달합니다.

이 두개의 식을 합치면 Beer's Powder approximation method를 얻을 수 있습니다.

![](https://blog.kakaocdn.net/dna/nZ6kC/btsPoLrwOuf/AAAAAAAAAAAAAAAAAAAAAKeutimtmyu0OvNhQ-0U4Sxf1-UF8kycn8wvkQREdxqn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=CKjz9A%2BXppA2t3Ooq9rbLQNRVPM%3D)
![](https://blog.kakaocdn.net/dna/bwf6GQ/btsPnhrFUxk/AAAAAAAAAAAAAAAAAAAAAMjb3BIHeIQreO-v_RdoSYvqIFKVcjpLgTC6Hmwcldj5/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=mxcymRKNBu2D0FTmfQxhPJcjSqM%3D)
![](https://blog.kakaocdn.net/dna/bmMRZu/btsPnL6YrSs/AAAAAAAAAAAAAAAAAAAAAETK4C-569kJWUjDYLygR7tR29omUf3kyD-g-jKSi0sK/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fkRYQb7Kw0tzw0eTWr3ZoQyprHA%3D)

beer lambert: 깊이에 따라 지수적으로 밝기 감소

powder effect:  포면 바로 근처에서 bright peak치를 찍고, 깊어질수록 점차 포화, 빛 방향을 향한 면에서 어두운 가장자리가 강조되고, 오목한 부분이 더 밝음

beer + podwer: 표면에서는 파우더 효과로 밝은 peak, 깊어질 수록 beer's law의 자연스러운 밝기 페이드 아웃

이건 왜 이렇게 예쁘게 찍혔는지... 어쨌든 파우더 효과가 없죠

![](https://blog.kakaocdn.net/dna/OQIeY/btsPotLluLI/AAAAAAAAAAAAAAAAAAAAAKYL_rWj4ksNYQ9C8tqORUGbLnvXZmZSalt30WLy7uUM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=l1G2WHTHPRjMK6DntfwcnUVdEHE%3D)

파우더를 추가하면 이렇게 됩니다

좌측 파우더 X,  우측 파우더 O

![](https://blog.kakaocdn.net/dna/cqYBUJ/btsPnFMnh6U/AAAAAAAAAAAAAAAAAAAAAJt_DjZUpeLl7LxdjGaSwwKghbNb4Usiu_Z5tR9VVjzO/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FmEc71dMfi2gA%2BY1CmOhzDF2dc8%3D)![](https://blog.kakaocdn.net/dna/b9YieI/btsPoXyyn7g/AAAAAAAAAAAAAAAAAAAAADGrk-StYiOBMoY1AnoM2edmWzmcfLop8I-ZTOHa4g8_/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=c8AyUdJzUnhYWrK863VHXps0C%2F4%3D)

그냥 너무 밝아서 그런거아님? 이라고 매섭게 의심하실 수도 있지만

빛을 줄여도 파우더 효과는 없는 것을 볼 수 있습니다.

( 파우더 효과: 표면보다 살짝 안쪽이 in scattering때문에 더 밝았다가, 나중되면 소멸되는 느낌)

![](https://blog.kakaocdn.net/dna/JAFSB/btsPnoq2J8X/AAAAAAAAAAAAAAAAAAAAABtC41dABwj7R8eU66dMApqjUoi8LbvAnTiXRnnsIVtJ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=BIKDUj7iJlgNfmmdW6nu5vo280o%3D)![](https://blog.kakaocdn.net/dna/D74eB/btsPoXZD5pB/AAAAAAAAAAAAAAAAAAAAADlEncscvh1AfPLdyOPErJQbud-XK-J_mhQw3h602SuK/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=pL4ol%2BYr2Ru9UDKCH8ilZz5xtao%3D)



rendering부분은 ray marching 글로 대체하겠습니다!!  
  
공부할 수 있도록 기반을 다져준 홍쌤 샤라웃하고 떠나겠습니다! 감사합니다!

<https://www.honglab.ai/>

[honglab

그래픽스 새싹코스 파트2,3,4 묶음판매 Bundle • 3 learning products [그래픽스 새싹코스 번들] 파트1 공부 후 더 자세하게 배우고 싶은 분들을 위해 10% 할인된 가격으로 파트2,3,4 묶음판매를 진행합니

www.honglab.ai](https://www.honglab.ai/)

d