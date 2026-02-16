---
title: "[GameEngineArchitecture] C++ Review"
date: 2025-07-24
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

크래프톤 모집 공지에 적혀 있던 글이다.

![](https://blog.kakaocdn.net/dna/bFv5Ot/btsPx2AErNt/AAAAAAAAAAAAAAAAAAAAABHolKsbFw8QttfpBsEYkE_DlBJzL6A3e9Zw4JKnrnwS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=D0BogGxAH2mZ%2FCAymLbwKa78IkU%3D)

테크랩 합격에 도움이 되고자... 빠르게 읽어보려고한다.

시작은 3장인

Fundamental of Software Engeering for Games에서 시작하겠습니다.

이 장에서는 게임 프로그래머가 반드시 갖추어야 할 기초 지식들을 다룰 것입니다.

수 체계와 표현법, 전형적인 컴퓨터 및 CPU의 구성 요소와 아키텍처, 머신 및 어셈블리 언어, 그리고 C++ 프로그래밍 언어에 대해서 살펴볼 것입니다.

객체 지향 프로그래밍(OOP)의 핵심 개념들을 복습한 후,

게임 제작에 있어서 유용할 고급 주제들로 들어갈 것입니다.

### 

### **OOP 간단 복습**

#### **1. 클래스와 객체**

클래스란 속성(데이터)와 동작(코드)를 함께 묶어 의미 있는 하나의 단위를 구성한 것이다.

예를 들어,  반려견 코코는 개(dog)라는 클래스의 하나의 인스턴스다.

즉, 클래스와 인스턴스 사이에는 일대다(one-to-many) 관계가 존재한다.

#### **2. 캡슐화**

객체가 외부 세계에 대해 **제한된 인터페이스만을 제공하고, 내부 상태와 구현 세부사항은 감추는 것을 의미합니다.**

그렇게 되면 **사용자 입장에서는 복잡한 내부 구현을 알 필요 없이, 제한된 인터페이스만 이해하면 되므로 프로그램이 단순해집니다**.

또한 클래스 작성자는 해당 클래스의 인스턴스가 항상 논리적으로 일관된 상태를 유지하도록 제어할 수 있습니다.

#### **3. 상속**

상속은 하나의 클래스가 다른 클래스로붑터 속성과 동작을 물려받는 개념입니다.

상속 관계에서는 기존 클래스(부모 클래스)를 기반으로 새로운 클래스(자식 클래스)를 만들 수 있다.

상속은 클래스들 간의 계층적(트리구조) 관계를 만들어냅니다.

상속은 클래스 간의 is-a 관계를 만들어줍니다.

Circle은 Shape의 한 종류이므로, Circle은 Shape에서 파생되는 것이 자연스럽죠?

클래스 계층도를 그릴 때는 UML(Unified Modeling Language, 통합 모델링 언어) 표기법을 사용합니다.

이 표기법에서는

직사각형이 클래스를 나타내고, 속이 빈 화살표가 상속을 나타낸다. 상속 화살표는 자식 클래스에서 부모 클래스로 향합니다.

![](https://blog.kakaocdn.net/dna/bGASMv/btsPvYlfKXr/AAAAAAAAAAAAAAAAAAAAAP-YD1aBnDyJcZQGT1OrDjK6KUbKzuo67ZaJEgVqSvjb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=FEs6aG4kxBoSNw54nZzsNULS03A%3D)

#### **3-1 다중 상속**

한 클래스가 둘 이상의 부모 클래스를 가지는 것을 의미합니다.

**가능한 구조이지만 실제로는 혼란과 기술적인 문제를 많이 야기합니다.**

다중 상속은 간단한 트리 구조를 복잡한 그래프 형태의 상속 구조로 바꾸기 때문입니다.

예시로는 Diamond Problem(죽음의 다이아몬드)가 있습니다.

(간단하게 설명하면,

Class D는 Class B,C를 상속받고,

class B,C는 class A를 상속받기 때문에 A의 멤버 함수를 가지고 있겠죠?

그럼 D는 A의 멤버함수를 2번이나 상속받아 중복이 발생할 것입니다 -> virtual 상속으로 해결가능하나 복잡해짐)

![](https://blog.kakaocdn.net/dna/bwPArs/btsPvE8qRPX/AAAAAAAAAAAAAAAAAAAAANCuMCJ_xfV7i0d8v6KWumvkUETflmtB4kFbWaNsPboR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FmK%2Bi0DSHJfneMiqdoDoTl1nCx8%3D)

또한 다중 상속은 casting을 어렵게 만든다. 객체 내부에 여러 개의 가상함수 테이블 포인터가 존재하므로, **어떤 부모 클래스로 캐스팅하는냐에 따라 포인터 주소 자체가 달라질 수 있습니다.**

![](https://blog.kakaocdn.net/dna/EwZs7/btsPvZR1GWU/AAAAAAAAAAAAAAAAAAAAAHaiHc96MVhVq0Vjf8PIcwUIEM3W_4cMFCdpO-DuuA2y/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wLW05jvOEPEnBsnt6BGrMfjV66A%3D)

이러한 이유들로 대부분의 C++ 개발자들은 다중 상속을 완전히 피하거나, 매우 제한된 형태로만 사용합니다.

경험적인 규칙은

부모가 없는 단순한 클래스만 다중 상속의 대상으로 삼는다는 것입니다.

(이런 규칙 또한 죽음의 다이아몬드는 피하겠지만, 캐스팅에 대한 문제는 해결하지 못할 것 같네요)

#### 

#### **4. 다형성**

다형성은 다양한 **타입의 객체들을 하나의 공통된 인터페이스로 다룰 수 있게 해주는 언어적 특성입니다.**

이 공통 인터페이스 덕분에

서로 다른 타입의 객체들을 사용자 입장에서는 같은 타입의 객체들처럼 다룰 수 있다.

이를 위해서

1. 각 도형 타입마다 개별 클래스르 정의

2. 각 클래스들은 shape이라는 base class를 상속받는다.

3. 각 클래스는 virtual 함수인 Draw()를  오버라이드한다.

```
struct Shape
{
    virtual void Draw() = 0;       // 순수 가상 함수 (인터페이스)
    virtual ~Shape() { }           // 소멸자도 가상으로 선언 (안전한 파괴)
};

struct Circle : public Shape
{
    virtual void Draw()
    {
        // 원으로 그리기
    }
};

struct Rectangle : public Shape
{
    virtual void Draw()
    {
        // 사각형으로 그리기
    }
};

struct Triangle : public Shape
{
    virtual void Draw()
    {
        // 삼각형으로 그리기
    }
};
```

이렇게 구성하게 되면, 아래와 같이 깔끔하게 도형에 맞는 Draw를 호출 할 수 있습니다.

```
void drawShapes(std::list<Shape*>& shapes)
{
    std::list<Shape*>::iterator pShape = shapes.begin();
    std::list<Shape*>::iterator pEnd = shapes.end();
    for (; pShape != pEnd; pShape++)
    {
        pShape->Draw(); // 각 도형의 Draw() 함수 자동 호출 (virtual)
    }
}
```

#### **5. 구성(Composition) 과 집합(Aggregation)**

구성이란 여러 객체가 상호작용하여 상위 수준의 작업을 수행하도록 만드는 설계방식입니다.

**클래스간에 has-a  또는 uses-a 관계를 만들어줍니다**.

(엄밀히 말하면 has-a => composition, uses-a => aggregation)

우주선은 엔진을 가지고 있고, 엔진은 연료탱크를 가지고 있다고 예를 들어봅시다.

이런 관계가 바로 구성/집합이다. 이 방식을 사용하면 개별 클래스는 더 단순하고 목적이 명확해지며,  
**디버깅, 재사용 측면에서 훨씬 용이해집니다.**

**초보 객체지향 프로그래머는 상속에 과하게 의존하는 성향이 있는 반면, 구성/집합은 잘 사용하지 않는 경향이 있다.**

게임의 UI를 설계 중이라고 가정해보자.

Window라는 클래스는 사각형 GUI요소를 나타내고, Rectangle이라는 수학적 사각형 개념을 구현한 클래스가 있다.

초보자는 Window가 Rectangle을 상속받게 설계할 수 있다. (is-a 관계)

하지만 Window가 Rectagle을 포함하거나 참조하게 하면 (has -a 관계)

두 클래스 모두 간결하고 재사용이 용이하게 설계될 것이다.

#### **6. 디자인 패턴**

동일한 유형의 문제가 반복적으로 발생하고, 다양한 프로그래머들이 유사한 해결 방식을 적용한다면, 우리는 그것을 디자인 패턴이라고 부릅니다.

대표적인 디자인 패턴으로

**1. singleton**

특정 클래스의 인스턴스를 오직 하나만 생성하도록 보장하고, 전역 접근 지점을 제공한다.

**2. iterator**

내부 구조를 노출하지 않고,

각 요소에 효율적으로 접근할 수 있는 방법을 제공한다.

**3. abstract factory**

서로 관련되거나 의존적인 클래스들을

구체적인 클래스를 명시하지 않고 생성하는 인터페이스 제공

### **6.1 RAII**

RAII 패턴은 매우 유용한 디자인 패턴 중 하나이다.

**이 패턴에서는 자원의 획득과 해제를 객체의 생성자/소멸자에 자동으로 연결시킨다.**

자원 획득 => 생성자에서 실행

자원 해제 => 소멸자에서 자동 수행

이렇게하면 자원 해체를  잊어버리는 실수를 방지할 수 있다.

로컬 객체 하나 생성하면, 자원을 할당하고,

범위를 벗어나면 자동 해제된다.

```
class AllocJanitor
{
public:
    explicit AllocJanitor(mem::Context context)
    {
        mem::PushAllocator(context);
    }

    ~AllocJanitor()
    {
        mem::PopAllocator();
    }
};
```

```
void f()
{  
    // 단일 프레임 할당자에서 임시 버퍼 할당
    {
        AllocJanitor janitor(mem::Context::kSingleFrame);

        U8* pByteBuffer = new U8[SIZE];
        float* pFloatBuffer = new float[SIZE];

        // 버퍼 사용...
        // 메모리 해제는 불필요: 단일 프레임 할당자이기 때문!
    } 
    // janitor가 소멸되며 자동으로 pop
 
}
```

Cpp 메뉴얼

<https://en.cppreference.com/w/cpp.html>

[C++ reference - cppreference.com

Calendar (C++20) − Time zone (C++20)

en.cppreference.com](https://en.cppreference.com/w/cpp.html)

C++11 주요 기능 요약 글

<https://www.codeproject.com/Articles/570638/Ten-Cplusplus11-Features-Every-Cplusplus-Developer>

[CodeProject

For those who code

www.codeproject.com](https://www.codeproject.com/Articles/570638/Ten-Cplusplus11-Features-Every-Cplusplus-Developer)

아래는 간단한 게임 엔진 survey입니다.

**1. Quake 엔진**

게임 업계를 진보하게 만들어준 엔진이라고 볼 수 있다.

우리가 아는 FPS의 아버지 DOOM도 quake 엔진 기반이라고 볼 수 있다.

Quake1,2,3 모두 Quake 엔진으로 만들어졌다.

Quake1,2 모두 오픈 소스로 공개되어있다.

**2. 언리얼 엔진**

FPS 게임인 Unreal을 만들기 위해 제작된 엔진이 Unreal이다. ~~언리얼을 언리얼로 만든 언리얼한 상황~~

등장하자마자, Quake의 대항마로 인기를 얻음

언리얼 또한 소스코드를 공개했기에 ( 초반에는 돈주고 팔았음, 지금은 우리도 볼 수 있음 )

대부분의 회사들이 커스텀해서 사용한다.

**3. Source 엔진 (Valve)**

Half-Life2, HL2: Episode One,Two, Team Fortress2 등 에 사용됨

그래픽 성능은 UE4와 맞먹는다. (제한적으로 소스 공개)

**4. Frostbite(EA DICE)**

Frostbite 엔진은 2006년 Battlefield: Bad Company 개발을 위해 DICE가 만든 엔진에서 시작됐다.

Battlefield, Need for Speed, Dragon Age, Star Wars Battlefront II 등을 만드는데 사용되었다.

소스는 비공개

**5.RAGE(Rockstar)**

RAGE (Rockstar Advanced Game Engine)는 Rockstar의 독점 엔진이다.

GTA가 RAGE로 만들어졌다..! 소스는 비공개이다. 

**6. CRYENGINE**

NVIDIA 기술 데모용으로 시작해서 게임 엔진으로 확장된 케이스이다. 

CRYENGINE을 통해서 Far Cry가 제작되었다.

**7. PhyreEngine(Sony의 파이어엔진)**

플레이 스테이션 플랫폼에서의 개발을 용이하게 만들기 위해서 제작됨

PhyreEngine은 Sony의 라이선스를 보유한 개발자에게는 PlayStation SDK의 일부로 무료 제공된다**.**

flOw, Flower, Journey (thatgamecompany), Unravel (Coldwood Interactive) 등을 제작하는데 사용되었다.

**8. Unity**

쉬운 개발, 멀티플랫폼 배포 간소화을 위해 만들어진 게임 엔진이다.

직관적인 에디터 기반 개발 환경과 플랫폼별 성능 분석 및 최적화 도구가 있다. 품질 vs 성능 트레이드오프 설정 가능하다.

소스 코드는 공개하지 않는다.

Deus Ex: The Fall, Hollow Knight 등에 사용되었다.