---
title: "[UE5/언리얼5] 블루프린트(BluePrint) 튜토리얼- Get,Set #2"
date: 2022-12-25
toc: true
categories:
  - "Tistory"
tags:
  - "언리얼5 #UE5 #언리얼일지 #Get #Set #언리얼변수 #언리얼공부 #언리얼독학 # 언리얼입문"
  - "언리얼튜토리얼"
---

내가 이해하는 방법

Get : Read => 데이터를 읽는다.

Set : Write => 데이터 값을 바꾼다, 새로운 데이터 값을 쓴다.

Get, Set 함수를 쓰는 법(단축키)

1. 드래그 -> Get or Set 선택

2. Alt + 드래그 : Set

3. Ctrl + 드래그 : Get

(드래그 : 왼편에 있는 Variables에 있는 변수를 EventGraph에 드래그 드롭하는 것을 의미)

미래의 나를 위한 코멘트 : (여기서 Read, Write는 대학교 컴퓨터 구조 시간에 배운 개념이다.)

아직 언리얼을 많이 써보지는않았지만, C/C++를 공부했기에 이렇게 이해하면 맞을 것입니다!

우선 Get, Set 함수의 모양새입니다.

![](https://blog.kakaocdn.net/dna/by6FGQ/btrUtGgGdqC/AAAAAAAAAAAAAAAAAAAAAO-qpjL8XhTI6ONBwn8_tKA8wrZ6u3SktwgvpKc653LM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=EqQPsFkyjajHjn2j9COuBKUo13I%3D)

Set 사용법( Hp 값을 바꾸기): 화살표를 이어준다 -> Hp[0] 으로 표시된 부분의 값을 바꿔준다 -> Hp의 값이 바뀐다 -> 끝

![](https://blog.kakaocdn.net/dna/cv14hz/btrUzlVYL2B/AAAAAAAAAAAAAAAAAAAAAO0wAquViQ_l5Eo3rb-IBC4D-BrPLAxEj2V4BtwUnUcZ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=SdCR1mYWO%2B9QiW6o1PTcjqssWa8%3D)

이렇게 매우 간단합니다.

![](https://blog.kakaocdn.net/dna/xIXge/btrUwqp2tW3/AAAAAAAAAAAAAAAAAAAAAHbOT88mjruOoft-cU2o3DeUta66gpnCTT4PeARe8WXM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=F1DV7Tb51MkBKoepmMNBa1qDf1s%3D)

============================================================================================

Get 사용법(Hp값 출력)

흰색 두꺼운 화살표 : 프로그램 진행 순서

아래의 그림을 설명하면

Set(Hp를 50으로 바꾼다) -> printText를 한다 -> Text를 확인(check) -> Hp랑 연결되어있네? -> To Text(int형 Hp를 Text형으로 변환) -> Text형으로 변환된 Hp출력 ->끝

제가 이해한 순서도는 2번째 그림이다

(4, 5번째는 정확하게 언제 실행되는 지는 모르겠다..근데 그렇게 중요하진 않다)

=>(3 -> 4 -> 5 의 정확한 의미는 3번이 완료되고 4,5번이 실행되는 것이 아니라

     3번 실행 중 print될 text를 확인하는 작업이 일어날 때 Hp값을 Text형으로 변환해서 가져온다는 의미입니다.)

![](https://blog.kakaocdn.net/dna/bGGHLW/btrUuG1h1WA/AAAAAAAAAAAAAAAAAAAAAOhrf210_BVksuu0rOzb2rQd_c_IAxbZA5BQPBaOebDP/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=PjKgnHpRdPdyW8Mj7xQisDRRER0%3D)
![](https://blog.kakaocdn.net/dna/dfQTgo/btrUuqYtQaH/AAAAAAAAAAAAAAAAAAAAAOShrwjWxv6X1hNL0CYpFEJ74uanoVy4cy5oIF3CbqZb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=4yVzmrr0OHY2IXhEYccnX9%2B%2FrU4%3D)

풀어본 실습 1

초기설정 : int MaxHp =100 , int OnDamaged = -10

int형 변수 Hp를 MaxHp로 초기화하고 OnDamaged만큼의 피해량을 Hp에 가한다.

그리고 Hp를 출력하라

내가 풀어본 답:

![](https://blog.kakaocdn.net/dna/cltxP8/btrUtK4AGFI/AAAAAAAAAAAAAAAAAAAAABRw07sv2X8qw3EuPFxs8WAZ7cpV8JMjP5XXArgd-f9l/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=kTC8glQoXdkjxaDPfzMTXwAhq1w%3D)

결과 : -10

이렇게 하게 되면 연산을 실행하는 것이 아니라 값을 넣어주는 행동을 한다.

이 문제를 풀기 위해서 다음 시간에 사칙연산을 배워보겠다.