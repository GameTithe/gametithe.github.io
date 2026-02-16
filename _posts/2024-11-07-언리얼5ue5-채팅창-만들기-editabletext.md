---
title: "[언리얼5/UE5] 채팅창 만들기 (EditableText)"
date: 2024-11-07
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

![](https://blog.kakaocdn.net/dna/bwOdAR/btsKzcn1P23/AAAAAAAAAAAAAAAAAAAAAJSngk0BkxFHlG2IlUK4yvNIsgE0oFpGMGjCkwLryhHu/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1aMG5RHmOUIy%2Funxav1bfyMkdj8%3D)
![](https://blog.kakaocdn.net/dna/v2NVT/btsKyZI2BnG/AAAAAAAAAAAAAAAAAAAAAB1Bb8Nx1E4KFdq5rfw1yJ9t_s7CktnIrl67zta06YE7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=lro7dY1yvy7tyPs3X8pNPtWZ%2Bfo%3D)

## 

## **사전지식**

UEditableText 위젯은 사용자가 텍스트를 입력하고 커밋할 때 다양한 이벤트를 발생시킨다.

이때 OnTextCommitted Delegate가 사용되고, 아래와 같은 state가 존재한다.

![](https://blog.kakaocdn.net/dna/EwXIk/btsKzj1sphK/AAAAAAAAAAAAAAAAAAAAAN3x5W4Vc5TCz7hV3EEAuTGKgjafJs9TMDjNNGoI-n8g/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=LBVyv8XmGvSySDV%2Fqi6gW9gsi9U%3D)![](https://blog.kakaocdn.net/dna/bcNbt2/btsKz4P1ZgL/AAAAAAAAAAAAAAAAAAAAAAzVXRpxw0hKccGc-e1we-OXxveLu2lnmCcqPsifFj_F/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Eh7%2BnLd%2Bfqt9kArV6LfNc1zkjHQ%3D)

#### **NativeConstruct**

NativeConstruct는 UUserWidget의 라이프사이클에서 **위젯이 화면에 추가되고 나서 호출되는 함수이다.**

UI 가 화면에 표시되기 전에 추가적인 설정이나 초기화를 수행할 때 사용된다.

#### 1.Enter 이벤트를 받아주자. (Edit ->ProjetSetting -> Input ->.....)

Character.cpp

```
PlayerInputComponent->BindAction(TEXT("Chat"), EInputEvent::IE_Pressed, this, &ThisClass::ChatButtonPressed);
```

```
void ASCharacter::ChatButtonPressed()
{
	SController = SController == nullptr ? Cast<ASPlayerController>(Controller) : SController;
	if (SController)
	{ 
		SController->ActiveChatBox();
	}
}
```

#### 2. Chatting창 활성화

PlayerController.cpp

```
void ASPlayerController::ActiveChatBox()
{
	SHUD = SHUD == nullptr ? Cast<ASHUD>(GetHUD()) : SHUD;
	if (SHUD && SHUD->Chatting)
	{ 
		SHUD->Chatting->ActivateChatText();
	}
}
```

Chatting.cpp

```
void UChatting::ActivateChatText()
{
	if (ChatText)
	{  
		ChatText->SetIsEnabled(true);
		ChatText->SetFocus();
	}
}
```

### 3. Chatting창 알고리즘

Chatting.cpp

```
//입력이 들어왔을 때 호출됨
void UChatting::OnTextCommitted(const FText& Text, ETextCommit::Type CommitMethod)
{
	// OnEnter == 뭐가가 입력됨
	if (CommitMethod == ETextCommit::OnEnter && ChatText)
	{ 
		FText InputText = ChatText->GetText();

		if (!InputText.IsEmpty())
		{
			ASPlayerController* PlayerController = Cast<ASPlayerController>(GetWorld()->GetFirstPlayerController());
			if (PlayerController)
			{
				APlayerState* PlayerState = PlayerController->GetPlayerState<APlayerState>();
				FString Message = FString::Printf(TEXT("%s: %s"), *PlayerState->GetPlayerName(), *InputText.ToString());

				// 채팅 메시지를 보내기 위한 Server RPC 호출
				PlayerController->ServerSendChatMessage(Message);
                
                //메시지를 뿌르고 나서는 채팅창 비활성화
				DeactiveChatText(PlayerController);
			}
		}
	}

}
```

```
// UI가 만들어지고 호출됨(초기화용도)
void UChatting::NativeConstruct()
{
	APlayerController* PlayerController = GetWorld()->GetFirstPlayerController();
	if (PlayerController)
	{
		ChatText->OnTextCommitted.AddDynamic(this, &UChatting::OnTextCommitted);
		ChatText->SetIsEnabled(false);
	}
}
//채팅창 활성화
void UChatting::ActivateChatText()
{
	if (ChatText)
	{
		ChatText->SetIsEnabled(true);
		ChatText->SetFocus();
	}
}
//채팅창 비활성화
void UChatting::DeactiveChatText(ASPlayerController* Controller)
{
	if (ChatText && Controller)
	{
		ChatText->SetText(FText::GetEmpty());
		ChatText->SetIsEnabled(false);

		FInputModeGameOnly InputMode;
		Controller->SetInputMode(InputMode);
	}
}
```

#### 4. Chatting 뿌리기

Controller.cpp

```
//서버
void ASPlayerController::ServerSendChatMessage_Implementation(const FString& msg)
{
	ASGameMode* GameMode = Cast<ASGameMode>(GetWorld()->GetAuthGameMode());
	if(GameMode)
	{
		GameMode->SendChatMessage(msg);
	}
}
 
//클라
void ASPlayerController::ClientAddChatMessage_Implementation(const FString& msg)
{
	SHUD = SHUD == nullptr ? Cast<ASHUD>(GetHUD()) : SHUD;
	if (SHUD)
	{
		SHUD->AddChatMessage(msg);
	}
}
```

GameMode.cpp

```
void ASGameMode::SendChatMessage(const FString& Message)
{ 
	auto it = GetWorld()->GetPlayerControllerIterator();

	for(auto i = it; it; it++)
	{
		ASPlayerController* Controller = Cast<ASPlayerController>(*it);
		Controller->ClientAddChatMessage(Message);
	}
}
```

HUD.cpp

```
void ASHUD::AddChatMessage(const FString& Message)
{
	OwningPlayer = OwningPlayer == nullptr ? GetOwningPlayerController() : OwningPlayer;
	if(ChattingClass)
		Chatting = Chatting == nullptr ? CreateWidget<UChatting>(OwningPlayer, ChattingClass) : Chatting;
	 
	if (OwningPlayer && Chatting && ChatMessageClass)
	{ 
		UChatMessage* ChatMessageWidget = CreateWidget<UChatMessage>(OwningPlayer, ChatMessageClass);

		if (ChatMessageWidget)
		{ 
			ChatMessageWidget->SetChatMessage(Message);
			
			Chatting->ChatScrollBox->AddChild(ChatMessageWidget);
			Chatting->ChatScrollBox->ScrollToEnd();
			Chatting->ChatScrollBox->bAnimateWheelScrolling = true;
		}
	}
}
```

도움받은 블로그

### <https://velog.io/@dltmdrl1244/UE5-C-%EB%A9%80%ED%8B%B0%ED%94%8C%EB%A0%88%EC%9D%B4%EC%96%B4-%EC%B1%84%ED%8C%85-%EC%8B%9C%EC%8A%A4%ED%85%9C-%EA%B5%AC%ED%98%84>