---
title: "[언리얼5/ UE5] 첫 최적화... (Easy hook system 에셋)"
date: 2024-12-30
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

요로코롬 이쁜 에셋인데, 최적화가 필요하다고 하여서 처음 최적화를 시도해보았습니다.



에셋을 뒤적 뒤적하다보니,   
아래와 같은  Collapsed Graph를 발견했는데, 여기서 GetComponentByClass를 많이 사용하고 있었습니다.

![](https://blog.kakaocdn.net/dna/GokBe/btsLAAIBRu8/AAAAAAAAAAAAAAAAAAAAAOp_ylwqWY5yw-pco8iw5QQau1z44NaP9X2VeP9Q501a/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ZPDRWBVmMUdX63ucQr9%2B8ZIqbFg%3D)![](https://blog.kakaocdn.net/dna/y6zKC/btsLAw7g1iR/AAAAAAAAAAAAAAAAAAAAAMcJWYlm0RScjCB53lcqPr_zx2MjLnHvR_p6gCKsuts1/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=pGS3UNtfE3dwxU6As12%2BSBca3a4%3D)

이 함수는 전체 component를 확인하는 함수로, 성능에 안좋다고 알고 있기에

get component by class 함수가 한 번 호출되서 해당 class를 찾으면 저장할 수 있도록 코드를 수정했습니다.

![](https://blog.kakaocdn.net/dna/BkloL/btsLC2Q4PXd/AAAAAAAAAAAAAAAAAAAAAM8Lp8i4omnZXifZmH8PStCeYUvnj6n7KbsO9ODneZtU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=vFIoax78YItnp6vin6gxAk3rDTo%3D)

Insight를 사용해서 확인한 결과 2ms이 줄었습니다...! 미묘한 차이겠지만 뿌듯합니다..!

( 그래플링 훅 5번 사용했을 때 입니다)

![](https://blog.kakaocdn.net/dna/WufwJ/btsLA857xPR/AAAAAAAAAAAAAAAAAAAAANhYg9B7uiRQKlEMnru3KGHuvRAL9CU5TX9IX0WbCAfk/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=i5Pf7mXbnoJYzWV4QF%2FCjHbvMLk%3D)
![](https://blog.kakaocdn.net/dna/pHuHa/btsLBljSuu2/AAAAAAAAAAAAAAAAAAAAAKlcDk1oCtCPZa3HbQ8sTrYYjN85PtT_ERSZek_T4Tep/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1ByMK9DKofb%2F9Kc3n9kM69kfCS8%3D)