---
title: "[실습저장소] PBR (Physically Based Rendering)"
date: 2025-05-09
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

정리한 논문:

<https://tithingbygame.tistory.com/32>

[[논문]Physically Based Shading at Disney

논문을 읽고, 아는 내용과 섞어서 나중에 기억을 상기하기 위해 정리한 글입니다. 공부하면서 정리하다보니 오류가 있을 수 있습니다. 오류를 발견하면 댓글로 공유 부탁드려요!  (아래에 세

tithingbygame.tistory.com](https://tithingbygame.tistory.com/32)

Specular BRDF의 각 요소를 적용시킨 모습입니다.  
Specular G

![](https://blog.kakaocdn.net/dna/AUUBt/btsOvKuKeDr/AAAAAAAAAAAAAAAAAAAAAM6LuWZgYEUigeLB3HbR6gcgpeZi5GFQDAAOyJRpoa7O/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Ak821znhSBGI2d9afgq9aZIC8mA%3D)

Specular N

![](https://blog.kakaocdn.net/dna/1jZS9/btsOuYts7ZJ/AAAAAAAAAAAAAAAAAAAAAKvY6KQGaGTVlY1C6J2vrLU6hpZli484HDwfWOy9amm6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Gga06ALYyd9stYVzfxBDjfS6%2FVY%3D)

Specular F

![](https://blog.kakaocdn.net/dna/uI2Rd/btsOv5dY4So/AAAAAAAAAAAAAAAAAAAAAB1VyOPXOSE_hHhYHWSR8b1Utt9W2POQ-x7tGOTAUwD7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=FZ4AmEdOQ0U3ifFuHP2effYs93A%3D)

 IBL method로 Ambient Light를 구현해줬습니다.



두 term을 합치고, albedo, normal, ao texture를 입혀서 PBR을 구현했습니다.