---
title: "[실습저장소]삼각형 using TableDescriptorHeap(DX12로 로딩중 로딩중..)"
date: 2024-10-25
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

![](https://blog.kakaocdn.net/dna/bDJhy8/btsKluBGhUC/AAAAAAAAAAAAAAAAAAAAAFwz8Z4Txaoer7Q_ZcmzE2tTsWYOEUKlYNmkE3S4Dv1R/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=QXizTLE5Ez7PIlLCm%2BvtbRfDGbY%3D)

![](https://blog.kakaocdn.net/dna/olAaa/btsKjHCOt7S/AAAAAAAAAAAAAAAAAAAAAOeAN8MVReac7p2AdjeqrOYI1PWLySxlxB6xkAYsWvzl/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=yCu%2Fgp9kDtX83Gw8kgCtwVFZpyI%3D)

그리과 아래의 글을 비교하면 될 것 같다.

흐름

1. GPU에 Data쓰고, index를 통해서 CPU Descriptor를 받아온다

2. 받아온 CPU Descriptor를 GPU Descriptor에 Copy한다.

3. Decriptor를 사용해서 Register에 값을 할당한다.

**GPU에 Data쓰고  CPU Descriptor 받아오기**

![](https://blog.kakaocdn.net/dna/bIFrCB/btsKkXRU6mv/AAAAAAAAAAAAAAAAAAAAAJ0zAiv72R6OXIKd6Q_bhCRIDWF6VqKtrC7R7DeTsTJu/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FcUua0gDD5hbEhR0ELcCu12fcoQ%3D)

GPU 공간에 Data를 할당하고

그리고 CPU의 Descriptor Handle 반환하기

**SetCBV(Set Constant Buffer View)**

![](https://blog.kakaocdn.net/dna/tqpao/btsKlcuvtro/AAAAAAAAAAAAAAAAAAAAANGDsrwOsottDYcZO50JNcHCPEacEvi-XlTHwaWRWX6F/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1guuwWbscJRyifFRRRK5T8eM4jw%3D)

받아온 CPU View(Descriptor)를 GPU에 View(Descriptor) 보내기 (Devie를 사용했음!)

**레지스터에 값 전달하기**

![](https://blog.kakaocdn.net/dna/LCNRW/btsKkhDo3Hm/AAAAAAAAAAAAAAAAAAAAAJAOdHwhQkNGJu0UpMPqQhrrMjw3rL7Iy6GVb8aNerWY/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FTegAw%2B3bexFFkYmBM%2FeWsfHQVs%3D)