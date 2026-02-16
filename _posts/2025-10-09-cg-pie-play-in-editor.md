---
title: "[CG] PIE (Play In Editor)"
date: 2025-10-09
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

PIE(Play In Editor)는 게임 엔진이라면 당연히 포함되어야하는 기능입니다.

이 버튼입니다.

![](https://blog.kakaocdn.net/dna/TGsi5/btsQ2jn8hv1/AAAAAAAAAAAAAAAAAAAAANbqJs7Q9-fN2sl4B4lVT7JAFoAuc2hrLzAoFgPU_NH3/img.jpg?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=LOt2v9poUe0HyZI9kFN083ZnPfQ%3D)

PIE를 구현하기 위해서는 Editor World 에 세팅을 해둔 정보, 값들을 PIE World에 복사를 해줘야합니다.

![](https://blog.kakaocdn.net/dna/bMI1Di/btsQ2ouIgk0/AAAAAAAAAAAAAAAAAAAAAADwZHeYcmbXtj1vJvTyxyVUgAuMg_d-YqVYafQgvdfU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=EhDMkPySnzVhuy0M%2FEmH%2Bn3UG5Q%3D)

그럼 복사만 하면 끝인가?

사실 끝이긴한데, 어떻게 복사를 할 지 고민을 해봐야합니다.

만약 얕은 복사를 했다면,

PIE World 에서는 PIE Tick에 따라서 많은 일이 발생한 경우, 초기 Editor World 로 돌아가기 어려울 것입니다.

![](https://blog.kakaocdn.net/dna/CSpSp/btsQ2npkRkR/AAAAAAAAAAAAAAAAAAAAALzhkyQ4U7J-i4GOeCP1Tfz8_JnkzxevjtDPyG68FKy0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=MFiAGgeX8mm1midEeXV4Lz%2Bb%2BPw%3D)

하지만 모두 깊은 복사를 하게 되면, PIE World로 변화하는데 비용이 많이 들 것입니다.

어떤 것을 깊은 복사를 할 지, 어떤 것을 얕은 복사를 할 지 고민을 해봐야합니다.

저는

Mesh, Material처럼 Manage가 관리하고 있는 Resource들은 얕은 복사를 하였고,

그 외에 위치, 회전, 이동 등은 깊은 복사를 해주었습니다.

아래가 큰 틀에서 보았을 때, 파이프라인입니다.

![](https://blog.kakaocdn.net/dna/nJKhd/btsQZSjxwFJ/AAAAAAAAAAAAAAAAAAAAACETRLkKiVfw5EXz5rVuey0KZPIwRrRn2Fd7vfdKWLhb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=TS02KqFM7kK2smrSqKqNsAzwSeg%3D)

**1. PIE Play를 눌렀을 때, 복사 시작**

```
UWorld* UWorld::DuplicateWorldForPIE(UWorld* EditorWorld)
{ 
	UWorld* Dst = NewObject<UWorld>();
	Dst->Init(EWorldType::PIE); //WorldContext Setting  

	ULevel* SrcLevel = EditorWorld->GetCurrentLevel();
	ULevel* DstLevel = new ULevel(SrcLevel->GetName() + "_PIE");
	
	Dst->SetCurrentLevel(DstLevel);

	// PIE World에 Editor World를 복사하기 시작
	for (AActor* Actor : SrcLevel->GetLevelActors())
	{ 
		AActor* DupActor = static_cast<AActor*>(Actor->Duplicate());  
		if (!DupActor) continue;

		DstLevel->AddActor(DupActor);
	}

	return Dst;
}
```

**2. 얕은 복사 + 깊은 복사**

```
UObject* AActor::Duplicate()
{
	// AActor 복제
	AActor* NewActor = static_cast<AActor*>(GetClass()->CreateDefaultObject());
	if (!NewActor)
	{
		return NewActor;
	}

	// 얕은 복사 추가 
	NewActor->CopyShallow(this);
	NewActor->SetName(FNameTable::GetInstance().GetUniqueName(this->GetBaseName()));

	//필요하면 깊은 복사로 변경
	NewActor->DuplicateSubObjects();
	return NewActor;
	 
}
```

얕은 복사

```
void AActor::CopyShallow(const UObject* Src)
{
	const AActor* BaseActor = static_cast<const AActor*>(Src);

	this->RootComponent = BaseActor->GetRootComponent();
	this->OwnedComponents = BaseActor->GetOwnedComponents();
	this->InitPos = BaseActor->InitPos;
}
```

깊은 복사

```
void AActor::DuplicateSubObjects()
{
	USceneComponent* EditorSceneComp = RootComponent;
	TSet<UActorComponent*> EditorComps = OwnedComponents;

	// Reset current
	RootComponent = nullptr;
	OwnedComponents.clear();
 

	// Root Component 복사
	if (EditorSceneComp)
	{
		USceneComponent* NewRoot = static_cast<USceneComponent*>(EditorSceneComp->Duplicate());
		if (NewRoot)
		{
			NewRoot->SetOuter(this);
			NewRoot->SetOwner(this);
			RootComponent = NewRoot;
			OwnedComponents.Add(NewRoot); 
		}
	}

	// Duplicate other components
	for (UActorComponent* Comp : EditorComps)
	{
		// 이미 루트는 순회 했음
		if (!Comp || Comp == EditorSceneComp) continue;

		UActorComponent* NewComp = static_cast<UActorComponent*>(Comp->Duplicate());
		if (!NewComp) continue;
		NewComp->SetOuter(this);
		NewComp->SetOwner(this);
		OwnedComponents.Add(NewComp); 
	} 
}
```

원래 코드는 계층구조도 유지되도록 구현하였지만, PIE 코드를 이해하는데 방행되니 지웠습니다.

### **결과!**