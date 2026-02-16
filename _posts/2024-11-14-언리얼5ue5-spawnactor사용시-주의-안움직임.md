---
title: "[언리얼5/UE5] SpawnActor사용시 주의 (안움직임)"
date: 2024-11-14
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

이렇게 하면 Monster는 잘 생성된다.

```
FActorSpawnParameters params;
ASMonster* Monster = GetWorld()->SpawnActor<ASMonster>(m.Key , location, GetActorRotation(), params);
```

근데 스크린 샷 처럼 공중에서 내려오질 않는다. 중력도 받지 않는다.

Tick에 들어가지 않는건가? MovementComponent가 없는건가? 모든 것을 체크해봤지만 이미 존재했다.

답은 Controller가 없다는 것이다.

```
FActorSpawnParameters params;
ASMonster* Monster = GetWorld()->SpawnActor<ASMonster>(m.Key , location, GetActorRotation(), params);
Monster->SpawnDefaultController();
```

이렇게 DefaultController를 만들어주면 정상적으로 움직인다...  
  
버그를 해결하는데 오랜시간이 걸렸지만, 굉장히 단순한 문제였고,,,  
덕분에 까먹지 못할 것 같다...!

#### 

#### **디버깅과정**

**Tick이 잘 호출되는 지, Forward 크기가 1로 잘 출력되는 지는 다 확인했다.**

**그래서 AddMovementInput이 실행되지 않는 것이라고 추측했고, 디버깅을 해봤다.**

![](https://blog.kakaocdn.net/dna/oY7jf/btsKHHO6YyF/AAAAAAAAAAAAAAAAAAAAAK1f4jqxQdTfV-W8nr_11ezVa3ji5fW-jY17s5_vMTl3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=tLlLiGR6ogUJyOJD2PrNh19LPsM%3D)

축축 따라가다보면 이상한 점이있다.

![](https://blog.kakaocdn.net/dna/G6ags/btsKHN2HFBG/AAAAAAAAAAAAAAAAAAAAAB5qpA-CfzjWLa7PUuQ1fEpK1ReFLEqb7UktwixqqAmI/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3Mjtx%2FYenXiObV5Y8qp9Rap45L0%3D)

여가서 IsMoveInputIgnored()라고 있는데 이 함수에서 Controller를 체크해주는 것이다.

그래서 초반에는 여기도 잘 실행되고 있구나 하고 넘어갔다. (if문도 다 통과함)

근데 이게 웬걸 Controller는 존재하지않았고, IsMoveInputIgnored 앞에 not 연산자 때문에 If문에 들어가는 것이었다...

쩝... 다들 이 블로그를 보고 빠르게 해결했으면 좋겠다!

![](https://blog.kakaocdn.net/dna/cIFJdh/btsKHq1b5SE/AAAAAAAAAAAAAAAAAAAAAOsqncsFVG-HDbvVGE6dO866vXNTRdrS-UNs8Y16sx5u/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=29meuCmZuC6otwlHHZVKONZf4vY%3D)
![](https://blog.kakaocdn.net/dna/nItap/btsKG8GpCnz/AAAAAAAAAAAAAAAAAAAAAO3Na5n-ytqGv5ComLommqbeSDUdyMB1yjXYUTw30_q4/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=VspaQLB5HN00lyN%2BW1O%2FpVZKG5Y%3D)
![](https://blog.kakaocdn.net/dna/NJXVq/btsKGMjhq5O/AAAAAAAAAAAAAAAAAAAAADkrxm5JANpwO2Wq3SbTeGuVESjZTsktu0O_lTJM_583/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=dsxvEMWyO3NHRaI7fUgwAixt6P4%3D)