---
title: "[UE5/언리얼5] 블루프린트(BluePrint)튜토리얼 - Gate, MultiGate, Do Once, Do N #8"
date: 2023-11-14
toc: true
categories:
  - "Tistory"
tags:
  - "#언리얼5 #UE5 #언리얼일지 #사칙연산 #0출력 #언리얼변수 #언리얼공부 #언리얼독학 # 언리얼입문 #Gate #MultiGate #DoOnce #DoN"
---

## **GATE**

![](https://blog.kakaocdn.net/dna/QLU5D/btsAjjKFlB1/AAAAAAAAAAAAAAAAAAAAAKXr0ab2ixPWMVetx9KfKmCg3WpobPivQQR5KzeiT3Xz/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fTsO2SovHy%2FPRnEHKqsJczyRX7Y%3D)

**Enter**

Open상태이면 Exit로

Close상태이면 무반응

( 기본 상태는 Open )

**Open**

Gate의 상태를 Open으로 바꿔준다

**Close**

Gate의 상태를 Close로 바꿔준다

**Toggle**

Gate의 상태를 반대로 바꿔준다

( Open -> Close / Close -> Open)

**Start Closed**

기본 상태를 Close로 설정한다.

## **MULTIGATE**

![](https://blog.kakaocdn.net/dna/cUPW6U/btsAmudy5u6/AAAAAAAAAAAAAAAAAAAAAOR2Y51yioV62Q3OnR8LLpThvzMMOvGA1lUUw34A7NO1/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=EwBqVLFyU89ZRPfhsmgEN25dasY%3D)

Gate와 유사하지만 Output이 많다고 생각하면된다.

**1** 을 눌러서 Out 0, Out 1, ... , Out N 을 모두 실행하면 **Close 상태로 바뀐다.**

**Reset**

상태를 Open으로 바꿔준다. **( 이때 다시 Out 0 부터 실행된다. )**

**IsRandom**

Out을 0 ~ N 순서대로 실행하지 않고, 랜덤으로 실행한다.

**Loop**

Out을 0 ~ N 을 모두 실행해도 Gate의 상태가 Close로 바뀌지 않고,

다시 Out 0 ~ N 까지 순서대로 실행된다.

**StartIndex**

시작 인덱스를 설정할 수 있다.

**Out n**

Add pin을 눌러서 Out의 수를 늘릴 수 있다.

## **DO ONCE**

![](https://blog.kakaocdn.net/dna/bylAD8/btsAaNztLhY/AAAAAAAAAAAAAAAAAAAAANQC-WDcwL50_j3OWimXqpSdphXjC_fLJacJc87WJYUL/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=oRWE5nORaQ1wmygjXgxjROq3Fxw%3D)

함수 이름과 같이 1번만 실행한다. 기본 상태 값은 Open상태이다.

1을 누르면 Completed와 연결된 부분을 실행한다. 그리고 더 이상 실행되지 않는다 ( Close 상태 )  
Reset을 눌러서 다시 Open을 해줘야된다.

**Reset**

연결된 부분을 실행하고 Close 상태로 바뀐다.

**Start Closed**

기본 상태 값을 Close로 설정한다.

**Completed**

Open일 때 실행 시킬 함수(?)와 연결되어 있다.

## **DO N**

![](https://blog.kakaocdn.net/dna/RLnrG/btsAmBcGGa0/AAAAAAAAAAAAAAAAAAAAAFcKYf5nfuc1o08_rx7RFBnmC53PuRgOBtuLVg2ewv_v/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=a1ZcZzHa%2Fcfi6dBhAG0cCR9C5lg%3D)

Do once와 유사한 함수이지만, 이름과 같이 여러번 ( N번 ) 실행시킨다고 생각하면 된다.

**Enter**  
Counter가 N보다 작을 때 Exit와 연결된 함수를 실행시킨다.

**N**

몇 번 실행할지 설정한다.

설정한 수만큼 실행한 이후에는 상태를 Close로 바꾼다.

**Reset**

Counter를 0으로 초기화

**Exit**

실행할 함수와 연결되어 있다.

**Counter**

몇 번 실행시켰는지 카운트 해주는 변수이다.

1번 실행 될 때 마다 1씩 증가한다. (아래의 그림처럼 Counter를 로그로 출력할 수 있다.)

![](https://blog.kakaocdn.net/dna/qnnLq/btsAjQnWkeD/AAAAAAAAAAAAAAAAAAAAADrJ_a39ejwbjE5XSzUsN3u9K_Yk9EN-h5l8zT8jyeJb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=zguQsvjmTp9voSydR9Y2Msop440%3D)