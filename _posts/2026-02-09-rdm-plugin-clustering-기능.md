---
title: "[RDM Plugin] Clustering 기능"
date: 2026-02-09
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

Union Find 알고리즘을 사용해서 clustering 을 구현했다.

일정 시간 내, 일정 범위 내에 총알이 빗받칠 경우 그 범위를 아우르는 구멍을 뚫어주는 기능이다.

이 기능이 필요하다고 생각한 이유는

총알이 한 곳에 집중 포화가 된다고 가정하면, 그 순간 많은 구멍이 생길 것이고 그로인해 많은 vertex들이 생기게 될 것이다.

이 상황을 방지하고자, 큰 범위로 Clustering해서 구멍을 뚫어주는 기능을 추가했다.

( 큰 범위가 관통처리 된다면, Subtract 연산 비용 감소 + vertex 수 감소 + 효과시각적인 효과까지 많은 이득을 가져다 줄 것이라고 판단했다.)

클라이언트-서버 동기화를 위해서

Clustering 자체는 서버에서 실행되고, 그 결과값을 클라이언트한테 muli cast를 해준다.

아래 이미지에서 Clustering이 잘 되는 것을 확인할 수 있는 이유는   
(모든 총알 구멍의 크기는 동일하다, 근데 큰 구멍 몇개를 확인할 수 있을 것이다. 그 부분이 clustering된 구멍이다.

tistory에서 영상 지원을 중단한다고 추후에 유튜브에 올리고 링크를 달겠습니다.)

클라이언트-서버 간 동기화

![](https://blog.kakaocdn.net/dna/UnCzw/dJMcahDaJDk/AAAAAAAAAAAAAAAAAAAAAMq_-63_tf4gtXTpH1Xx_2bYhmClKL2IDeXTWnAu4LZU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nMbT60BmOEww0cbC2yI2n1LuZ3Q%3D)
![](https://blog.kakaocdn.net/dna/v81zX/dJMcaaqwVJ1/AAAAAAAAAAAAAAAAAAAAAPGuPRpmL-0nSXp1EqqFDK2Zauyak_J5OQJJKJzpYX8q/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=LZUfA7owqUjPDek8DJFSJpz0nTY%3D)
![](https://blog.kakaocdn.net/dna/TyZGb/dJMcafejPTS/AAAAAAAAAAAAAAAAAAAAACCoQ4GdLjdizcPry9ySVJNL2kpmg47OUECRuXf_vDJL/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nKAJ3JvdMX0tXmBHX2jeQFivd6Y%3D)

이후 QA과정중에서

Clustering에서 병목이 생기는 것 같다는 문의가 들어왔다.

언리얼 인사이트로 프로파일링을 해봤다.

1. 시간이 많이 잡히는 부분은 Boolean Subtract하는 부분이다. (구멍 뚫는 부분)

=> 필연적 시간

![](https://blog.kakaocdn.net/dna/RjLfG/dJMcag5mSYg/AAAAAAAAAAAAAAAAAAAAAP13FLBWrxA65KM8rMx3px0OpXs5jtKqlWQdC9IoURFG/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=OAMVeD0QDuQxLcNGyawlfL9za10%3D)

2. Union-Find는 나노세컨드 밖에 시간을 쓰지 않는다.

=> Clustering 수집은 병목이 아니라는 결론이 나왔다.

![](https://blog.kakaocdn.net/dna/d89i2Z/dJMcajubZMw/AAAAAAAAAAAAAAAAAAAAANE0Nr8_Kahi0hH7ZmlavodQqyt3dZmp-fKKxeDqzL9L/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=uTdn9MDRgVdLYda3eOx%2BbffkUj4%3D)