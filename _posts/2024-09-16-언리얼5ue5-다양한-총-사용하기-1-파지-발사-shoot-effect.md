---
title: "[언리얼5/UE5] 다양한 총 사용하기 - 1 (파지, 발사 shoot effect)"
date: 2024-09-16
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

![](https://blog.kakaocdn.net/dna/dOh1Xj/btsJFqTSCqt/AAAAAAAAAAAAAAAAAAAAAKo3iok3jF6SQzuhkUPWdfJcDk3MJWNporcgPKAur36y/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=u035ecJOSaLFublKzZ%2FBKmZnGwM%3D)

모델의 skeleton mesh를 보면 weapon\_r에 무기가 존재하는 것을 볼 수 있다.

우리는 다양한 종류의 무기를 파지하기 원한다.

그럼 weapon\_r 위치에 여러가지 총을 두면 해결된다.

WeaponSocket을 weapon\_r 자리에 만들어보자. ( 우클릭 -> Add Socket )

캐릭터.h / 캐릭터.cpp

![](https://blog.kakaocdn.net/dna/bJuCIB/btsJDSYotQN/AAAAAAAAAAAAAAAAAAAAAIsSpSdfwjE_iJMnG1aIbf39Kzn36Zl41s3rv2sLa20K/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=0KuVOONJaOfdkKLEzEiC7SGrkKA%3D)
![](https://blog.kakaocdn.net/dna/K1Z83/btsJEThL4tx/AAAAAAAAAAAAAAAAAAAAACw9005lIaloAoXteJ33imK_RjGrwr-yr8Zl72TvJgqj/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=zNfAs5sEIE6m8DNakPIRVtpFFHE%3D)

C++로 하면 간단하다.

TSubclassOf <AGun> :여러가지 총을 받기 위함

AGun \* : 실제 총 인스턴스

* **KeepRelativeTransform**: 자식의 상대적 트랜스폼을 유지
* **KeepWorldTransform**: 자식의 월드 트랜스폼을 유지
* **SnapToTargetIncludingScale**: 부모와 트랜스폼(위치, 회전, 스케일) 모두 동일하게 맞춤
* **SnapToTargetNotIncludingScale**: 부모의 위치, 회전은 맞추고, 스케일은 유지

* **SetOwner**: 액터-액터 관계
* **SetupAttachment**: 컴포넌트-컴포넌트 관계

![](https://blog.kakaocdn.net/dna/Urinq/btsJEpH8JjO/AAAAAAAAAAAAAAAAAAAAAJY3m_NXq3xviyjTxKIbBrCLRi-qSoOpFeMslTcFUvz1/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=d87rsVBUak47SXmBNbHau8sSDXs%3D)

총.h / 총.cpp

![](https://blog.kakaocdn.net/dna/cQo8yS/btsJDgyV2eW/AAAAAAAAAAAAAAAAAAAAALiZZG3EQLetCcycOtafLYZOmhvQLgq53hRySecfKk2E/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=h%2F68MjWwVwYLQ8Ukc7YvEOiPe5A%3D)

(Mesh = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("Mesh"));  로 설정하고 BP에서 Mesh를 할당했다.)  
  
  
MuzzleFlashSocket은 총의 SkeletalMesh에 들어가면 총구에 Socket이 하나있다.

총을 잡고 있을 때 사용한 원리와 동일!

![](https://blog.kakaocdn.net/dna/kyhM5/btsJDfUlm53/AAAAAAAAAAAAAAAAAAAAALwU6_adI8Nn4cVCX4pNF16iDxsd-3V1DE6m6rKwqjUN/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=FgvffJOCGjyoSNdnIYsIaGEwFr4%3D)
![](https://blog.kakaocdn.net/dna/oGMAo/btsJETIREJa/AAAAAAAAAAAAAAAAAAAAALwRXuU2wB4iCi6PqAvk26UL21-5-brY7x_xeho50SVW/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=BCHS8idVEzaeCjVylDBJ8ymTb%2BQ%3D)
![](https://blog.kakaocdn.net/dna/uf1kW/btsJDipZQqg/AAAAAAAAAAAAAAAAAAAAALKktnvVh-QfXWpfB1Tkxzr7MJgMojpMH90N9h1CDmh4/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9rWf3T%2BrVCtzT1U2XaxpuIZ2yco%3D)

Blueprint에서 particleSystem만 설정해주면 준비완료

헤맸던 포인트

총 쏘는 것을 어디서 실행시키지?

1. Gun 의 Blueprint에서 LeftMouseButton을 실행시키자

=> 왜인지 실해이 안됌

2. Gun의 C++ 왼클릭 input을 mapping하자

->SetupPlayerInputComponent 함수가 없음

결론

아 Gun은 Actor니까 입력을 안받는구나

캐릭터에서 입력을 받고 Gun에 있는 함수를 실행시켜야겠구나

![](https://blog.kakaocdn.net/dna/Z7N6s/btsJCXzEhZ4/AAAAAAAAAAAAAAAAAAAAADjAgFgdoTaIgQfoW6SJSDLu8ZfIthFJv5c520-9PAkn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=HEn94o7egNLo4J26%2FAOUpalMZaI%3D)

![](https://blog.kakaocdn.net/dna/cDizi9/btsJCX7sx56/AAAAAAAAAAAAAAAAAAAAAGFf7spMNHAbP-K3CcAmtlQCj_B2cZ7uFrkP6eb4nPtV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GelK0blqAY2tbr%2BMmcMyvl5xo%2BE%3D)