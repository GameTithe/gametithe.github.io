---
title: "[RDM Plugin] 멀티쓰레딩 최적화"
date: 2026-02-09
toc: true
categories:
  - "UE5_Plugins"
sub_category: "Realtime Destructible Mesh"
tags:
  - "UE5_Plugin"
---

우리 플러그인인 Realtime Destructible Mesh에서의 가장큰 병목은 Boolean Operation 연산이라고 파악이 되었고, 이를 해결하기 위해서 멀티쓰레딩을 도입했습니다.

언리얼 엔진에서 제공해주는 AsyncTask와 ParallelFor를 활용해 속도를 개선하는 과정과,

그 과정에서 발견한 쓰레드가 많다고 반드시 빨라지는 것이 아니라는 것을 공유하는 글입니다.

참고한 문서입니다.

<https://dev.epicgames.com/community/learning/tutorials/BdmJ/unreal-engine-multithreading-techniques>

[Unreal Engine Multithreading Techniques | Community tutorial

Unreal Engine Multithreading Techniques is a concise 27-minute tutorial designed to introduce the learner to the essentials of multithreading in Unreal ...

dev.epicgames.com](https://dev.epicgames.com/community/learning/tutorials/BdmJ/unreal-engine-multithreading-techniques)

### Async, AsyncTask

![](https://blog.kakaocdn.net/dna/EgeMi/dJMcabQlyyc/AAAAAAAAAAAAAAAAAAAAAHARWswvWfz6-YB8boZHj2w4Bm0jILLuFN773cNuqx_P/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KRGhxcXwYz8las2j0%2Bnt4ZgdRnQ%3D)

Async 를 사용하면 언리얼 내장 Thread Pool을 사용할 수 있기 때문에 사용자가 직접 관리하지 않아도 된다.

![](https://blog.kakaocdn.net/dna/1FY0b/dJMcai2XjC1/AAAAAAAAAAAAAAAAAAAAAJZrEfEW2wG70zPFQ3kzJpCDJBJ6CdUli9B-ruKXYYT6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wZTZhTKCnOpOd0%2B05I4luI3bEzI%3D)

AsyncTaskd의 AnyBackgrounThreadNormalTask를 사용하게되면 가벼운 작업을 언리얼 스레드풀에 예약할 수 있다.

작업이 할당되면 실행 후 잊어버리는 방식이다.

즉 백그라운드 스레드에서 비동기적 실행이 진행되고, Gamethread는 결과 대기하지 않는 방식이다.

메인 스레드 접근이 필요한 엔진 객체와 상호 작용하는 상황에서도 사용할 수 있다. 유용하게 쓰일 것이다.

AsyncTak를 통해서 람다함수를 게임 스레드가 실행시키도록 설정할 수있다.

```
AsyncTask(ENamedThreads::GameThread, [](){})
```

GameThread를 지정하고 싶으면 위와 같이 하면된다.

이렇게 하면 메인 Game Loop가 돌 떄 처리하는 TaskGraph의 게임 스레드 큐에 작업을 넣게 된다.

(우리 프로젝트에서는 Boolean Operation이 끝나고 Set Mesh를 GameThread에서 진행할 수 있도록 AsyncTask를 사용했다.)

|  |  |  |
| --- | --- | --- |
|  | AsyncTask | Async |
| 리턴값 | 없음 | TFuture<T> |
| 결과 대기 | 작업이 언제 끝나는 지 알기 어렵다 | .Get()이나 .Wait()로 결과를 기다리거나 받을 수 있다. |
| 주요용도 | 단순 실행 / GameThread로 작업 넘기기 | 결과값이 필요한 비동기 계산 |

### Parallel For

![](https://blog.kakaocdn.net/dna/bJzCVj/dJMcadAAc0b/AAAAAAAAAAAAAAAAAAAAADgpEotESFCDT4XRSShEwBuWRkMJ9Yd4w423LQB7uuo8/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Oc7eCLZSDMrfIAbYDE3Vxe3Mx3k%3D)

데이터 병렬 처리를 위해 설계된 도구인 ParallelFor 함수이다.

수동으로 루프를 만들고, 스레드간 작업을 분배하는 작업을 자동으로 수행해준다.

일괄처리, 대량 계산, 독립적인 작업에 적합하다.

아래의 수치들은 Parallel for를 사용했을 때의 결과들입니다.

![](https://blog.kakaocdn.net/dna/H3kDh/dJMcahC1JIL/AAAAAAAAAAAAAAAAAAAAAOmOYsKNu9g84sg_bKXHnDcz1LgohRzGfNwFDRVubTc6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=F0yGBJBNatH6p6ckxVs4b16c90k%3D)
![](https://blog.kakaocdn.net/dna/dcoeF0/dJMcabpgZCW/AAAAAAAAAAAAAAAAAAAAACIFuYMP9_qgcyi7cZYBY2DRzn7Ca3hpBINJUujLP2Im/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=td1ISVQi3gEZ%2BnWenRJgKaxw3jw%3D)

#### 1. Bool Operator를 1개의 thread로 돌릴 때

824.5ms

![](https://blog.kakaocdn.net/dna/cuZsmA/dJMcafLZel8/AAAAAAAAAAAAAAAAAAAAAKcHMSSgmbPLbXsXBL40XJXshRcovVYNNHZ52kLAQMiM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=qlEQq1kfgKe29aljN0d6n%2FzEN34%3D)

#### 2. Bool Operator를 n개의 thread로 돌릴 때 ( 아직 적정 thread, batch size를 못 찾음 )

326.7 (ParallelFor)

소요시간이 반은 줄었다..!

![](https://blog.kakaocdn.net/dna/TNpFT/dJMcabbKFL5/AAAAAAAAAAAAAAAAAAAAAAlF3uW4lN0xQrxWyCtLbarYJmuf8PvUUC7Mz4WiGhUR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=v9Exa%2BPRNuR%2BQ1y6J4mTKAp0iGk%3D)

#### 본격적인 Thread의 영향력 테스트

현재 나의 환경에서의 thread 활용 가능 수는 26개이다.

1. Thread 1개 일 때

![](https://blog.kakaocdn.net/dna/cCT3yD/dJMcahQzvfM/AAAAAAAAAAAAAAAAAAAAAAHi7VOIRPw-kDNQ8bIC07eUtunNag1SmbrZhy0aOz7o/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=AhPxPBdJT9XSubdjauhJvhUTIB8%3D)

2. Thread 2개 일 때

![](https://blog.kakaocdn.net/dna/cqungx/dJMcagc4ccZ/AAAAAAAAAAAAAAAAAAAAAGuAjr0NDtSTUH_T1EWSJL9PbDiKVckg0aMIuaGcG7B0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fvj68xA8qvLRrHbDD53rqdi50tg%3D)

3. Thread 3개 일 때

![](https://blog.kakaocdn.net/dna/vGO16/dJMcaaYdItK/AAAAAAAAAAAAAAAAAAAAAO-TJUdUvWCplBGTTrKSuFgvfiaLqsjjU78-HLwfmU9B/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=v8Ovr0ELmiq8TrHII90PrSHcu3Y%3D)

3. Thread 4개 일 때

![](https://blog.kakaocdn.net/dna/uIWq1/dJMcacobZGy/AAAAAAAAAAAAAAAAAAAAADiEwwi6462KnGDwvEW6fj9EmHM-sO6KEbk2ZRIh-_vX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=VsF%2FiRITP72FiufWpNrQWApJE2g%3D)

4. Thread 5개 일 때

![](https://blog.kakaocdn.net/dna/l2JN4/dJMcahC1O0O/AAAAAAAAAAAAAAAAAAAAALk6YNEZx9AtYtFZoD0qRxZyQVlMShluHcFcIZaUjU7E/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=j13t%2FbmTTfR48SE67fcwnZhOZro%3D)

4. Thread 10개 일 때

![](https://blog.kakaocdn.net/dna/TDgi9/dJMcaaKF4Yh/AAAAAAAAAAAAAAAAAAAAADfVUdmOpPnJyZ6MDq0WUPu-nN2WUJAZ8VXzc7WhDSCV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=j55%2FoYMohnPIZM8dDh5vwcWwiEc%3D)

\

5. Thread 15개 일 때

![](https://blog.kakaocdn.net/dna/8Yze6/dJMcabpg4UH/AAAAAAAAAAAAAAAAAAAAAGyxTbhEOctmDZVzpl1jdBI_B5gnxPzwWrRFsFGKatwH/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=m4BhG0gjCGdGhmoJY2J3red4%2B7k%3D)

6.Thread 20개 일 때

![](https://blog.kakaocdn.net/dna/dscVNh/dJMcajt1Y0V/AAAAAAAAAAAAAAAAAAAAALUKJP2-E6VW1_wHHuS-QRj_GvhhV1By6BWaz_lhYsIN/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=MoHSnRBo6lgUZ2LtYOMkQCtk22s%3D)

7. 우리가 엔진에 적용되어 있는 Thread 수 정하는 algorithm

![](https://blog.kakaocdn.net/dna/HVbqs/dJMcagYqan8/AAAAAAAAAAAAAAAAAAAAAPi897UfXlPm7QhvUDEm8VDYRy7eIlkbDME4sA6-1ZnM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Q%2F3hlH0riD2PCAk5xJv320JqSRo%3D)

알게된 점

1. Thread의 수가 많다고 좋은게 아니다

2. Thread 1개 사용하는게 제일 빨랐다.

Thread가 많이질 수록 Overhead도 같이 발생한다.

1. Context Switching: Cpu 코어가 Thread를 교체하는 비용이 실제 연산 비용보다 커질 수 있다.

2. Cache Trashing: 여러 Thread가 서로 다른 메모리 영역을 건드리면서 L1/L2 Cache Hit 가 낮아진자.

3. Oversubscription (과잉 구독/대기): 그 아래 갈색 바 Oversubscription은 해당 스레드가 현재 물리적 코어 수보다 많은 작업을 요청했거나, 대기 상태에서 다른 스레드에게 자원을 양보하고 있음을 나타내는 상태입니다.

주로 ParallelFor가 끝날 때까지 메인 스레드가 블로킹될 때 나타납니다.

![](https://blog.kakaocdn.net/dna/9UC1d/dJMcacuYzku/AAAAAAAAAAAAAAAAAAAAAFFEoAZpD_FpY5mOi1w_NQHW9S9tCoelZTJ4Jgm-KSSI/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Hmx4ROBLVOUhiFV21Age8Pqapug%3D)

**Parallel for에서의 thread 수 비교**

**thread 12개일 때**

BooleanWorkerParallel\_ParallelFor 6개 처리 시간을 보면 0.04ms이다.

하지만 나머지 6개를 multi Thread를 돌렸을 때 13.3ms가 든다.

![](https://blog.kakaocdn.net/dna/CxpZR/dJMcacaFJMH/AAAAAAAAAAAAAAAAAAAAAM1wPcq3Vlwl-UZFQ8vlI_WqTy-vjjHV_81EbyDqUIh6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=qsHa0Gm79CXrvTnGKiwI%2BWeNtVk%3D)

**thread 1개일 때**

Parallel for 의 thread를 1개만 줘도 자꾸 다른작업에 끌려감

![](https://blog.kakaocdn.net/dna/nDgn0/dJMcabQmBN6/AAAAAAAAAAAAAAAAAAAAAM0J0LLsh7kCv2bvzME80XJ3CxipYI_yLyphG2XtdGkV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=2K9h6HelGAyxdGCazWLKVHPx3CE%3D)

 single로 돌릴려면 Parallel을 사용하지말자

### 결론

Parallel for보다 AsyncTask를 이용해서 최적화를 해보자