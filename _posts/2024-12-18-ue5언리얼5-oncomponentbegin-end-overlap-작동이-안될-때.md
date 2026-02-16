---
title: "[UE5/언리얼5] OnComponentBegin, End Overlap 작동이 안될 때"
date: 2024-12-18
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

신경써야될 문제가 2개 있습니다.

**1. AddDynamic을 생성자에서 하지 말자**

AddDynamic을 BeginPlay에서 해줘야 됩니다.

```
	BoxComponent->OnComponentBeginOverlap.AddDynamic(this, &ThisClass::PrintPawnTags);
	BoxComponent->OnComponentEndOverlap.AddDynamic(this, &ThisClass::StopPrintingTags);
```

<https://www.reddit.com/r/unrealengine/comments/hbahyn/event_begin_overlap_doesnt_trigger_solution/>

**2. Bind할 함수에 UFUNCTION 매크로를 선언하자**

UFUNCTION매크로를 선언하지 않으면 함수가 바인드 되지 않습니다. 아예 함수가 콜이 안되니 답답한 상황을 겪을 수 있습니다.

<https://forums.unrealengine.com/t/c-oncomponentbeginoverlap-error-with-adddynamic/361612/2>

[[C++] OnComponentBeginOverlap Error with .AddDynamic

UFUNCTION() void TriggerEnter(class UPrimitiveComponent\* HitComp, class AActor\* OtherActor, class UPrimitiveComponent\* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult & SweepResult); UFUNCTION() void TriggerExit(class UPrimitiveComponent

forums.unrealengine.com](https://forums.unrealengine.com/t/c-oncomponentbeginoverlap-error-with-adddynamic/361612/2)

이렇게 2가지가 문제였습니다. 요즘 검색도 GPT로하는 개발자 분들이 많은데, 이런 노하우(?)들은 GPT도 잘 모르더라고요. 다들 GPT에만 의존하지 맙시다. 저도 많이 쓰긴합니다 :)