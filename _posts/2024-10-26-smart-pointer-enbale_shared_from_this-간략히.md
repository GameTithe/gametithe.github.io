---
title: "smart pointer, enbale_shared_from_this - 간략히"
date: 2024-10-26
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### 1. Smart Pointer

### 포인터를 자동으로 관리해준다. 메모리 관리를 수동으로 할 필요 없이 스마트 포인터를 사용하여 객체의 메모리 해제를 자동으로 처리할 수 있다.

* **std::unique\_ptr**: 단독 소유권을 가지며, 다른 포인터와 소유권을 공유할 수 없다. 객체가 더 이상 사용되지 않을 때 자동으로 메모리를 해제합니다.
* **std::shared\_ptr**: 여러 개의 포인터가 하나의 객체를 공유할 수 있다. 모든 포인터가 더 이상 객체를 참조하지 않으면 메모리가 자동으로 해제된다.
* **std::weak\_ptr**: shared\_ptr와 함께 사용할 수 있으며, 객체의 소유권을 가지지 않고 단순히 참조한다. 따라서shared\_ptr이 있는 동안에만 객체를 사용할 수 있다.

### 2. Smart Pointer 사용이유

* **메모리 누수**: 사용 후 메모리를 해제하지 않는 경우 메모리 leak이 일어난다.
* **잘못된 메모리 접근**: 이미 해제된 메모리에 접근하려고 하면 크래쉬가 날 것이다... (이미 다른 데이터가 들어가 있다면 안날 수도 있다... 그럼 더 큰일!)
* **이중 해제**: 같은 메모리를 여러 번 해제하려고 하면 크래쉬가 날 것이다...

### 3. enable\_shared\_from\_this이 뭔데..?

#### 문제 상황:

std::shared\_ptr를 사용하다 보면, 객체 내에서 자기 자신에 대한 shared\_ptr를 생성해야 할 때가 있다.

예를 들어, 멤버 함수에서 std::shared\_ptr를 생성해 반환하는 경우가 있을 수 있다. 이때 std::shared\_ptr(this)를 사용하면 문제가 발생합니다:

![](https://blog.kakaocdn.net/dna/Q8mkv/btsKkk8oVfb/AAAAAAAAAAAAAAAAAAAAAN29LxYwh3qD1m3dPTqAXgt7Y9YYd_Gu4YN3wbfLKIxl/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=v1fIXGSOvFIF0zjp8q8EIe0er38%3D)

이미 이 객체가 다른 std::shared\_ptr에 의해 관리되고 있다고 가정하면, 이렇게  std::shared\_ptr를 만들어서 return한다면  **두 개의 shared\_ptr가 같은 객체를 관리하게 되어 참조 카운트가 제대로 동작하지 않게 된다**.

#### **그래서**

enable\_shared\_from\_this는 **객체가 이미 shared\_ptr에 의해 관리되고 있을 때, 객체 내부에서 안전하게 자기 자신을 shared\_ptr로 반환할 수 있도록 도와준다.**

![](https://blog.kakaocdn.net/dna/biRZg6/btsKl7fmUNQ/AAAAAAAAAAAAAAAAAAAAALFZPDw2Oz0D55pSLzsADhZx8LW69-nLdd5I8gORI4Rz/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=l%2BNXmC2c3Nl3T8zodAgJoynjb5o%3D)

* **enable\_shared\_from\_this를 상속**하면 객체는 내부적으로 weak\_ptr를 통해 자기 자신을 추적하게 됩니다.
* **shared\_from\_this()**를 호출하면, 이미 존재하는 shared\_ptr로부터 **참조 카운트를 공유하는 새로운 shared\_ptr**를 생성한다. 따라서 참조 카운트가 올바르게 관리된다.