---
title: "[UE5] 캐릭터 이동 ( Enhanced Input + GameplayTags)"
date: 2025-06-18
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

오늘 하게 될 것... !



전체 과정 요약:

1.  SetupPlayerInputComponent에서 input action 을 매핑할 준비

2. Sunsystem에 DefaultMappingContext연결

이게 Default Mapping Context입니다.

![](https://blog.kakaocdn.net/dna/vwWoE/btsOGm0lrGn/AAAAAAAAAAAAAAAAAAAAAPznMEt_IL8xR91_BfzltC5SRRaUGHw5HtTEP2a46JTw/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=t92iZebFViswcJxOSyG42BrrK0Y%3D)

3. BindNativeInputAction 함수를 사용해서

Tag에 맞는 어떤 Input이 들어오면, 바인딩한 Action 함수를 호출한다,

**이제 시작해보자**

<https://tithingbygame.tistory.com/204>

[[UE5] NativeGameplayTag ( 코드단에서 설정 )

// Fill out your copyright notice in the Description page of Project Settings.#pragma once#include "NativeGameplayTags.h"namespace KnightGameplayTags{ /\*Input Tags\*/ KNIGHT\_API UE\_DECLARE\_GAMEPLAY\_TAG\_EXTERN(InputTag\_Move) KNIGHT\_API UE\_DECLARE\_GAMEPLAY\_TA

tithingbygame.tistory.com](https://tithingbygame.tistory.com/204)

이거보고 태그까지 잘 설정했다고 생각하고 진행하겠숩니다.

DataAsset을 상속받은 C++ class를 하나 만들자

![](https://blog.kakaocdn.net/dna/vTvMe/btsODpJtUil/AAAAAAAAAAAAAAAAAAAAAMEocEajfZPA6NOtJKKP5wkBbSFHbM6zyxHNiB0gX1YU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=SDEiAOelqkR4vK%2BK5jd8R15%2Fy9k%3D)

그리고 InputAction 구조체를 하나 만들자.

이건 tag와 action을 mapping 시켜주기 위한 구조체이기에, Tag와 InputAction을 포함하고 있다.

```
USTRUCT(BlueprintType)
struct FKnightInputActionConfig
{
	GENERATED_BODY()
public:
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, meta = (Categories = "InputTag"))
	FGameplayTag InputTag;
	 
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly) 
	UInputAction* InputAction; 
};
```

meta = (Categories = "InputTag")의 의미는 우리가 가지고 있는 Tags 중에서 InputTag 산하에 있는 Tags만 보겠다는 의미이다.

meta = (Categories = "InputTag")를 지우고 실행시키면 이렇게 InputTag가 아닌 Tags들도 같이 보여준다.

위에 처럼 class를 작성하면 editor에서 이렇게 볼 수 있다.

![](https://blog.kakaocdn.net/dna/0XVBx/btsOBDoCHqn/AAAAAAAAAAAAAAAAAAAAAFHFEbGsKmSD61NrAQh2TqgujEbBNfKR_gaMGSQButAO/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=iVxYTNxpFyJNVjAciNd58UHVzZc%3D)

( InputAction을 컴파일하기 위해서는 Build.cs에 EnhancedInput 모듈을 추가해줘야된다. 이전 글에서 했던것과 동일)

이 코드는 당장에 쓸 것은 아니지만, 나중에 tag를 사용해서 input action을 찾을 때 유용하게 사용될 것이다. 미리 만들어 놓자

(UDataAsset\_InputConfig에 만들면 된다.)

```
UInputAction* UDataAsset_InputConfig::FindNativeInputActionByTag(const FGameplayTag& InputTag) const
{	
	for (const FKnightInputActionConfig InputActionConfig : NativeInputActions)
	{
		if (InputActionConfig.InputTag == InputTag && InputActionConfig.InputAction)
		{
			return InputActionConfig.InputAction;
		}
	}
	return nullptr;
}
```

```
UCLASS()
class KNIGHT_API UDataAsset_InputConfig : public UDataAsset
{
	GENERATED_BODY()

public : 
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly)
	UInputMappingContext* DefaultMappingContext;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly)
	TArray<FKnightInputActionConfig> NativeInputActions;
	  
};
```

UInputMappingContext는 우리의 입력 시스템과 Action을 맵핑시켜주는 내장 시스템이라고 알고 있으면된다.

그리고 위에서 만든 구조체를 배열로 받아주자.

이렇게 세팅을 하고 DataAsset을 C++ Class를 상속받아서 만들면 아래처럼 세팅해줄 수 있다.

![](https://blog.kakaocdn.net/dna/cOxF4l/btsOBCXzQXp/AAAAAAAAAAAAAAAAAAAAANBtJB-CXh9MuWjwp9Cea-8-5RhqVLNlyaIRYbzgvULX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=4bDKwLMG8nyLdas0MA561tBxVcw%3D)

UInputMappingContext도 기본 제공해주는 것을 사용하고

InputAction또한 만들어진 것을 사용하면된다.

![](https://blog.kakaocdn.net/dna/J6nHT/btsOBFNwJr6/AAAAAAAAAAAAAAAAAAAAAIpfy-Yg4gB2hqymft28Jez_1Pt56HK9KD_-jKB8MZgH/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=a7lCLK1wi2IOdkkckejW7KbQcOs%3D)

모두 ThirdPerson 패키지에 존재한다.

![](https://blog.kakaocdn.net/dna/clg1xy/btsOA7jA3MJ/AAAAAAAAAAAAAAAAAAAAAIYxmZAsA_wXT6QDQLRESs4eT1pR6h6z8n2YkFTqIqr6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fR%2BqryACOwxFj5DZhm2uzI82HY4%3D)

### Make Function For Bind Action

EnhancedInputComponent를 상속 받은 C++ Class에서 시작하자.

![](https://blog.kakaocdn.net/dna/b1BByO/btsOA2W7Qzc/AAAAAAAAAAAAAAAAAAAAACITKWougqq2Njou0yvYj53l_MsojKJl0aC8-hiUdP45/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=L5eoVz1utiCA1UW92b6WpnlzJJI%3D)

BindAction을 하기 위해서 아래와 같은 함수를 호출해야된다.

우리가 인자를 받아서 BindAction을 호출하는 함수를 만들어 보자

![](https://blog.kakaocdn.net/dna/0CZaW/btsOBqpyvJK/AAAAAAAAAAAAAAAAAAAAADL7lvZXrasB1tG4l_86lduFhxvZRw4N9FXdbnq0a_lf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=PcfFNnfZhRSlTHYGjjycA7GQsdA%3D)

BindAction의 인자들을 받는 NativeBindInputAction함수를 만들어주자.

```
UCLASS()
class KNIGHT_API UKnightInputComponent : public UEnhancedInputComponent
{
	GENERATED_BODY()
	
public:
	 template<class UserObject, typename CallbackFunc>
	 void BindNativeInputAction(const UDataAsset_InputConfig* InInputConfig, const FGameplayTag& InInputTag, ETriggerEvent TriggerEvent, UserObject* ContextObject, CallbackFunc Func);
};
```

우리가 이전에 만들어둔 FindNativeInputActionByTag를 호출해서 InputAction을 찾아오자

```
template<class UserObject, typename CallbackFunc>
inline void UKnightInputComponent::BindNativeInputAction(const UDataAsset_InputConfig* InInputConfig, const FGameplayTag& InInputTag, ETriggerEvent TriggerEvent, UserObject* ContextObject, CallbackFunc Func)
{
	checkf(InInputConfig, TEXT("Input config data assets is null, can not proceed with binding!!"));
	
	if (UInputAction FoundAction = InInputConfig->FindNativeInputActionByTag(InInputTag))
	{
		BindAction(FoundAction, TriggerEvent, ContextObject, Func);
	}

	
}
```

GameplayTag를 활용할 수 있는 우리의 Component로 바꿔주자

Edit->Project Setting -> Input Component 검색

![](https://blog.kakaocdn.net/dna/epT11V/btsOCkI1vK9/AAAAAAAAAAAAAAAAAAAAAP2rmMw_cyIhU-8olbsV8Qd_VXguKJJECPIQgCfE6a2I/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2Bv77NHN9Jja7D2N0%2FqYJGLJBnzI%3D)

### 

이제 Bind할 수 있도록 함수를 만들었으니 실제 character class에 가서 Input에 다른 Action을 Binding을 해보자

### Binding Input

**UEnhancedInputLocalPlayerSubsystem**은 언리얼5의**Enhanced Input System**에서

입력 처리의 전반적인 흐름에서 어떤 입력 맵(Mapping Context)을 현재 활성화할지 를 제어하는 역할을 한다.

(그래서 UEnhancedInputLocalPlayerSubsystem에 Mapping Context를 등록해줘야한다.)

아래 코드의 흐름은

0. 내 캐릭터가 호출될 때 같이 호출되는 SetupPlayerInputComponent 함수에 override해서 input action을 매핑합니다.

1. LocalPlayer의 SubSystem을 찾아온다.

2. 거기에 MappingContext를 해준다.

3.InputComponent를 내가 만든 InputComponent로 캐스팅해준다

4. 내가 만든 InputComponent에 Action을 Binding해준다.

```
void AKnightHeroCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	checkf(InputConfigDataAsset, TEXT("Have to mapping InputConfigDataAsset"));


	ULocalPlayer* LocalPlayer = GetController<APlayerController>()->GetLocalPlayer();
	UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(LocalPlayer); 
	
	check(Subsystem);

	Subsystem->AddMappingContext(InputConfigDataAsset->DefaultMappingContext, 0);  

	UKnightInputComponent* KnightInputComponent = CastChecked<UKnightInputComponent>(PlayerInputComponent);
	  
	KnightInputComponent->BindNativeInputAction(InputConfigDataAsset, KnightGameplayTags::InputTag_Move, ETriggerEvent::Triggered, this,&ThisClass::Input_Move);
	KnightInputComponent->BindNativeInputAction(InputConfigDataAsset, KnightGameplayTags::InputTag_Look, ETriggerEvent::Triggered, this,&ThisClass::Input_Look);
  }
```

아래는 Binding한 Action들 입니다.

```
void AKnightHeroCharacter::Input_Move(const FInputActionValue& InputActionValue)
{ 
	// X: A or D
	// Y: W or X
	const FVector2D MovementVector = InputActionValue.Get<FVector2D>();
	const FRotator MovementRotator(FRotator(0.0f, Controller->GetControlRotation().Yaw, 0.0f));

	if (MovementVector.Y != 0.0f)
	{
		const FVector ForwardDirection = MovementRotator.RotateVector(FVector::ForwardVector);
		AddMovementInput(ForwardDirection, MovementVector.Y);
	}
	
	if (MovementVector.X != 0.0f)
	{
		const FVector RightDirection = MovementRotator.RotateVector(FVector::RightVector);
		AddMovementInput(RightDirection, MovementVector.X);
	} 
}
void AKnightHeroCharacter::Input_Look(const FInputActionValue& InputActionValue)
{
	Debug::Print(TEXT("Input_LOOK"));
	const FVector2D LookAxisVector = InputActionValue.Get<FVector2D>();
	if (LookAxisVector.Y != 0.0f)
	{ 
		AddControllerPitchInput(LookAxisVector.Y);
	}

	if (LookAxisVector.X != 0.0f)
	{ 
		AddControllerYawInput(LookAxisVector.X);
	}
}
```

여기에 본인이 점프도 구현해보세요 ^-^

<https://tithingbygame.tistory.com/206>

[[UE5] 캐릭터 점프 구현 ( Enhanced Input + GameplayTags)

void AKnightHeroCharacter::SetupPlayerInputComponent(UInputComponent\* PlayerInputComponent){ KnightInputComponent->BindNativeInputAction(InputConfigDataAsset, KnightGameplayTags::InputTag\_Jump, ETriggerEvent::Started, this,&ACharacter::Jump); KnightInputCo

tithingbygame.tistory.com](https://tithingbygame.tistory.com/206)