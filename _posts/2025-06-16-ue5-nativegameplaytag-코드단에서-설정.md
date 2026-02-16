---
title: "[UE5] NativeGameplayTag ( 코드단에서 설정 )"
date: 2025-06-16
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

```
// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "NativeGameplayTags.h"

namespace KnightGameplayTags
{
	/*Input Tags*/
	KNIGHT_API UE_DECLARE_GAMEPLAY_TAG_EXTERN(InputTag_Move)
	KNIGHT_API UE_DECLARE_GAMEPLAY_TAG_EXTERN(InputTag_Look)
}
```

KNIHGT\_API(프로젝트 이름을 어떻게 설정했는지에 따라 다르게 입력해야 될 것이다.): 모듈 밖에서도 사용가능하도록 해준다.

InputTag\_Move/ Look: 코드에서 사용할 식별자

```
#include "KnightGameplayTags.h"

namespace KnightGameplayTags
{
	/*Input Tags*/
	UE_DEFINE_GAMEPLAY_TAG(InputTag_Move, "InputTag.Move")
	UE_DEFINE_GAMEPLAY_TAG(InputTag_Look, "InputTag.Look")
}
```

위에서 설정한 식별자에 Tag 등록

이렇게하고 컴파일하면 링크에러가 생길텐데,

모듈하나를 추가해주자

우리가 include란 NativeGameplayTag의 위치를 찾아보면 GameplayTags 산하에 존재한다.

![](https://blog.kakaocdn.net/dna/1IrKW/btsOCNRpP5o/AAAAAAAAAAAAAAAAAAAAAJQLYb6ie1Js-pJ5KZQEG3zkI2-GyKAwr2gwPDS3jTVs/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xWVgEvgs3j8ESoxtFehxdpp06bI%3D)

Build.cs에 모듈을 추가해주면 오류가 사라질 것이다.

![](https://blog.kakaocdn.net/dna/d57BRR/btsOAYNVY1Z/AAAAAAAAAAAAAAAAAAAAANg9LmfPleiShrfevkSB6ybOoMn9--ams0Xu39acqL1u/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=idg6oWCMd9Z0OHVtJXLgd5qiDPY%3D)

잘 만들어졌는 지 확인해보자

Edit -> Project Setting -> GameplayTags->Manage Gameplay Tags를 선택하자

![](https://blog.kakaocdn.net/dna/XuxJ3/btsOA5lGTZk/AAAAAAAAAAAAAAAAAAAAAAW0oEamwHd8QOSrRI8KoeltoIi4IkYC8VHKpZxtOCrC/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=E3xatAJjOoQQTonNSXCfzIuBNdE%3D)

그럼 우리가 만든 Tags를 확인할 수 있다.

![](https://blog.kakaocdn.net/dna/lMVtk/btsOCmUiF8v/AAAAAAAAAAAAAAAAAAAAAJ9lZteaPBrHFH_3DWRtKyYqiYklJrlwp0yRBLdMJesC/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=u4MDOPUXOhi4hUBR4IUnVCbW7ZM%3D)