---
title: "[RDM Plugin] MVP 제작 및 Test Scene 제작"
date: 2026-02-09
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

총알이 여러발 피격되서 부하를 생기는 상황을 만들기 위해서 총을 여러 개 생성할 수 있도록 테스트 환경을 구축했다.

![](https://blog.kakaocdn.net/dna/ExveY/dJMcagYnBEq/AAAAAAAAAAAAAAAAAAAAAAsZSDO7iQgppGXGuNCHFcWoNjTZPAn8TudElcAInxFM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=c%2Fx1M2fPTbq086SaaQl4M55nc48%3D)

Test Scene 생성 완료!

Frame Drop은 예상 범주...! 이것을 줄이는게 궁극적인 목표이기 때문!

![](https://blog.kakaocdn.net/dna/bJmVmA/dJMcaiPomie/AAAAAAAAAAAAAAAAAAAAAJY-3lUNyy3PIEi_tjw-z5y86CQA57x6MQggRfwYIO1m/img.gif?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=uv%2BbEKZcJbnUJYN8lgceApiOrdQ%3D)

Trouble Shooting

1. 총을 생성하면 무조건 손으로 생성됨

아래 처럼 총의 Beginplay에서 총(Mesh)을 캐릭터의 손으로 위치를 변경시킨다.

```
void AShooterWeapon::BeginPlay()
{
	Super::BeginPlay();
    
    	// .... 

	// attach the meshes to the owner
	WeaponOwner->AttachWeaponMeshes(this);
}
```

총의 구조를 보면 이렇게 FirstPerson, ThirdPerson Mesh가 존재하고,  
FirstPerson, ThirdPerson Mesh 의 Socket에 부착되게 된다.

![](https://blog.kakaocdn.net/dna/2pHCt/dJMb99Zf1Ze/AAAAAAAAAAAAAAAAAAAAAPYpsjEaF3UNn1ZNtoIh9ZtS4myS5uEnWCDhkYOOijhf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ao6yDLEWwIWYPGtzRS6eJtEi6PM%3D)

처음에는 이렇게 총의 위치를 원복시키려고 했지만 실패

```
NewWeapon->SetActorRelativeLocation(LocationOffset);
```

그 이유는 총의 메쉬들은 이미 ShooterWeapon\_Rifle에 없기 때문이다.

그래서 아래와 같이 총의 First, Third Person Mesh에 직접 접근해서 위치를 옮겨 주었다.

```
// 손으로 가있던 총의 Mesh들을 원래 위치로 원복
if (USkeletalMeshComponent* FPMesh = NewWeapon->GetFirstPersonMesh())
{
        FPMesh->AttachToComponent(NewWeapon->GetRootComponent(), AttachRule); 
}

if (USkeletalMeshComponent* TPMesh = NewWeapon->GetThirdPersonMesh())
{
        TPMesh->AttachToComponent(NewWeapon->GetRootComponent(), AttachRule); 
}
```

![](https://blog.kakaocdn.net/dna/ExveY/dJMcagYnBEq/AAAAAAAAAAAAAAAAAAAAAAsZSDO7iQgppGXGuNCHFcWoNjTZPAn8TudElcAInxFM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=c%2Fx1M2fPTbq086SaaQl4M55nc48%3D)