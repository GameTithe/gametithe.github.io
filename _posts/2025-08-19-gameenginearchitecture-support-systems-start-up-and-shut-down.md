---
title: "[GameEngineArchitecture] Support Systems Start-Up and Shut-Down"
date: 2025-08-19
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

모든 게임 엔진에는 low level support system들을 필요로 합니다. 당연하게 느끼고 있지만, 중요한 작업들을 관리하는 역할을합니다.

(엔진의 시작과 종료, 메모리 관리, 게임 기능 설정, 파일 시스템&asset 접근 등등)

이런 subsystems를 알아가봅시다잉!

### 

### Subsystem Start-Up and Shut-Down

게임 엔진은 많은 상호작용하는 서브시스템들로 이루어진 복잡한 소프트웨어입니다.

이런 서브시스템들은 엔진이 처음 시작될 때 정해진 순서대로 초기화가 되어야합니다. (의존성이 존재할 수 있으니)

예를 들면, B 매니저가 A 매니저를 참조? 의존? 데이터를 필요로? 한다면, A 매니저를 반드시 먼저 초기화 해야될 것입니다.

종료 순서는 초기화 순서의 반대 방향입니다.

초기화: A => B

종료: B => A

### 

### C++ Static Initialization Order (or Lack Thereof)

대부분의 현대 게임 엔진은 C++로 작성되므로, 엔진의 서브시스템들을 시작하고 종료할 때 C++의 네이티브 초기화/종료 semantics를 활용할 수 있는지 간단히 살펴봅시다.

C++에서는 전역, 정적 객체가 존재합니다. 이 객체들은 진입점(main과 같은)이 호출되기 전에 생성됩니다.

이 때 생성자가 호출되는 순서는 예측 불가능합니다. (인스턴스, 객체, 변수 모두 예측 불가능)

위에서 말했던 것처럼 게임 엔진의 subsystem들은 의존성이 존재하기 때문에 생성과 소멸이 예측불가능하면 안된다.

때문에 전역, 정적 객체로 호출하는 방법은 적합하지 않다.

( 만약 C++가 전역, 정적 클래스 인스턴스들의 생성, 소멸 순서를 제어할 수 있었따면... 싱글톤 인스턴스를 전역으로 정의할 수 있었을 것이고, 그러면 동적 메모리 할당이 필요없어지니 행복했을 텐데...)

### 

### Construct On Demand

하지만 C++의 한 가지 트릭이 있다. (빈틈의 실!)

함수 안에서 선언된 static 변수는 함수가 최초로 호출될 때 생성된다.

그럼 아래와 같이 한다면, 여차저차 static으로 선언이 가능한 것이다.

```
class RenderManager
{
public:
    // 오직 하나뿐인 인스턴스를 반환.
    static RenderManager& get()
    {
        // 이 함수-정적 변수는 최초 호출 시 생성된다.
        static RenderManager sSingleton;
        return sSingleton;
    }

    RenderManager()
    {
        // 의존하는 다른 매니저들을 먼저 시작.
        VideoManager::get();
        TextureManager::get();

        // 이제 렌더 매니저를 시작.
        // ...
    }

    ~RenderManager()
    {
        // 매니저 종료.
        // ...
    }
};
```

하지만 이 방식은 생성 순서는 예측가능하지만, 소멸 순서는 제어할 수 없다.

또한 우리가 언제 get함수를 호출해서 매니저가 언제 생성되는지 예측하기도 어렵다.

그래서 이 방법 또한 좋은 방법은 아니다..

### 

### A Simple Approach That Works

simple is the best라는 말이 있지 않은가!!

그냥 singleton manager 형태를 유지하고, 시작(startup), 종료(shutdown) 함수를 정의하는 방법을 사용해보자

이 함수들이 생성자와 소멸자의 역할을 대신하고, 실제 생성자와 소멸자는 아무것도 하지 않도록 만들자

이렇게 하면 진입점 이후에 프로그래머가 명시적으로 함수(startup)를 호출할 것이고,

생성을 제어할 수 있게된다.

소멸 역시 프로그래머가 명시적으로 함수(shutdown)를 호출할 것이고,

소멸을 제어할 수 있게된다.

```
class RenderManager
{
public:
    RenderManager()
    {
        // 아무것도 하지 않음
    }
    ~RenderManager()
    {
        // 아무것도 하지 않음
    }
    void startUp()
    {
        // 매니저 시작...
    }
    void shutDown()
    {
        // 매니저 종료...
    }
    // ...
};
class PhysicsManager { /* 비슷하게... */ };
class AnimationManager { /* 비슷하게... */ };
class MemoryManager { /* 비슷하게... */ };
class FileSystemManager { /* 비슷하게... */ };
// ...

RenderManager gRenderManager;
PhysicsManager gPhysicsManager;
AnimationManager gAnimationManager;
TextureManager gTextureManager;
VideoManager gVideoManager;
MemoryManager gMemoryManager;
FileSystemManager gFileSystemManager;
// ...
int main(int argc, const char* argv)
{
    // 엔진 시스템들을 올바른 순서로 생성
    gMemoryManager.startUp();
    gFileSystemManager.startUp();
    gVideoManager.startUp();
    gTextureManager.startUp();
    gRenderManager.startUp();
    gAnimationManager.startUp();
    gPhysicsManager.startUp();
    
    // 게임 실행
    
    // 역순으로 소멸
    gPhysicsManager.shutDown();
    gAnimationManager.shutDown();
    gRenderManager.shutDown();
    gFileSystemManager.shutDown();
    gMemoryManager.shutDown();
    return 0;
}
```

이보다 더 우아한 방법들도 있다. 하지만 언제나 단순하게 베스트이다.

그 이유로는

1. 단순하기 구현이 쉽다.

2. 명시적이다. 코드만 봐도 시작 순서를 즉시 알 수 있다.

3. 디버그와 유지보수가 쉽다. 만약 어떤 것이 너무 일찍 시작되거나 너무 늦게 시작되었다면, 코드의 한 줄만 옮기면 된다.