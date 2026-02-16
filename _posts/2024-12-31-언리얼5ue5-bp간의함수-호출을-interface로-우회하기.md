---
title: "[언리얼5/UE5] BP간의함수 호출을 Interface로 우회하기...?"
date: 2024-12-31
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

상황설명

BP\_PredictionSpline에서 Hero의 Camera Position을 가져오고 싶은 상황입니다.

아래와 같이 BP\_Hero에서 GetCamera함수를 만든다면, Casting을 한 번 하고 호출할 수 있습니다.

![](https://blog.kakaocdn.net/dna/7i7c2/btsLCHfLnW8/AAAAAAAAAAAAAAAAAAAAANf885WLsD0RnnTSImEVuxjRsUIlUj3DCNeZJokWgdMM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=eLashc%2FTt4W7HNJUkoUUMF8eEzU%3D)![](https://blog.kakaocdn.net/dna/bJ1tSV/btsLA9dgIKZ/AAAAAAAAAAAAAAAAAAAAALnXBlV2WH8BHD6FW95rHwfD2KJzi-wu8G4MyVqnItP-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=m8FSVFmngxCHluUd6f9na0Xn5MY%3D)

바로 호출하려면 어떻게 할 수 있을까요? 정답은 interface로 구현하는 것입니다.

아래와 같이 바로 호출할 수 있습니다.

![](https://blog.kakaocdn.net/dna/kMG9o/btsLBuVZopm/AAAAAAAAAAAAAAAAAAAAABjdgSvYWG7UHAIhn2sHA_b6IKvJepWAMPwfUMfhR-zO/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=o6Xoq9nk4A2gtixzDE5wHzJej%2FU%3D)![](https://blog.kakaocdn.net/dna/b253CL/btsLDnVeufR/AAAAAAAAAAAAAAAAAAAAAH3-l3X9S55Ym1FhkfD7l78vVsguV_fBAqTh75UOBpdt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=WIOEa6o8YHJxbzU%2FNr3Xw7xr7EQ%3D)

아니 근데!

Interface도 hero에 구현한건데, 왜! !!

함수는 호출이 안되고, Interface는 호출이 되는 것일까요?

우선 GetOwner는 Actor를 반환한다는 것을 기억하고 갑시다.

UInterface가 UObject를 상속받아서 만들어진 것을 볼 수 있습니다.

![](https://blog.kakaocdn.net/dna/dqFbUC/btsLCGHVfIc/AAAAAAAAAAAAAAAAAAAAADafsh0IEt2Y78HRY0pqqXUz5Th630baEHv_iyrGvNqE/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=a4GMpQX5IVRD3OtESRPxIvjn208%3D)

ACharacter도  APawn을 상속받고,

APawn은 AActor를 상속받고,

AActor는 ?? UObject를 상속받습니다.

![](https://blog.kakaocdn.net/dna/cz7S5t/btsLAUgv9Oo/AAAAAAAAAAAAAAAAAAAAAM20V6cMysG_eDxSx6S1wXmMjtvzDbJ7dMjytda3sWXf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=7mFvtG9iaCKelpdDadc7lZr5omU%3D)

Interface와 Actor 모두 Object를 상속받으니, Get Owner함수를 사용하면 Interface는 바로 호출이 가능한 것 입니다.