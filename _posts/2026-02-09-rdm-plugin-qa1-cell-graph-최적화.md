---
title: "[RDM Plugin] QA1: Cell graph 최적화"
date: 2026-02-09
toc: true
categories:
  - "UE5_Plugins"
tags:
  - "UE5_Plugin"
---

Cell Structure가 들어온 이후 갑자기 frame drop이 심해졌다는 이슈 ( cell structure 만의 잘못은 아니였고, 여러 문제가 겹쳤었다. )

그래서 시작한 코드 분석 및 최적화

지금 구조상 총알을 한 발 당 1번의 boolean operation 연산이 아닌 batch로 총알들을 모아서 한 번에 처리해주고 있다.

하지만 disconnected cell 을 찾기위해 실행되고 있는 BFS는 총알 한발당 한번씩 돌고 있었다.

증거자료

![](https://blog.kakaocdn.net/dna/v5Amy/dJMcaaD3Q7e/AAAAAAAAAAAAAAAAAAAAAMj6MUShzp05Vm7A4daIygN3MBQBOijU-Oht4YbSsxfh/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ZjKjJ1ig%2BMIxIiHoEoQGAZrtITE%3D)

현재 구조는 아래와 같다.

파괴 요청이 들어오면 Enqueue를 해놓았다가, TickComp에서 한 틱마다 Flush를 해준다.

![](https://blog.kakaocdn.net/dna/byvJUD/dJMcaaKPMEd/AAAAAAAAAAAAAAAAAAAAAO_9n60BYqZHqBQlcDmzzUJ1uPXpBI-V3WMjIJQzcjgl/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=zX6%2BIkE8m4g%2FZPIodCGhDvyiPlQ%3D)

지금 UpdateCellStateFromDestruction이 FlushServerBatch에서도 호출되고 있다.

![](https://blog.kakaocdn.net/dna/bOIA3W/dJMcafSVhz1/AAAAAAAAAAAAAAAAAAAAAKrMkPUxLE-tu-JY7baXnV0WS2Qhvvj7Nou0FDPyQT89/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=k01fvjdipG5pmkkaRljOBbAj6uw%3D)

최종 로그

![](https://blog.kakaocdn.net/dna/wi9zB/dJMcaiB3nYn/AAAAAAAAAAAAAAAAAAAAAALCAmS_rU4cqr2EDOQxywEUzC8J8GpyWcZxXZPZSV6J/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Pa%2B0v%2B2i6b52K2Vr0DBllfsbgFA%3D)

#### before: N개 요청 => BFS N번 after: N개 요청 => BFS 1번

최적화 전



최적화 후



![](https://blog.kakaocdn.net/dna/ufOQs/dJMcacWaNxi/AAAAAAAAAAAAAAAAAAAAAERR34vF1HiHjxRw6b6kyuX8YigtiDkWO6HTSpHdgEAb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1osXhRdJ8k8NlBFuQG%2B815Yf%2Bjw%3D)