---
title: "[PhysicsForGameDeveloper] 등가속운동"
date: 2025-07-31
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

이번 장에서는 운동학(kinematics)의 핵심 개념들을 설명합니다.

구체적으로는 **선형 및 각 변위(linear and angular displacement)**, **속도(velocity)**, **가속도(acceleration)**에 대해 다룹니다.

### 

### **Introduction**

운동학은 **물체에 작용하는 힘과는 무관하게** 그 물체가 **어떻게 움직이는지를 연구하는 학문**입니다.  
따라서 운동학에서는 물체의 **위치, 속도, 가속도**에 초점을 맞추며,  
이러한 성질들이 **어떻게 서로 연관되고 시간이 지남에 따라 어떻게 변화하는지**를 분석합니다.

이번 장에서는 두 가지 유형의 물체를 다룹니다:

**1. 입자(particles)**

**2. 강체(rigid bodies)**

강체는 일정한 거리로 떨어진 입자들로 system으로,

입자들 간에는 **상대적 병진이나 회전이 없습니다**.

강체는 움직일 때 **형상이 변하지 않으며**, 형상의 변화가 있다 하더라도 그 변화가 **매우 작거나 중요하지 않기 때문에 무시할 수 있습니다.**

**하지만 강체(rigid body)**를 다룰 때는 물체의 **크기와 방향**이 중요하므로, **선운동(linear motion)**과 **회전운동(angular motion)** 모두를 고려해야 합니다.

반면, **입자(particle)는 질량은 있으나 크기나 형태는 무시할 수 있는 물체**로 간주됩니다.  
예를 들어, 투사체(projectile)나 로켓의 궤적을 다룰 때, 그 물체의 크기는 무시해도 되므로 **입자로 모델링**할 수 있습니다.

정리하면

마치 문제를 다룰 때 **줌 아웃**해서 전체 경로만 보는 것처럼, **입자는 **전체 궤적**만 분석하면 되는 반면**

( 입자를 다룰 때는 주로 **선운동**이 중요하고, **자체 회전은 중요하지 않습니다.** )

강체는 **자세와 회전까지도 세밀하게 분석해야 합니다.**

### 

### **Velocity and Acceleration**

입자든 강체든 관계없이, 운동학에서 **공통적으로 중요한 물리량**들이 있습니다.

1. 위치(position)

2. 속도(velocity)

3. 가속도(acceleration)

### 

### **Velocity**

일반적으로 속도는 **크기와 방향을 가진 벡터량**입니다.  
**속도의 크기를 보통 속력(speed)이라고 합니다.**

공식적으로,

**속력은 이동한 거리와 걸린 시간의 비율**을 의미하고

**속도는 변위와 걸린 시간의 비율을 의미합니다.**

