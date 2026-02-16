---
title: "[MultiCoreProgramming] 멀티프로세서의 종류"
date: 2024-09-26
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

## **0. 병렬 컴퓨터**

병렬 컴퓨터는(A parallel Computer) PE(processing elements)의 집합이다.

PE : 큰 문제를 빠르게 풀기위해 cooperate, communicate하는 연산 유닛

(  cooperate, communicate  => 서로 데이터를 주고 받는다.)

병렬 구조 (Parallel Architecture)

= Computer Architecture(컴퓨터 구조) + Communication Architecture (=> 서로 데이터를 주고 받는 구조)

## 

## **1. 메모리에 관한 멀티 프로세서 종류**

### 

### **Centralized Memory Multiprocessor** (중앙 집중형 메모리 멀티프로세서, SMP)

* **소수의 프로세서**(수십 개 미만)와 코어를 갖는 시스템이다. (in 2006)
* 모든 프로세서가 single centralized memory를 공유한다. (공유할 수 있을 만큼 프로세서들이 작다. 병목 현상이 적다.)
* 어떤 메모리(memory1)에 접근할 떄 프로세서들의 latency가 **동일하다**. (접근하는데 걸리는 시간이 동일하다)
* SMPs(symmetric multiprocessors)라고도 불린다. 모든 프로세서가 **단일 메인 메모리**와 **대칭적 관계**를 가지기 때문이다.
* 캐시가 크면 메인 메모리에 가지 않아도 된다. (대역폭에 대한 요구가 줄어든다. 버틀락이 줄어든다.)
* Switch와 Memory bank를 이용하면 몇 십개의 프로세서까지 확장시킬 수 있다.
  + switch는 프로세서와 메모리 간의 데이터 흐름을 관리하고, memory bank는 메모리 접근을 병렬화하여 시스템 전체의 대역폭을 향상시킨다.
* 기술적으로는 더 많은 프로세서를 사용하는 것이 가능하지만, **프로세서가 많아질수록 중앙 메모리를 공유하는 것이 비효율적**이 됩니다.

**UMA (Uniform Memory Access time)**

* **공유 주소 공간**을 사용하는 **중앙 집중형 메모리** 구조로, **모든 프로세서가 동일한 시간**에 메모리에 접근할 수 있습니다.
* 즉, **모든 프로세서가 메모리 접근 시 같은 지연 시간**을 가집니다.

![](https://blog.kakaocdn.net/dna/bCrNsL/btsJJDnfSmi/AAAAAAAAAAAAAAAAAAAAAFvkTZMRDj_hHH9nRPFwHmD5ZOOFOFDZPqHU1Wir9L1w/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=FZEkpXZ%2BK48GsVbCEeS1A9sguWg%3D)

### **Physically Distributed-Memory multiprocessor** (물리적으로 분산된 메모리 멀티프로세서, DSM)

* **더 많은 프로세서와 코어**를 포함한 시스템.
* explicit하게 프로그래밍을 해야된다. (~주소에 저장해줘, ~에 write해줘, ~를 read 해줘)
* 프로세서가 많이질수록 bandwidth 요구가 커진다.(병목 현상이 커진다.) 그래서 **centralized memory(단일 중앙 메모리)**를 사용하는 대신 **각 프로세서가 자체적인 메모리**를 가지는 **분산 메모리 구조**로 설계됩니다.
* 어떤 메모리(memory1)에 접근할 떄 프로세서들의 latency가 **다르다**. (접근하는데 걸리는 시간이 다르다.)
* 로컬 메모리를 접근할 때에는 접근 시간을 줄일 수 있다.
* 프로세서간의 통신이 복잡하다
* BW(band width)의 이점을 증가시키기 위해서는 소프트웨어를 수정해야한다.

**NUMA (Non Uniform Memory Access time)**

* **공유 주소 공간**을 사용하지만, **분산 메모리** 구조를 갖는 시스템입니다. 각 프로세서가 **로컬 메모리**와 **다른 프로세서의 메모리**에 접근할 때 걸리는 **시간이 다릅니다**.
* 즉, **로컬 메모리에는 더 빠르게 접근**할 수 있지만, **다른 프로세서의 메모리에는 더 느리게** 접근합니다.

![](https://blog.kakaocdn.net/dna/bq9cEf/btsJKE6k2vR/AAAAAAAAAAAAAAAAAAAAAC9-B2wXy_e4ReRmyTQDp7HMQrrpcQjWrZ5NHQCFmg5-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=HateYlFsdNG8iGvIgMg45vwO%2Fcg%3D)

## 

## **2. 멀티프로세서간의 통신 방법**

**Message-passing MultiProcessors**

* 각 프로세서가 **명시적으로(explicitly) 메시지를 주고받는 방식**으로 통신합니다.
* 프로세서 간 데이터를 주고받을 때, **메시지를 전달**해서 정보를 공유하는 구조입니다

**Shared Memory Multiprocessors**

* load와 stores를 통해 **공유된 주소 공간**에서 통신이 이루어집니다.
* 프로세서들이 **공유 메모리**를 통해 데이터를 주고받으며, 서로 동일한 주소 공간을 사용합니다

## 

## **3. Amdahl's Low**

Amdahl's Law은 **시스템의 성능**을 병렬화했을 때! **얼마나 향상**시킬 수 있는지를 설명하는 공식입니다.

이는 특정 작업에서 **병렬화가 가능한 작업**과 **병렬화가 불가능한****작업**이 주어진 경우,

병렬화를 통해 기대하는 성능향상에 이루기 위해, 필요로 되어지는 병렬 작업의 정확도가 어느정도인지 계산할 수 있다.

100개의 프로세서가 있을 때, 80배의 속도를 높이고 싶다면 (프로세서 1개일 때)

sequental(병렬화가 불가능한 작업)의 비율은 어느 정도여야할까?

**1:** 작업량

**S0**: 병렬화 후, 전체 시스템의 속도 향상 비율 (Speedup, %)

**S1:** 병렬화 된 부분의 속도 향상 비율 (프로세서가 100개가 되면 100만큼 더 향상됨)

**f** : 병렬화가 가능한 작업의 비율 (전체 작업 중 병렬 처리 가능한 부분, 0~1)

여기서 중요한 것은 **전체 작업 중 병렬화가 불가능한 부분**이 클수록, 즉 **1 - f**가 커질수록 병렬화를 하더라도 성능 향상에는 한계가 있다는 점입니다.

![](https://blog.kakaocdn.net/dna/bPRSSo/btsJL1Pl4t8/AAAAAAAAAAAAAAAAAAAAAC3-CrvOAfToz2X_KRhR9vhzLBPm2Y30q56G3gmfgb0B/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=adMB%2F4g6%2FaBvXg6LtRaN2M1Wfu4%3D)

0.25%만이 병렬로 처리가 안될 때 100개의 프로세서를 병렬로하면

80%의 가속을 얻을 수 있다.

32개의 CPU, 2GHz, 원격 메모리 액세스 시간은 200ns이다.

로컬 메모리에 접근하여 hit했을 때의 CPI는 0.5입니다.

remote memory 접근 400 사이클( =200ns / 0.5ns)이다.

(CPI: cycle per instruction)

이때 0.2%가 remote메모리에 접근해야 된다면 성능이 어떤 영향을 줄까

CPI = Base CPI + Remote request rate \* Remote request cost이다

        = 0.5(local memory 확인해보기) + 0.2% \* 400 (local에 없으니 remote memory로)

        = 1.3

성능 향상 비율 = CPI 세로운 / CPI 기본 = 1.3 / 0.5 = 2.6배

2.6배 만큼 저하된다.