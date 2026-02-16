---
title: "[언리얼5/UE5] Setup Spawn Ability (능력 스폰 설정)"
date: 2024-11-16
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

![](https://blog.kakaocdn.net/dna/c35X1I/btsKIbbyBbu/AAAAAAAAAAAAAAAAAAAAAMn2juBTRWNpmGMa3fgzIzD8a1-sgvCMxhxj_Jw94edn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=sA985ue4VE7kmND4P5S%2FFE8HuNo%3D)

이렇게 GameplayAbiliy.h에 들어가면 Given과 End 함수를 찾을 수 있다.

이 함수들을 override하자

![](https://blog.kakaocdn.net/dna/bAiqku/btsKI5aoBEi/AAAAAAAAAAAAAAAAAAAAAMyoNR1dg8-2nPWdTXHQ7HpKEXzOsI9VyxfCebgg_M4p/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9dxTSLbgd4LuqanWz6uUEf2mq3U%3D)

GameplayAbility.h

```
UENUM(BlueprintType)
enum class EWarriorAbilityActivationPolicy : uint8
{
	OnTriggered,
	OnGiven,
};

/**
 * 
 */
UCLASS()
class WARRIOR_API UWarriorGameplayAbility : public UGameplayAbility
{
	GENERATED_BODY()

protected:
	//~ Begin Ability Interface
	virtual void OnGiveAbility(const FGameplayAbilityActorInfo* ActorInfo, const FGameplayAbilitySpec& Spec) override;
	virtual void EndAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo, const FGameplayAbilityActivationInfo ActivationInfo, bool bReplicateEndAbility, bool bWasCancelled) override;
	//~ End Ability Interface

	UPROPERTY(EditAnywhere, Category = "WarriorAbility")
	EWarriorAbilityActivationPolicy AbilityActivationPolicy = EWarriorAbilityActivationPolicy::OnTriggered;

};
```

ENum Class로 사용해서, 알맞은 정책을 선택해준다.

GameplayAbility.cpp

```
void UWarriorGameplayAbility::OnGiveAbility(const FGameplayAbilityActorInfo* ActorInfo, const FGameplayAbilitySpec& Spec)
{
	Super::OnGiveAbility(ActorInfo, Spec);

	if (AbilityActivationPolicy == EWarriorAbilityActivationPolicy::OnGiven)
	{ 
		if (ActorInfo && !Spec.IsActive())
		{
			ActorInfo->AbilitySystemComponent->TryActivateAbility(Spec.Handle);
		}
	}
}

void UWarriorGameplayAbility::EndAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo, const FGameplayAbilityActivationInfo ActivationInfo, bool bReplicateEndAbility, bool bWasCancelled)
{
	Super::EndAbility(Handle, ActorInfo, ActivationInfo, bReplicateEndAbility, bWasCancelled);
	
	if (AbilityActivationPolicy == EWarriorAbilityActivationPolicy::OnGiven)
	{
		if (ActorInfo)
		{
			ActorInfo->AbilitySystemComponent->ClearAbility(Handle);
		}
	}
}
```

이렇게 OnGiven인지 정책을 먼저 확인하다.

맞으면 Ability를 활성화 시켜준다.

OnGiven에 대한 것이니, 끝날 때 능력을 Clear해준다.

이렇게 하면 알고리즘은 다 짠것이고,BP로 만들어주자

![](https://blog.kakaocdn.net/dna/dFTcaK/btsKIyYuhYS/AAAAAAAAAAAAAAAAAAAAAEAdIizxqD7e3MxDxDHCWF4TNz1QdYwGVj_SoPU1bt_L/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ar6IE1XN8gqgktIBvIL8qT1vDao%3D)![](https://blog.kakaocdn.net/dna/lbHoF/btsKI4iiqsZ/AAAAAAAAAAAAAAAAAAAAAKqPHkvqeIUVVATzrCBxMg8eWEIUJtEr2_jiYGJOImDo/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=49OC3uR2s%2FDGnllGr6U3jqRSqdg%3D)

![](https://blog.kakaocdn.net/dna/bF2NND/btsKIcVL0AF/AAAAAAAAAAAAAAAAAAAAAFYGMhLl-xrEXqxJ-mk1JW_RSZU128gHYc_tHsDrD7Rg/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9sDmc9Hwtjy96R%2FSX3pkc91sT7w%3D)

이렇게 해주면 무기 생성을 위한 기본적인 셋팅은 끝이다.