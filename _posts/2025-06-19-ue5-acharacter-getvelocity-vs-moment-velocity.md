---
title: "[UE5] ACharacter->GetVelocity() VS Moment->Velocity"
date: 2025-06-19
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

```
	GroundSpeed = OwningCharacter->GetVelocity().Size2D();
	
	HasAcceleration = OwningCharacterMovement->GetCurrentAcceleration().SizeSquared2D();
```

**OwningCharacter->GetVelocity():** 현재 Actor의 이동 속도 **(물리 기반, 외부 힘 포함)**

**OwningCharacterMovement->Velocity:** MovementComponent가 계산한 내부 이동 속도 **(컨트롤 기반)**

만약 폭발에 의해서 캐릭터가 뒤로 날라가는 상황이라고 가정해보자

이때 

ACharacter-> GetVelocity(): 속도 있음 (Actor 실제 움직임)

MovementComponent->Velocity: 속도 없음 (컨트롤러는 이동 명령 안 내림)