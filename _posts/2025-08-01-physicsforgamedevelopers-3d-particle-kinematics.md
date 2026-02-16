---
title: "[PhysicsForGameDevelopers] 3D Particle Kinematics"
date: 2025-08-01
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### 

### **3D 입자 운동학 (3D Particle Kinematics)**

앞에서 학습한 2D운동학 속성 벡터들을 3차원으로 확장하는 것은 그렇게 어렵지 않습니다.  
이는 단순히 벡터 표현에 한 개의 성분(컴포넌트)을 추가하는 것만으로도 충분합니다.

이전 섹션의 2D 운동학에서 본 것처럼, z 방향의 단위 벡터 k를 도입하면 다음과 같이 쓸 수 있습니다

![](https://blog.kakaocdn.net/dna/b8vVjP/btsPE2fGcWz/AAAAAAAAAAAAAAAAAAAAABudys5VtSn5uRJEgVQiXPLd697kCgq7AB0f2-M1uclw/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Q0W7iAPcLxluuB30b3%2BzOTFyPTk%3D)

이전에는 두 성분을 따로 다룬 후 합쳤다면, 이제는 세 성분을 따로따로 계산하고 그들을 합쳐서 결과 벡터를 정의합니다.  
이 과정을 가장 잘 보여주는 예제가 하나 있습니다.

2D예시를 보고오면 이해하기 더 좋습니다.

<https://tithingbygame.tistory.com/246>

[[PhysicsForGameDeveloper] 2D Particle Kinematics

2D 입자 운동학 (2D Particle Kinematics)1차원 운동, 즉 운동이 직선 상으로 제한되는 경우에는 앞서 배운 공식을 그대로 적용하여순간 속도, 가속도, 위치 변화량 등을 쉽게 구할 수 있다. 하지만, 운동

tithingbygame.tistory.com](https://tithingbygame.tistory.com/246)

**상황 예시**  
전함에서 포탄을 목표물로 발사하는 게임을 만들고 있다고 가정해 봅시다.   
이 활동에 복잡도를 더하기 위해, 사용자에게 포탄의 궤도에 영향을 주는 여러 요소를 제어할 수 있도록 하면 좋습니다.

1. 포의 수평 및 수직 발사 각도

2. 포탄의 초속(muzzle velocity): 이는 포에 장전된 화약의 양에 의해 결정됨

![](https://blog.kakaocdn.net/dna/7L2zD/btsPDt6wKI5/AAAAAAAAAAAAAAAAAAAAABlRIPfawUWu6tXGMZKkrgPtSV2dnamrBMSOC-mviftq/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Q9WmNMMznQdhClPdl8aF6%2BR8p%2BI%3D)

### 

### **x 성분 (x-Components)**

x성분은 이전 소총 예제와 유사하게 목표물을 바라보는 방향입니다.

포탄에 작용하는 드래그(force)가 없다고 가정합니다.

=>따라서 x 방향 가속도는 0입니다.

즉, x 방향 속도는 일정하며 포탄이 포에서 나갈 때의 x-방향 속도와 같습니다.

하지만 항상 포를 수평으로 쏘는 것은 아니기에, 대포 방향에 맞는 x성분을 계산해야됩니다.

속도 벡터는 아래와 같습니다.

![](https://blog.kakaocdn.net/dna/F1ZVX/btsPFi3FDUp/AAAAAAAAAAAAAAAAAAAAAD7pb1EaFDc_pMOaX-fQP6XuX3kq3XdbTQXfa0H6tWlA/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Oyti2JDzhrQt%2BLWT6TALSUS9IUE%3D)

여기서 주어지는 것은 방향과 크기 뿐입니다. 방향은 사용자가 대포를 어떤 방향으로 조준했는지에 따라 정해지는 것이고, 크기는 화약?포탄? 의 양에 따라 달라질 것입니다.

속도의 성분을 계산하기 위해서 대포의 방향각들과 속도의 크기를 바탕으로 구성된 식이 필요합니다.

![](https://blog.kakaocdn.net/dna/b5vgfN/btsPENJQlRO/AAAAAAAAAAAAAAAAAAAAABRHEVfiBKr26Az6S3V-PNRUauoOQLTpkQAqaXnm1n2y/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=XZGouLZwRnA%2BEtpVevis7vg3TIA%3D)![](https://blog.kakaocdn.net/dna/cnyW69/btsPEsy7J3n/AAAAAAAAAAAAAAAAAAAAAJNg9d74FhXcDo8TsUfmCN_J5Ofu4y0U2Ic5akJ_G-Wh/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KwcID1AxJlO%2F%2FqVsiinljEksj04%3D)

속도 벡터의 방향이 대포의 조준 방향과 같다고 가정할 수 있으니, 대포 자체의 길이 L을 갖는 벡터로 보아 각도를 적용할 수 있다.

즉, 대포의 길이를 기준으로 한 벡터 성분을 이용하여 위의 방향 코사인 식을 대체할 수 있다.

![](https://blog.kakaocdn.net/dna/bcP6ww/btsPEoXPrTu/AAAAAAAAAAAAAAAAAAAAAOCJZwWhrGRh4q9222UyWrNKJNUARgDPTTJr1nZW7w8S/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=24x6FmRW1fSCD%2FSpS%2FD%2FkItOH7U%3D)

추가 설명

더보기

우리는 길이 L인 대포를 어떤 방향으로 조준중이다.

그 방향에 대해서 x,y,z 축이 얼마나 기여를 하고 있는지 알고 싶다.

그렇기 때문에 정규화를 한 후, 각 축과 이루는 각의 코사인 값을 구하는 것이다.

![](https://blog.kakaocdn.net/dna/bcP6ww/btsPEoXPrTu/AAAAAAAAAAAAAAAAAAAAAOCJZwWhrGRh4q9222UyWrNKJNUARgDPTTJr1nZW7w8S/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=24x6FmRW1fSCD%2FSpS%2FD%2FkItOH7U%3D)

정규화를 해주었으니 이 벡터의 크기는 항상 1이다.

![](https://blog.kakaocdn.net/dna/dFk5xK/btsPE7gUNtY/AAAAAAAAAAAAAAAAAAAAAC1My1j8CR5pdJK4SZbBcmbZITANByw00wGZ2sXaUyiy/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=YVbQH2JbUH9Roa61DsOibZTow40%3D)

즉, 정리하면

cos θx = Lx/ L 의 의미는 대포의 벡터의 방향 중 x축 방향으로 얼마나 향하고 있는 기여율을 나타내는 것이다.

위의 그림에서는 a,r이 주어지니

이러한 각도들을 사용하면, xz 평면 위로의 대포 길이 L의 투영값 b는 다음과 같이 구할 수 있을 것이다.

![](https://blog.kakaocdn.net/dna/JYoS4/btsPELFcZ9a/AAAAAAAAAAAAAAAAAAAAAInTRDJdGr1vC3ZIOA8ouZBuZ1VTAMh3_69VsS8L5mNp/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=688W9p4uUpU0IuV%2BJyhbQUHSa84%3D)

대포 길이 L의 각 좌표축에 대한 성분은 다음과 같다.   
(삼각함수를 알고있다면 이해가 될 것이다...!, 혹시 모르시면 댓글 남겨주세요 그림판으로 설명추가하겠습니다)

![](https://blog.kakaocdn.net/dna/bQLYai/btsPELeaRmf/AAAAAAAAAAAAAAAAAAAAAJHUxbKCnBXNdnbjpRgcRgFV9XK4NWIes7mYSqfSmmy6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hAL5ZKvJX77twgMLrRvUlK%2Fk55s%3D)

여기서 구한 Lx,Ly,Lz를 대입하면 방향 코사인을 계산할 수 있을 것이다.

이를 통해 속도의 각 성분을 다음과 같이 계산할 수 있다.

![](https://blog.kakaocdn.net/dna/bac5Ru/btsPEwO4YX2/AAAAAAAAAAAAAAAAAAAAAGIPBztNX3Fn_pA4O1Bel0tdiMsUkjZFJa2Jh4hTlU-A/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=JD3u2317zM8RTL8yI%2BiWfLmixT4%3D)

마지막으로, x-성분의 최종식이 완성됩니다.

![](https://blog.kakaocdn.net/dna/dN8RUp/btsPDFMtrk3/AAAAAAAAAAAAAAAAAAAAADDOPdd2_U72dResvjYHGmjbgBTw7unPXVHhgRXuuT7w/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Ih3y6F%2BiN2sspi9NHqcelnQMBpU%3D)

### 

### **y 성분 (y-Components)**

y성분도 소총 예제와 유사하지만, 초기 속도에 y성분이 있다는 점이 다릅니다.

위에서 구한 속도가 존재합니다.

![](https://blog.kakaocdn.net/dna/cCj6eJ/btsPC5rnO6T/AAAAAAAAAAAAAAAAAAAAAALJxd-tEtP5Cl8RghcYCd4cdh53J4eOpjC6IEdZ3of-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=vH8Z4nH%2B72akw0%2BKwWEOLB5HFJE%3D)

'

중력 가속도는 존재하니,

이를 통해서 v를 다시 업데이트 해줍니다.

![](https://blog.kakaocdn.net/dna/TO6Dk/btsPE6oRGdY/AAAAAAAAAAAAAAAAAAAAAJVYseWDNbyv1cumIGtXv2kcIVOoPIydjrlUW6iTtZID/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2BGez1b60W6pB1r6wHsHE81k3RWU%3D)

위의 식이 왜 이렇게 바뀌었는 지 이해가 어렵다면, 이 내용을 먼저 보고 오세요!

<https://tithingbygame.tistory.com/245>

[[PhysicsForGameDeveloper] 등가속운동

이번 장에서는 운동학(kinematics)의 핵심 개념들을 설명합니다.구체적으로는 선형 및 각 변위(linear and angular displacement), 속도(velocity), 가속도(acceleration)에 대해 다룹니다. Introduction운동학은 물체에

tithingbygame.tistory.com](https://tithingbygame.tistory.com/245)

y축 변위(displacement)의 식을 세우기 전에, 대포의 위치를 고려해야 합니다.  
즉, 대포의 높이와 포신 끝의 높이를 더해, 포탄이 처음 발사되는 초기 y 위치(y0)를 계산합니다.

여기서 L\*cos(α)는 위에서 구했었습니다!

![](https://blog.kakaocdn.net/dna/F4SyV/btsPDOo5UkB/AAAAAAAAAAAAAAAAAAAAAA2yGyApyx-J6cWNaROqVLx3hGxHlq_vuW-aKFLmW6at/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=7856%2FApikbhyeVciwTfqbDoiKlw%3D)

그럼 y성분의 최종식이 완성됩니다!!

![](https://blog.kakaocdn.net/dna/bR82wM/btsPEuwW9ks/AAAAAAAAAAAAAAAAAAAAADNMqvqX4Dgjkh_IMCqFx2p5QJKRc5jCnwbj6B7PLZyV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=HSqTO4cynTiJSvuEnva5vSDKFBA%3D)

### 

### **z-성분**

z-성분은 x-성분과 유사하며 다음과 같이 쓸 수 있습니다.

![](https://blog.kakaocdn.net/dna/tCy2s/btsPDpDanvC/AAAAAAAAAAAAAAAAAAAAADReLL_frs2hqqsdGLTGVE3pP0SQiR5quFQCPsGZOcSJ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ihfzn6E%2Fyrq3juL0Ubca%2BBQ6VsM%3D)

### **The Vector**

x,y,z 각 성분을 모두 구했으니 이제 합쳐봅시다!

![](https://blog.kakaocdn.net/dna/KqYfR/btsPDWgb3sF/AAAAAAAAAAAAAAAAAAAAAIAEf2p6wbw1ntxzPbkknyg6E7oRGya9aOrsqm2wEQHh/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9%2FAq%2BqCj5bT1YTYikoQEvZSLt2k%3D)

## 

## **Hitting the Target**

이제 포탄의 궤적을 완전히 기술하는 방정식을 다뤘으므로, **목표물이 어디 있는지**를 고려하여 **직격(hit)이 발생했는지 판단**해야 한다.

이를 위해 내가 만든 샘플 프로그램에서는, 이 운동 방정식들을 구현하고,  
**단순한 바운딩 박스 충돌 검사(bounding box collision detection)** 를 이용해 포탄이 목표에 명중했는지 확인하도록 했다.

![](https://blog.kakaocdn.net/dna/HVXtX/btsPDqIMOXn/AAAAAAAAAAAAAAAAAAAAADkdRZyKw5naxe3px97QWzs7pUGAlibr_RlklJsyFfqY/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=SoMV4EdspHiuP02qwsPT9ZqdbXk%3D)

아래는 책에 실려있는 시뮬레이션 코드의 일부를 발췌해왔습니다.

핵심 루프인 DoSimulation 함수입니다.

![](https://blog.kakaocdn.net/dna/bIovos/btsPDpXraBG/AAAAAAAAAAAAAAAAAAAAAKcRNO_Bw3yZsSTKPYCIyACv9sJeHIT4x37bNFWPvfsQ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=CI7Dfvo00O9DSJxCVlKEqpwluR4%3D)
![](https://blog.kakaocdn.net/dna/bTlVOO/btsPEwasP5G/AAAAAAAAAAAAAAAAAAAAAE9DrEBhrRhkLDOV5VfWuWBAd9M7q8T0AH2vHhH6UCiI/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=HVyQM5KN5%2BshiL4jhpWTFKwdPyA%3D)

Lx, Ly, Lz를 구해주고

![](https://blog.kakaocdn.net/dna/5TAAO/btsPCSluGQE/AAAAAAAAAAAAAAAAAAAAAFq-2rSqKeuV1pkeiN66HT9HSm0YytS2CbpiqsBesK8q/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=O%2Bcti2t9%2BKot5Z0eVlVRTMG345o%3D)

이를 활용해서 direction cosines(cosine direction ratio)을 구합니다.

![](https://blog.kakaocdn.net/dna/zMUlI/btsPEMqEJl2/AAAAAAAAAAAAAAAAAAAAANCA95LHCBaXLvpqdcC_c7fOJ0UVKNf82-ATqN-B7ovT/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=pl%2BG5nj4gjO6LgN3ZNA0BvWxoJI%3D)

x, z의 초기 위치를 구하는 코드입니다.

![](https://blog.kakaocdn.net/dna/bjpoyx/btsPDFeG9EZ/AAAAAAAAAAAAAAAAAAAAAML4toqli6Ik_kO78PdJlg0I-aWnl1KZYvTimB_wYL2T/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=isgLmJpJjjk2FG7x2%2FSBlcC8gVA%3D)
![](https://blog.kakaocdn.net/dna/WFFjt/btsPDWN00q9/AAAAAAAAAAAAAAAAAAAAAChqUY0ovQ9B6xX6fsjsBA6OzGo_LdtCA-Gf8XpYFS5-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=JPmpc7BWJZcdJuiECOHaXfG%2F1Fk%3D)

위에서 구했던 식 그대로 코드로 옮긴것 뿐입니다.

s.i 에는 xe가, s.k 에는 ze가 더해져있는데

단순히 초기 위치(s0)을 조정해준것입니다.

![](https://blog.kakaocdn.net/dna/b5TI1w/btsPEN37IAK/AAAAAAAAAAAAAAAAAAAAAGNb-vXq0RHFA8DcJSaZtimCGLrz3StUkKyrp0tmMU2I/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GAC5vpTONKQ51X3KBv3Pf1y%2BUfw%3D)
![](https://blog.kakaocdn.net/dna/bQ5NYD/btsPEpvFlth/AAAAAAAAAAAAAAAAAAAAAJonJ565UUVCqzySaFq5dMTtFMBtt8CUrPLU2u3FzCwY/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ObW5r1tfz%2FyM5j3FFQRekftX%2Fhg%3D)

그 아래 코드들은 충돌 처리 코드이기에 설명은 생략하겠습니다