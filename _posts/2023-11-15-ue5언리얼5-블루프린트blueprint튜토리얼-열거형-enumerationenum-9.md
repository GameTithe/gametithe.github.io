---
title: "[UE5/언리얼5] 블루프린트(BluePrint)튜토리얼 - 열거형 Enumeration(Enum) #9"
date: 2023-11-15
toc: true
categories:
  - "Tistory"
tags:
  - "enum"
  - "Enumeration"
  - "언리얼5 #UE5 #언리얼일지 #사칙연산 #0출력 #언리얼변수 #언리얼공부 #언리얼독학 # 언리얼입문"
  - "열거형"
---

## **Enum**

**코딩할 떄 많이 써봤을 것이다.**

**이것을 언리얼 엔진에서 사용해 보자.**

**1.  Content Browser 에서 우클릭 -> Blueprints -> Enumeration 클릭  해서 Enum을 만들어준다.**

![](https://blog.kakaocdn.net/dna/LD9qG/btsAhdEgoHE/AAAAAAAAAAAAAAAAAAAAADRwCKZyOP1-tGsFid-zUUy5MfWkpDUUejLtbsD4dU4s/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=EB629IuihOUN6CiY0y9Zmb4rUCs%3D)

![](https://blog.kakaocdn.net/dna/bj9zH3/btsAa8XRkCt/AAAAAAAAAAAAAAAAAAAAAK7Z8cnmu1klZKHBIYGevp9SRlzy__xXNku5DuynXCKG/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=4epE893JJ1esFYfHn51KudnIZ5s%3D)

**2. 만들어준 Enum의 이름을 설정하고 더블 클릭 -> Enumerator를 필요한 만큼 추가 및 이름 설정을 한다**.

![](https://blog.kakaocdn.net/dna/lEP2a/btsAkkbk9Ht/AAAAAAAAAAAAAAAAAAAAANrrwc6lBc92Ax_V3SwMGjMTbcKphT-6HF1tRA7F8opM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=235n88MUa5sQkN9zss98aMYtRAU%3D)

**3. Level Blueprint 에 들어가서 변수를 만든다 -> 타입을 만들어준 Enum  타입으로 설정할 수 있다.**

![](https://blog.kakaocdn.net/dna/cxAFcv/btsAmyf5hwr/AAAAAAAAAAAAAAAAAAAAANdUlHc-DunhAEF2zDIkWkGCYlRYLbSHo3_Gvnl1gqY6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=LuNzFxyV9BGkmb7KpPoYMXsoY6g%3D)

+

1. Enum To string ( 열거형에서 문자열로)

Enum to string을 통해서 문자열로도 출력할 수 있다.

![](https://blog.kakaocdn.net/dna/bndJuD/btsAnBq4yJf/AAAAAAAAAAAAAAAAAAAAAOSDDKONTLxCyLT_4RXm3sm6DUGrOL5uVPE68f1ugBHp/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=z06Cthje3KHG17POQwmmASt9DjE%3D)

2. Int to Enum ( 정수에서 열거형으로 )

- ToByte를 통해서 Byte로 먼저 바꿔준다.

- ByteToEnum 열거형이름  으로 바꿔준다.

만약에 다른 형태로 바꾸고 싶은데 잘 안된다면

구글에 Blueprint 변수타입 To 변수타입 이라고 치면 잘 사람들이 먼저 질문한 것들이 존재할 것이다.