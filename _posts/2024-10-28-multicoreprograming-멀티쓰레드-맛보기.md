---
title: "[MultiCorePrograming] 멀티쓰레드 맛보기"
date: 2024-10-28
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

아래의 코드는 전역변수 sum에 +2를  25000000번하는 것이다.

**Lock없이** 멀티쓰레드 코드를 실행했을 때

![](https://blog.kakaocdn.net/dna/cOOVWH/btsKnihilYP/AAAAAAAAAAAAAAAAAAAAAH8ZhfzzJnH5dw1uNI5suoRrOgUGtqNg7Mc184K2ofvP/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=MVLw6xnCqzAJJnmz823uSACaZ24%3D)

**왜 값이 다르게 나오나요?**

![](https://blog.kakaocdn.net/dna/GvbQ9/btsKl6WqjgP/AAAAAAAAAAAAAAAAAAAAAOObSN1632zfOM0dyzI3NrlBBhLn0VkiW5nbFEbWybGv/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=uYitERpvpqvzhXxKXbFEhGK31Hg%3D)

**사실 덧셈 연산자의 어셈블리 코드를 보면 위와 같이 3개의 단계로 나눠져있다.**

**1. SUM에 있는 값을 EAX로 이동**

**2. EAX에 있는 값에 +2**

**3. EAX에 있는 값을 SUM으로 이동**

이런 과정을 거치는데 **더한 값을 다시 SUM에 가져다 놓기 전에 ( +2가 안된 값)**다른 thread가 SUM에 있는 값을 가져가서 연산을 시작한다면

**1번의 SUM연산이 사라진 것이다.**

이렇게 lock을 걸지 않고 공유데이터에 자유롭게 write를 하면 결과값에 오류가 생긴다.

**무식하게 Lock**을 했을 떄

![](https://blog.kakaocdn.net/dna/ck9rdX/btsKlsyQeNp/AAAAAAAAAAAAAAAAAAAAAAIQd5pwrv8PJIO-xxAHiBVqWBspTxPPo0I9x5OM9OSd/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=YIRFuSw1Jr6UKNN25xyrLeLTGw4%3D)

**Atomic**연산자를 썼을 때

![](https://blog.kakaocdn.net/dna/sjgYg/btsKnhQcG5Z/AAAAAAAAAAAAAAAAAAAAAHeSxwzFIUweIpL_JutMcIZVlLDK8Xu1Ei5gaxforndU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=T9lcDnuUy7gF0Knb5QJSRKE3klQ%3D)

**Data Race를 줄였을 때**

![](https://blog.kakaocdn.net/dna/b8mKDX/btsKl6hR5XS/AAAAAAAAAAAAAAAAAAAAAPgd8XtZ3RHpWH4Oi9Xkq-fMpyYPC8CHp8UIP3bJop0b/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3IS5cfWcBio4hbqAYKclJTkD1%2Fg%3D)

데이터 레이스를 줄였을 때가 되어야지 Thread 3개를 쓴 것이 단일 쓰레드 보다 빨라진다.

Lock, Atomic연산자를 쓴것을 보면 단일 쓰레드보다 느리다.

Lock을 쓰지 않으면 결과값이 달라진다.

느리거나, 결과가 틀리다면 멀티쓰레드를 쓸 이유가 없다...

아래는 실습코드이다. 한번씩 돌려보자

**무식한 LOCK**

![](https://blog.kakaocdn.net/dna/nYB5W/btsKlW0TPVa/AAAAAAAAAAAAAAAAAAAAANRU_1P2sDtOc_QJbcYFO-8b4-fb92mAf17BanRy3ktb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=u91idturmexI7D3H72XsGAu6D3M%3D)

**DataRace줄이는 방법**

![](https://blog.kakaocdn.net/dna/cI4nsV/btsKm44HHnX/AAAAAAAAAAAAAAAAAAAAAO9yYktDcyOJWU6UdFGTBFwgTe-RYRI-EZeG8S5AlwYw/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hv3aXvB7MrlmY1qDd2yEnl28pg8%3D)

앞의 3개는 +2할 때마다 lock을 했지만

여기서는 local 변수 localSum을 이용해서 +2를 lock없이하고,

마지막에 전역변수에 더할 때만 atomic연산자로 더한다.

DataRace가 굉장히 줄었고, 그 덕분에 속도도 빨라졌다. 결과 값도 당연히 정확하다.