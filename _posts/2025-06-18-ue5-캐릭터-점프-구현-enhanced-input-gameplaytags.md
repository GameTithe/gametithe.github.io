---
title: "[UE5] 캐릭터 점프 구현 ( Enhanced Input + GameplayTags)"
date: 2025-06-18
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

```
void AKnightHeroCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	KnightInputComponent->BindNativeInputAction(InputConfigDataAsset, KnightGameplayTags::InputTag_Jump, ETriggerEvent::Started, this,&ACharacter::Jump);
	KnightInputComponent->BindNativeInputAction(InputConfigDataAsset, KnightGameplayTags::InputTag_Jump, ETriggerEvent::Completed, this,&ACharacter::StopJumping);
}
```

캐릭터의 점프는 언리얼에서 구현을 해놓았습니다.

그래서 Input과 Action을 맵핑만 잘 시키면됩니다. 매핑에 대한 것은 다른 글에서 정리했으니, 따로 언급은 안하겠습니다.

Jump를 구현하면서 알게된 것도 아래에 정리해놓았습니다.

Complete는 스페이바에서 손을 떼면 호출이된다.

그럼 이론상 무한점프가 가능한거 아니가?

스페이바 떼면서 stopJumping이 호출되니까, 그다음에 누리면 바로 점프를 하겠네?

언리얼 코드를 보면서 알게된 것

1. resetJumpState를 할 때, Falling도 체크하기 때문에 땅에 닿아야 다시 점프가능

2. StopJumping 외에 Jumping Allowed라는 함수가 있는데 거기서도 똑같이 Falling을 동시에 체크하더라 + JumpCount까지 같이

```
void ACharacter::StopJumping()
{
	bPressedJump = false;
	ResetJumpState();
}
void ACharacter::ResetJumpState()
{
	bPressedJump = false;
	bWasJumping = false;
	JumpKeyHoldTime = 0.0f;
	JumpForceTimeRemaining = 0.0f;

	if (CharacterMovement && !CharacterMovement->IsFalling())
	{
		JumpCurrentCount = 0;
		JumpCurrentCountPreJump = 0;
	}
}

bool ACharacter::JumpIsAllowedInternal() const
{
	// Ensure that the CharacterMovement state is valid
	bool bJumpIsAllowed = CharacterMovement->CanAttemptJump();

	if (bJumpIsAllowed)
	{
		// Ensure JumpHoldTime and JumpCount are valid.
		if (!bWasJumping || GetJumpMaxHoldTime() <= 0.0f)
		{
			if (JumpCurrentCount == 0 && CharacterMovement->IsFalling())
			{
				bJumpIsAllowed = JumpCurrentCount + 1 < JumpMaxCount;
			}
			else
			{
				bJumpIsAllowed = JumpCurrentCount < JumpMaxCount;
			}
		}
		else
		{
			// Only consider JumpKeyHoldTime as long as:
			// A) The jump limit hasn't been met OR
			// B) The jump limit has been met AND we were already jumping
			const bool bJumpKeyHeld = (bPressedJump && JumpKeyHoldTime < GetJumpMaxHoldTime());
			bJumpIsAllowed = bJumpKeyHeld &&
				((JumpCurrentCount < JumpMaxCount) || (bWasJumping && JumpCurrentCount == JumpMaxCount));
		}
	}

	return bJumpIsAllowed;
}
```