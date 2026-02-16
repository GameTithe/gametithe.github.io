---
title: "[UE5/언리얼5] 블루프린트(BluePrint)튜토리얼 - 데이터(DataTable) 입력하기 #10"
date: 2023-12-14
toc: true
categories:
  - "Tistory"
tags:
  - "data"
  - "DataTable"
  - "Enumeration"
  - "언리얼5 #UE5 #언리얼일지 #사칙연산 #0출력 #언리얼변수 #언리얼공부 #언리얼독학 #언리얼입문"
---

몬스터, 플레이어 공통으로 갖고있는 데이터를 새로운 종(?)를 만들어 줄 때 마다 같은 작업을 하는 것은 귀찮을 일이다.

데이터 테이블을 만들어서 쉽게 해결 해 보자

## 

**1. Struct를 만들어서 CreatrueData로 만들어 준다.**

여기에 공통으로 사용되는 데이터들을 넣어 줄 것이다.

![](https://blog.kakaocdn.net/dna/pwZ0n/btsB1va5woT/AAAAAAAAAAAAAAAAAAAAANKWZ-hiK79vzyC0RCFGy6SfDVz-j5qSzp8IGIGlHjXf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=BLnQa8TeEyg05hIXD9tE6PjJ7LI%3D)

**2. 데이터 테이블을 만들어준다.**

데이터 테이블을 만들 때 CreatureData와 연동을 시켜준다.

여기에서 종(?)을 추가하고, 값을 입력해준다.

![](https://blog.kakaocdn.net/dna/cIxLu0/btsB1MXNsXJ/AAAAAAAAAAAAAAAAAAAAAFcYYoG4GF_VoZaRABBaskqfg6wIK6ZBucW87ZGqLNU-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=6UWkgkQaLRL5yVN1%2BxoTgCaJUPc%3D)

Creature들에게 공통으로 들어가는 것들을 만들어준다.

Hp, Damage, 애니메이션(paper flipbook)

![](https://blog.kakaocdn.net/dna/sYaUA/btsBVyNBLtH/AAAAAAAAAAAAAAAAAAAAAMaH6ci1LVpL0X_OgRmDT_WnBJcZqWV8HtAZpKLoPCjf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=D1H71vspSe7kYMDZUovLFtvNxpo%3D)

CreatureData를 DataTable에 연동시켜놨었기에, Add를 해주면 CreatureData들을 설정할 수 있는 새로운 종(?)을 얻을 수 있다.

![](https://blog.kakaocdn.net/dna/brZrWI/btsBY2gcfPe/AAAAAAAAAAAAAAAAAAAAAJLo1hEpF_pZK3RDCDJI5Un7WFyN5MZsietJGDwgEWXf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=13AK%2F8MP2MlgmvCpKDstmzUZsw0%3D)

이제 Data를 적용하고 싶은 종(?)의 BP로 돌아가서

Get Data Table을 하자

Data Table 산하의 함수와 Utilities산하의 함수가 있는데.

Utilities산하로 가야한다. Data Table 산하의 함수는 이름(종의 이름)만 출력할 뿐이다.

![](https://blog.kakaocdn.net/dna/ObLFj/btsBXQOaSBL/AAAAAAAAAAAAAAAAAAAAAM_vCcelFts2PqVrdlOGLnolsR4eFuejpydUYmHf3q4c/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=QihInvnfXJtH0AiKV69uYjJpaqI%3D)

DataTable 산하의 함수

![](https://blog.kakaocdn.net/dna/bvXIQF/btsB1upJqQa/AAAAAAAAAAAAAAAAAAAAANGj67SvB3mKiiigrj7ELytKgJVEVhYK3-85YNHrorxv/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=voFLexEeM2QCgA4OWP3UHXqukm0%3D)

이렇게 CreatureData 형 변수에 값을 넣어주면, 해당 종(?)의 값들을 얻을 수 있다.

![](https://blog.kakaocdn.net/dna/0TLHI/btsBUCbEjVg/AAAAAAAAAAAAAAAAAAAAAFG5XzCR72ygy47tsWr3LBQF5QqYsCQYX2BfrDZI24AD/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Vf92QQ8W6Bd%2B6%2FoMDGx3F%2BdLX1A%3D)