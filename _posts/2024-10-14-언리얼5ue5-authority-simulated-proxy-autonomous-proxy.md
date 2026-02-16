---
title: "[언리얼5/UE5] Authority, Simulated Proxy, Autonomous Proxy"
date: 2024-10-14
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

멀티플레이어 게임을 만들다가 중간 중간 헷갈리니 정리를 해놓자!  
  
Controller은 simulated proxy에서 유효하지 않는다!  에서 시작된 정리...

### 1. **Authority**

* **Authority**는 오브젝트를 제어하는 주체를 의미한다. 서버가 Authority를 가지고 있다.
* **서버**는 오브젝트들을 관리한다. **클라이언트**는 **서버로부터 오브젝트의 상태를 받아** 업데이트합니다. (서버에서 처리해서 뿌려주는 느낌이다.)
* ex) 클라 -> 서버 : 나 총 쏠게                                                                                                                                                                 서버->클라: 총 쏴

![](https://blog.kakaocdn.net/dna/bC2Pyf/btsJ2tYM6nd/AAAAAAAAAAAAAAAAAAAAAO_n6WwGigKmrCl2M_dF3pdj04BeWbrjDH1ybLmidI1r/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=YY%2Bnsmf2sKk7p9P5AWzvaQXxkmI%3D)

### 2. **Simulated Proxy**

* 클라이언트에서 서버가 제어하는 오브젝트를 나타내는 상태이다.
* 클라이언트가 직접 조작하지 않는 다른 플레이어나 환경 오브젝트들이 이에 해당한다.
* ex. 다른 클라이언트를 Simulated Proxy로 그 캐릭터를 표현하고 서버에서 받은 정보로 상태를 업데이트 한다.

![](https://blog.kakaocdn.net/dna/ccbVVe/btsJ2cbUSpS/AAAAAAAAAAAAAAAAAAAAADBvGC5Z7AFljxo4DGGrBIRtz9MdpcurEfKcvDkL8yuI/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=LLmMD3e2GTeGYqhX4MdNFbH8Tj4%3D)

### 3. **Autonomous Proxy**

* **플레이어가 제어하는 캐릭터**가 이에 해당합니다.
* 클라이언트가 **서버에게 자신의 정보를 전송**하고, **서버는** 그 정보를 확인한 후 **동기화**하여 **다른 클라이언트에도 반영**한다.
* ex![](https://blog.kakaocdn.net/dna/ccbVVe/btsJ2cbUSpS/AAAAAAAAAAAAAAAAAAAAADBvGC5Z7AFljxo4DGGrBIRtz9MdpcurEfKcvDkL8yuI/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=LLmMD3e2GTeGYqhX4MdNFbH8Tj4%3D)