![](https://blog.kakaocdn.net/dna/bjx7m5/btsPENJFMY9/AAAAAAAAAAAAAAAAAAAAALEB_LRMu4uiG_fciKZO_x0MOskCys3zHhIrnJI4c6i5/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=6QMPWpgkznAdaAKd4GD%2FUtw151A%3D)

예를 들어, 한 자동차가 직선 도로를 주행하고 있습니다.  
다음 두 지점을 지난다고 가정합니다:

![](https://blog.kakaocdn.net/dna/b4ZmEj/btsPCI36XVF/AAAAAAAAAAAAAAAAAAAAAB09Ilwh4XxJu93RhHb7sCrHAtTXC5s_6UeVVkn8ckIn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=SOndsqxBUA9sui9ytml48rd9SdM%3D)

t1=0초에 지점 1에서 출발

t2=1.136초에 지점에 도착

두 지점 사이 거리 s = 100 ft

일 때 속도를 계산해보자!

속도 = 변위 / 시간  => 100 ft / 1.135s => 88.03ft/s 임을 알 수 있다.

![](https://blog.kakaocdn.net/dna/czrZay/btsPDl8s1yW/AAAAAAAAAAAAAAAAAAAAAEUoEqJO3iw0g-QcyWhuHCNhVAKWw8H1HrsTDLevpaJT/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=gDvaNsAU70w1KHMMDxG7WuDRZ5U%3D)

방금 구한 속도는 평균 속도이기에, 이 시간동안 감속했는 지, 가속했는 지는 알 수 없다.

### 

### **Instantaneous Velocity(순간 속도)**

위 예시에서의 속도는 전체 구간의 **평균속도**입니다.

정확한 분석을 하려면, **어떤 한 순간의 속도**인 순간속도(instantaneous velocity)를 이해해야 합니다.

이 개념은 다음과 같은 극한으로 정의됩니다.

![](https://blog.kakaocdn.net/dna/nGpfa/btsPCiEyYFT/AAAAAAAAAAAAAAAAAAAAACWJU1vLG1xG_kg_IRwwdCScJaSYlivW7Ix-XLHNdnqV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=aOpZBRcDQHTeDddtAysMPsD75BM%3D)

**위치의 변화율 / 시간의 변화율**이 바로 순간 속도입니다.

(이것은 수학적으로 미분으로 표현됩니다.).

![](https://blog.kakaocdn.net/dna/yJmMv/btsPDr8yR93/AAAAAAAAAAAAAAAAAAAAADehAfo1uy3-QnSLYcYhgfbnixxBeeKEl_Lu_xrOrhCJ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1cpCsVVhUibHO3J9V%2F5f1CfsPBE%3D)

### 

### **속도와 변위 관계식**

속도와 변위의 관계는 아래와 같이 적분으로 정리할 수 있습니다:

![](https://blog.kakaocdn.net/dna/bIwmz2/btsPEsFMeXK/AAAAAAAAAAAAAAAAAAAAAHVPkYbxu7u0Ucv7WuwR25xVWa6Ql-u8D-G1WSv39ug_/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nr0394q26BxKFRV4hXSy3l7R%2FU4%3D)

**이 관계는 속도에 대한 적분이 변위임을 보여줍니다.**  
속도와 변위 간에 상호 변환할 수 있는 통로가 됩니다.

### 

### **변위와 거리의 차이**

**운동학에서는 변위(displacement)와 이동 거리(distance traveled)를 구분하는 것이 중요합니다.**

**변위:** 출발지점에서 도착 지점까지 직선거리

**이동거리:** 내가 도착하기 전까지 이동한 거리도 포함

**1차원에서는** 변위와 이동 거리가 같습니다.

하지만 **벡터 공간**에서 생각할 때, 변위는 단순히 이동 거리만이 아니라

**출발 지점과 도착 지점 사이의 벡터 차이**를 의미합니다.

**따라서, 전체 궤적이 직선이 아니라면 변위와 이동 거리는 다를 수 있습니다.**  
시간 간격이 매우 짧아질수록 변위와 거리는 비슷해집니다.

### 

### **Acceleration(가속도)**

가속도는 아마도 친숙할 개념일 것입니다.  
운전 경험을 떠올리면, 가속도는 **속도를 얼마나 빨리 증가시킬 수 있는지**를 의미합니다.

**가속도는 시간 변화율에 따른 속도 변화입니다.**

평균 가속도 공식

![](https://blog.kakaocdn.net/dna/FcCBg/btsPEphZoui/AAAAAAAAAAAAAAAAAAAAAG4XsQipx-djWE1EZnNonQIEvm_OJhobiVAWcE2B9D7P/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=8xe2KZ1V9ogPsJTCt5ZJmDEIg84%3D)

순간 가속도

![](https://blog.kakaocdn.net/dna/clWQMQ/btsPC5xYaOW/AAAAAAAAAAAAAAAAAAAAABb_QsPIVG6RyfFuVN08bi5fLV53Lb1T3XMAoem21Rqs/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=yglN9ZyGQOjSACC8LwH27fgHReU%3D)

### 

### **속도와 가속도의 적분 관계**

아래의 미분 방정식을 적분하여 다음과 같은 관계를 얻습니다.

![](https://blog.kakaocdn.net/dna/dt0xFG/btsPEtYZepD/AAAAAAAAAAAAAAAAAAAAANz8l9y4Z3-Q-s4THC-2zN-SQBNE9jNifRaP0RK1jaLC/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nDcZvWFdpFrOhEcDIoJxlbQ4AuI%3D)

운동학에서 주요한식들이다.

![](https://blog.kakaocdn.net/dna/IDFhY/btsPEwOWzWl/AAAAAAAAAAAAAAAAAAAAAMgruzTSKNbs1OIsbxDwDoCYoYozPlnvC8mSdjBX0m8M/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wM2mq%2B0StGtvRqC1LtoOP9t4cqg%3D)

첫 번째식은 v를 ds/dt로 치환하면 되고

두 번째식은 chain rule을 활용해서 아래와 같이 유도할 수 있다.

![](https://blog.kakaocdn.net/dna/JYHuw/btsPCSZWYrO/AAAAAAAAAAAAAAAAAAAAAGmCmH7ERadj2swwZuQ-Nq22ENlog145RwH-dTwT6tWo/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=M%2Bce%2BFTpa59T4GzPB9KqxN2AQGc%3D)

### 

### **등가속도(Constant Acceleration) 문제**

가장 간단한 운동학 문제 중 하나는 **가속도가 일정한 경우**입니다.  
대표적인 예는 지구 중력 가속도 g=32.174 ft/s^2 또는 9.8 m/s^2입니다.

가속도가 일정하면, 적분이 간단해집니다.

아래의 식을 적분해봅시다.

![](https://blog.kakaocdn.net/dna/bre4Y4/btsPDE00OG8/AAAAAAAAAAAAAAAAAAAAAG0iozcNnYhJJ0bpiYt87ILjoEp908QJ9onsm577BsXZ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=4zqgqsW6Wgg4v6qvTSQN7ZxVnNk%3D)
![](https://blog.kakaocdn.net/dna/WQ9ma/btsPCkbpd32/AAAAAAAAAAAAAAAAAAAAALCzF93c3ivQukA0gbYzmzfggOkkSjuUlyzpI5SdvauR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fsK9GxO1bKgsLWE6bFpqK98XsoM%3D)

t1 = 0이라면

![](https://blog.kakaocdn.net/dna/XAnDF/btsPDZ4ORe2/AAAAAAAAAAAAAAAAAAAAAJHi7Sjp_1UqpEkbohQipYyZRz3zCIiNWYKnrXbkT9qQ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=p3NgYXccMmV5jchmsEV0WZNqqZY%3D)

### 

### **속도를 변위로 표현하기**

시간이 아니라 변위 s를 기준으로 속도를 구할 수도 있습니다.

운동학 미분 방정식

![](https://blog.kakaocdn.net/dna/cs0Bt5/btsPE4qT7Ar/AAAAAAAAAAAAAAAAAAAAAElWEXdfq-ZfDGCZ1yu2S_VeL06kouP_I1prNIarPn_x/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=oZxIVRixdM723ejOe33Ta1BNi%2Bk%3D)

양 변을 적분하면

![](https://blog.kakaocdn.net/dna/UVGgB/btsPDGkeorD/AAAAAAAAAAAAAAAAAAAAACiI8OG_VzclFOoLaE3Chg43KF0M2HgxHT4ExPwILnwy/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Dcqe9SeRa35MoWk8g%2Bkdz9pnwps%3D)

### 

### **변위를 시간에 대해 표현**

이전의 순간 속도 식

![](https://blog.kakaocdn.net/dna/bVsjol/btsPC8hcBKh/AAAAAAAAAAAAAAAAAAAAAPMhHig0NLcY3n9ec4GiWSNWFx0BZkmUvWTA5dHlW8Ut/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=T8ycjFgqBDzL%2Fnncb7QFmq%2BskIQ%3D)

위 식을 이용해서 v = ds/dt를 다시 적분하면

![](https://blog.kakaocdn.net/dna/beXzP9/btsPEqOMhLD/AAAAAAAAAAAAAAAAAAAAAHqK_3UE67KZIkItcCgE99KTzl6D-xi0mitxmHGJay4n/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Y4IMernebyE48LQ%2B26%2F81zo44d8%3D)

대충 이렇게 전개됐다.

![](https://blog.kakaocdn.net/dna/dE6PUI/btsPDa0jO6k/AAAAAAAAAAAAAAAAAAAAABK3E3iGxCMCpK-IIx5j97HJusrITtaGNndgCKxgOCJC/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=eD74tXSDes8u9wSeDgQ9bSATgJo%3D)

### 

### **세 가지 기본 운동학 방정식 요약**

1. 속도

![](https://blog.kakaocdn.net/dna/PxqHj/btsPEMxeKTZ/AAAAAAAAAAAAAAAAAAAAAOTK8gALIrw9KhdJs_32DwyzWRyVUyOUHJRoR8XKM2sF/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=rgPbZ1ZCuOC6G%2FAjsi4SVyZJseU%3D)

2. 변위와 속도

![](https://blog.kakaocdn.net/dna/FOp31/btsPEqOMjwJ/AAAAAAAAAAAAAAAAAAAAAD3IF0aX_dOc2eLLEeIj46ZKp6FqXFpkEyuq_WJ1W34W/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=32CJMsSMb2vzOMGsai5YixJmBXM%3D)

3. 변위와 시간

![](https://blog.kakaocdn.net/dna/q88aj/btsPDXML5Tg/AAAAAAAAAAAAAAAAAAAAALpGWsecqeBBkrsXrCPrKXhJZw1zukAQGAoeo6uhrOsG/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=XVOrEaA9m4Xj64DXpjiSZ9Iud7c%3D)

조심해야 될 점은

위의 방적식들은 모두 등가속도 운동일 떄만 유요하다.

가속도가 시간, 속도, 위치 함수인 경우에는 이 식들을 그대로 쓰면 안된다!!

## 

## 비등가속도 (Nonconstant Acceleration)

아래 내용은 비등가속도 계산이 쉽지 않다는 것을 보여주기 위한 내용같습니다.

더보기

실제 세계의 문제에서 자주 나타나는 상황 중 하나는,  
**운동 중인 물체에 항력(drag force)이 작용하는 경우입니다.**

보통 항력은 속도의 제곱에 비례합니다.

뉴턴의 제2법칙 F=ma를 떠올려 보면,  
이러한 항력이 유도하는 가속도 역시 **속도의 제곱에 비례**함을 알 수 있습니다.

이 장에서는 이후에 항력 공식을 유도하는 몇 가지 기법을 보여주겠지만,  
지금은 항력 유도 가속도의 함수형을 다음과 같이 둡시다:

![](https://blog.kakaocdn.net/dna/cROQJL/btsPDZDNqej/AAAAAAAAAAAAAAAAAAAAAOCfhwuuO6ejbFOCaqtICzsOaWQEVTRNhY2RwS7urHrB/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=OtNOuqf7fd%2BKHPWKssYrsilaDug%3D)

여기서 k는 상수이며,  
마이너스 부호는 이 가속도가 물체의 속도 방향과 **반대 방향으로 작용**함을 나타냅니다.

이제 이 공식을 a=dv / dt에 대입하면

![](https://blog.kakaocdn.net/dna/s31Ky/btsPFjg4jUS/AAAAAAAAAAAAAAAAAAAAACIifmrtoZ0V2d1SncHSQYqC3g0cprgDodz5cJ-BQD4j/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=jDiaeFFPqE9s6LNkl2MuOO74Ncw%3D)

양변을 적분하면

![](https://blog.kakaocdn.net/dna/clvTbU/btsPENJH7P1/AAAAAAAAAAAAAAAAAAAAAPcozN7mgaw9PEvYrLofqDBQivRA4WMekKZYqqBygsAD/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=lK9hKIxqzKHwpNjblwf2%2Fz8Pjjk%3D)

다음과 같은 결과를 얻을 수 있습니다.

![](https://blog.kakaocdn.net/dna/GEsEg/btsPDDODIMI/AAAAAAAAAAAAAAAAAAAAAMnhPTz-kNLX1dzJD1hJPmtoG4928ynpvKTW00uJnKa4/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=0z%2B4McmXhjbg0d6fGyT7xERiKgY%3D)

v1(초기 속도)와 t(시간)에 따른 v2를 얻을 수 있습니다.

위 식의 v2에 ds/ dt를 넣고 다시 적분하면 s에 대한 표현식을 얻을 수 있습니다.

![](https://blog.kakaocdn.net/dna/bfelUQ/btsPDppuMze/AAAAAAAAAAAAAAAAAAAAABA4O0nyQOhijcGTndj9AF6QYkr2kPIAuAVjmBMtZ1w6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wcClpImOJ5szorgX3l9zGHg%2Bsms%3D)
![](https://blog.kakaocdn.net/dna/cFG1KS/btsPDl1HjSU/AAAAAAAAAAAAAAAAAAAAALgQBYgH008AjkjmBCZeSE00J8tb9OI1tluQZZpYsfdd/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FN5rY%2Fb8VkYLK3Meu7RXqH3hGlI%3D)

s1이 0이라면

![](https://blog.kakaocdn.net/dna/bqVsjC/btsPEqONs8b/AAAAAAAAAAAAAAAAAAAAAE37yDqZgO-G4iDgo-VeE5rO7gsvQvuttqeLx59hdyIT/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=kBomv%2B07dqpBONYQg%2FpTGbBGcHA%3D)

이렇게 됩니다.

이 예제는 **비등가속도 문제**가 등가속도 문제에 비해 얼마나 **복잡**해질 수 있는지를 보여주는 사례입니다.

이 경우는 비교적 단순한 예이기 때문에 속도와 위치에 대한 **해석적인(Closed-form) 해**를 구할 수 있었지만,  
현실에서는 여러 힘이 동시에 작용하면서 가속도 표현이 훨씬 복잡해진다.

이런 경우 해석적 해를 구하는 것이 거의 불가능할 수 있고,  
그래서 **수치 해석(Numerical Integration)** 같은 기법을 사용해야 합니다.

이런 문제는 11장에서 다루겠습니다