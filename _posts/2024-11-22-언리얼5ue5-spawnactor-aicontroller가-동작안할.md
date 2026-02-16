---
title: "[언리얼5/UE5] SpawnActor, AIController가 동작안할"
date: 2024-11-22
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

이게 진짜 이상한게 몬스터의 AIController있고, AIController가 Player를 향해 가도록 도와준다.

근데 어느순간 부터 나를 찾기는 했는지, 나를 바라보지만, 공중에서만 걷고있다. (애니메이션만 실행)

Controller관련해서 C++ 을 계속 디버깅했다. (로그 출력, breakpoint)  
AIController도 잘 할당되었다.

심지어 MoveToTarget함수까지 잘 들어오고

MoveToActor도 breakpoint로 잘 동작하고 있음을 확인했다...

![](https://blog.kakaocdn.net/dna/dgde5C/btsKSnoUlps/AAAAAAAAAAAAAAAAAAAAAOmhJTwKTtcsZ3DIswzn1nDyQBa5m9T_4ob9G-bVPA9U/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=M8QCPxeOOZXfG2V1ZUuKTdjTMwU%3D)

원인은 Monster의 Collision Preset을 PhysicsActor에서 Pawnd으로 바꿔주니,,,잘 실행되었다...

구글링해도 비슷한 내용이 없다..

추측하건데, spawnActor할 때 Controller를 따로 붙혀줘야되는 것처럼, Actor 되어있으니 잘 되었나 싶다..  
  
Collision Preset을 건드렸던 기억과,C++에서는 절~대 문제가 없다는 증거(?)로

겨우 겨우 해결했다... 누군가에겐 도움이 되었으면 좋겠다

![](https://blog.kakaocdn.net/dna/wUa5g/btsKS2YHc4u/AAAAAAAAAAAAAAAAAAAAANhIzHb-YkZycheWOvp5zs8k3v-0MdCAJ3XZZ5p0rB2L/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=mXtUaBFz5EsfHFW7ZStm6XPmAuc%3D)
![](https://blog.kakaocdn.net/dna/rWHnL/btsKREdEJaZ/AAAAAAAAAAAAAAAAAAAAAH0GglKW40rkZZw23fJl_pr1kHW3k3XmNriK0Pyqa_Vp/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=VaHQT5kMsbsjTxOq9cF%2FHzmp2pI%3D)

이건 SpawnActor 관련해서 저번에 적은 글이다.

<https://tithingbygame.tistory.com/98>

[[언리얼5/UE5] SpawnActor사용시 주의 (안움직임)

이렇게 하면 Monster는 잘 생성된다.FActorSpawnParameters params;ASMonster\* Monster = GetWorld()->SpawnActor(m.Key , location, GetActorRotation(), params); 근데 스크린 샷 처럼 공중에서 내려오질 않는다. 중력도 받지 않는

tithingbygame.tistory.com](https://tithingbygame.tistory.com/98)