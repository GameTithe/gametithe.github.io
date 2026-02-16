---
title: "[언리얼5/UE5] Hard/Soft Reference"
date: 2025-06-14
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

**Hard Reference는 참조된 에셋을 즉시 메모리에 로드하고 유지하며**

**Soft Reference는 참조만 유지하고 원하는 시점에 수동으로 에셋을 로드할 수 있도록 한다.**

Blueprint에서는 내가 BP\_ThirdPersonCharacter를 상속 받은 TestActor를 로드하려면  
BP\_ThirdPersonCharacter 강제로 로드한다. (Hard Reference)

![](https://blog.kakaocdn.net/dna/brMCOD/btsOAlh1dXQ/AAAAAAAAAAAAAAAAAAAAAMvJMmbaw7YxRdA3f0an8cyUAvvTg2NS4a1BlYIb5YO1/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=iSN0HXZO6hkRn2OXVGHqKmWWKvs%3D)

이런 문제를 우회하기 위해서 Blueprint로는 절대 casting을하지 말고, interface로 casting을 하라는 소문(?)이 있다.

하지만 이것 또한 사실이 아니다. casting자체는 비용이 들지 않는다.

실제 문제는 아래와 같다.  
Test Actor에 접하고 싶을 때, 용량이 큰, BP\_ThirdPersonCharacter를 같이 로드해야된다. (Hard Reference)

![](https://blog.kakaocdn.net/dna/ch0XP8/btsOAEBCuVG/AAAAAAAAAAAAAAAAAAAAAJ3AXsMy5uHyjTzPLXSpzn2tUHiwwh1xFvvI51-fxIB0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=s8%2F5P1UYRAiw6H5Yk7KuT9CXW1U%3D)

또다른 상황으로 보자

![](https://blog.kakaocdn.net/dna/cyvMLO/btsOAkpTWBe/AAAAAAAAAAAAAAAAAAAAAOFH6EVU2pfXHizWtNQ4Z_GonrbCuyutr-ztthdvQdxC/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ibwfrhzfLtg3c2VM0DI6dO2ptAw%3D)

연결된 흰색 선들이 모두 hard reference를 이어져있어서, 중간 지점의 값을 얻으려고 할 때도 이미지에 보이는 모든 것들의 값을 계산한 뒤에야 얻을 수 있다면, 행동 하나하나에 대한 로딩시간이 길어질 것이다.

마지막 예시

![](https://blog.kakaocdn.net/dna/PlKz5/btsOCm0uU0x/AAAAAAAAAAAAAAAAAAAAAGOKa7AJUq2TkyDy9CrtlwSe4SJOq7xU4sskodXThqSq/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=kBfbpwo%2FdhQ0QXi3lfyhT7WWXk0%3D)

이렇게 시작화면에서 용량이 큰 보스몹을 캐스팅한다면, 로딩 시간이 오래걸릴 것이다.  
(하지만 유저는 오늘 보스몹까지 못갈것같은데,,,?)

그런데말입니다..

이렇게 hard reference를 항상 피하고 싶은 것처럼 이야기는 했지만, ( 실제로 피하는게 맞긴한데,,  )

허용해줄 수 있는 경우도 있다.

위의 예시처럼 BP\_ThirdPersonCharacter는 캐릭터를 사용하려면 대부분의 경우에 사용된다.

때문에 BP\_ThirdPersonCharacter가 hard reference 되는 것을 막을 필요는 없다.

또 다시 하지만

어쩄든 soft reference가 좋다

아래의 이미지를 보면 체감이 바로 될 것이다.

좌측은 soft reference, 우측은 hard reference

(character가 아닌 보스 몹이었다면?

soft reference: 3kb를 로드해놓고 boss몹이 생성될 쯤, 110MB로드

hard reference: 너가 오늘 보스몹을 볼 지 안볼지는 모르겠고, 일단 110MB 로드

![](https://blog.kakaocdn.net/dna/1piSC/btsOAE9w30z/AAAAAAAAAAAAAAAAAAAAAEa8QtvcgkwaMGx8B3wplZ2w7NqVJifXOsRPMewdFja6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3LwVSi3W6GizOjl2OPXtwQXxysQ%3D)

### 

Hard/ Soft Reference의 장단점을 보자

### **Hard Reference**

**장점**

* 에셋 접근이 쉽다
* 에셋이 로드되어있음을 보장한다

**단점**

* 메모리를 낭비한다.

### **Soft Reference**

**장점**

* 내가 원할 때 에셋을 로드할 수 있다.

**단점**

* 코드가 복잡해질 수 있다.
* 로드 타이밍을 맞추는 것이 어렵다
* 핵심 에셋에는 적합하지 않다.

단순하게 정리하면 아래의 그림과 같다.

![](https://blog.kakaocdn.net/dna/cV8kFc/btsOAwXVXIA/AAAAAAAAAAAAAAAAAAAAAHRHdtMM5GLeW9o31Lw-CKnLySpxExs54kQbZ52Okbn5/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=z0eqIoX8ilAQM0sIq69ffJkm3f0%3D)

우리는 이것을 피하고 싶은 것이고,

피하는 방법은 2가지 있다.

1. native C++ class로 캐스팅하기

![](https://blog.kakaocdn.net/dna/brwYGx/btsOBixOQRe/AAAAAAAAAAAAAAAAAAAAAAm1M7I0E2JHzJ1Z-dji8h4qofvg2SCKwhY_zBDZ4IMV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=jp9bqXzBdBuCS%2B1A2Vx5Z0z71Ic%3D)

이렇게 코드로 했으니까 soft reference겠지..? NOPE

![](https://blog.kakaocdn.net/dna/RpAFi/btsOBYr1k9V/AAAAAAAAAAAAAAAAAAAAACDlgLAdBK7ghfZAoD9NdKisen21dRUpFPMdGZb0xBgY/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=yqFego8Rd8xSDeixrso5BBUrIZI%3D)

이렇게 사용하자

2. 용량이 적은(값이 싼) BP paraent class로 캐스팅하기

**Blueprint에 로직을 부모 클래스에만 추가하기**

BP의 부모 클래스에만 로직을 추가하면 자식 클래스에 불필요한 코드 중복을 줄이고, 메모리 사용과 로딩 시간을 최적화할 수 있다.

**중요한 오브젝트와 기능은 C++로 구현하기**

**BP object reference 피하기**

객체 간의 참조를 줄이거나 인터페이스를 이용하여 의존성을 최소화하자. 모든 오브젝트가 메모리에 로드되어 비효율적으로 프로그램이 실행될 수 있다!

알면 좋은

더보기

### **TObjectPty**

**Access Tracking**

Access 시점을 추적해서 UObject의 라이프사이클 관리 및 에디터 툴 기능 지원에 사용한다.

**Lazy Loading**

Hard reference를 최소화한다.

멤버변수로만 사용된다.( TObjectPtr는 UPROPERTY 안에서만 사용 가능 )

Access Tracking되는 부분은 editor에서만 유효하게 때문에 성능저하에 영향이 없음

###