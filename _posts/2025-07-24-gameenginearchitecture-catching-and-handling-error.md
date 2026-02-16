---
title: "[GameEngineArchitecture] Catching and Handling Error"
date: 2025-07-24
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

게임 엔진에는 다양한 방식의 오류 감지 및 처리 방식이 있습니다.

게임 프로그래머라면 이러한 방식들의 장단점과 적절한 사용 시기를 이해하는 것이 매우 중요합니다.

### **Types of Errors**

소프트웨어 프로젝트에서는 일반적으로 두 가지 종류의 오류가 존재합니다.

1. 사용자 오류 (User Error)

사용자가 잘못된 입력을 하거나 존재하지 않는 파일을 열려고 하는 등, 프로그램 외부에서 발생

2. 프로그래머 오류 (Programmer Error)

코드 자체의 버그, 프로그래머의 잘못!

(사용자가 누구냐에 따라 경계가 모호하긴 하지만 일반적인 경우로만 생각하자)

### **Handling Errors**

사용자의 오류와 프로그래머 오류는 완전히 다른 방식으로 처리되어야합니다.

사용자 오류

=> 친절하게, 부드럽게 안내하자

프로그래머 오류

=> 메세지 출력 후 계속 진행?? 이건 부적절하죠, 프로그램을 멈추고 디버깅 정보를 제공해줘야한다.

### **Handling Progammer Errors**

프로그래머 오류를 감지하고 처리하는 가장 좋은 방법 중 하나는 에러 검출 코드를 소스에 직접 삽입하고,

에러 발생 시 프로그램을 즉시 중단시키는 것입니다.

**이런 매커니즘을 assertion system이라 부릅니다.**  (본인도 언리얼 엔진을 다룰 때 assert() 로 자주 사용한 방법이있다.  계속 크래쉬가 나서 힘들었던 경험이 있는데 이게 표준이였구나..!)

물론 assertion만이 정답은 아니고, 상황에 맞게 잘 판단해서 사용해야됩니다.

### **Error Return Codes**

**가장 흔한 방식 중 하나는 문제가 감지된 함수에서 실패 코드를 반환하는 것입니다.**

**가장 좋은 방법으로는 enum을 사용하는 것이다.**

```
enum class Error {
    kSuccess,
    kAssetNotFound,
    kInvalidRange,
    // ...
};
```

이렇게 하면 함수의 정상 결과와 오류 결과를 명확히 분리할 수 있으며,  
문제의 원인을 구체적으로 나타낼 수 있습니다.

호출한 함수는 반환된 오류 코드를 검사하고, 즉시 처리하거나 상위 함수로 전달해야 합니다.

### **Exceptions**

간단하고 확실한 방식입니다. ( try catch 문과 같은.. )

**장점**

1.에러 감지와 처리의 분리

2. 코드 작성 간결

**단점**

1. 오류를 감지한 함수가 실제로 문제를 처리할 능력이 없는 경우가 많다.

어떤 함수가 호출 스택 40단계 깊이에서 문제를 감지했는데,

실제 처리할 수 있는 곳은 main()이나 최상위 게임 루프일 경우, 모든 중간 함수가 에러 코드를 일일이 전파해야 한다.

**해결방법:**

throw 를 통해서 예외 객체(exception object)를 던지고, 스택을 역추적하며 try-catch 블록을 찾는다.

매치되는 catch 블록이 있으면 거기서 예외를 처리한다.

1. 오버헤드 증가

함수 프레임이 커지니,

인라인 최적화가 막히거나, 코드 캐쉬 (l-cache) 성능 저하

2. 전역 도입이 필요

예외를 한 곳에서만 써도, 프로그램 전체가 예외를 지원해야됨

3. 흐름 예측이 어려움

예외는 코드에 명시적으로 보이지 않아, goto 보다 위험할 수 있따.

4. 로컬 객체의 예상치 못한 파괴

예외가 발생하면, 중간 함수들고 본인 객체가 언제 파괴될지 보장못함

5. 예외 없는 경우에도 부작용 발생 가능

코드량 증가로 간접적인 성능 저하

**이러한 이유들로 런타임 코드에서 예외처리를 사용안하는 회사들도 더러 존재한다.**

### **Exception and RAII**

RAII 패턴은 예외 처리와 함께 사용되는 경우가 많습니다.

생성자가 자원을 획득하려 시도하고, 자원 획득에 실패하면 예외를 던진다(throw)

이렇게 하면

**객체 생성 후 상태를 확인하는 if 체크 없이,**  
**생성자 호출이 성공적으로 끝났다는 것만으로 자원 획득 성공을 보장할 수 있습니다.**

즉, 생성자가 예외 없이 정상적으로 반환되면,  
해당 자원은 반드시 성공적으로 확보된 상태라는 확신을 가질 수 있다.

그 이후로는 RAII가 주는 자동 해제, 스코프 기반 정리 등 모든 이점을 누릴 수 있다.

**또한 예외 대신 어설션 실패(assertion failure)를 사용해**  
**일부 자원 획득 실패를 개발 중에 빠르게 탐지할 수도 있다.**

### **Assertions**

위에서 계속 말하고 있는 **assertion은 expression(표현식)을 검사하는 코드입니다.**

조건이 참이면 아무일도 일어나지 않고.

조건이 거짓이면, 프로그램이 멈추고, 에러 메세지가 출력되고 가능하면 디버거가 실행됩니다..

언리얼의 assert 함수를 사용해주면 이렇게 프로그램을 멈추고, 에러 메세지를 출력해준다

![](https://blog.kakaocdn.net/dna/oHFq8/btsPv5x6fcg/AAAAAAAAAAAAAAAAAAAAADMNojZOnS8DQJbXRuKOCO2CN701AypUCb4kbp5r3RQV/img.jpg?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=EsEQD8aRA2uCIrsgn1xtdYKDdx0%3D)

assert는 코드가 정상적으로 작동, 유지 되는지 확인해주는 좋은 함수이다.

하지만 출시 전에는 성능 확보를 위해서 제거하기도 한다.

(일반적으로 assertion은 디버그 빌드에서만 활성화 되도록 구성된다.)

assert 구현 예시이다.

```
#if ASSERTIONS_ENABLED

// 디버깅 중단을 위한 인라인 어셈블리 (CPU마다 다름)
#define debugBreak() asm { int 3 }

#define ASSERT(expr) \
  if (expr) { } \
  else { \
    reportAssertionFailure(#expr, __FILE__, __LINE__); \
    debugBreak(); \
  }

#else
#define ASSERT(expr) // 비활성화 시 아무것도 하지 않음
#endif
```

**assertion 사용시 주의 사항**

1. 프로그래머 오류를 처리하는 용도로만 사용할 것

2. 사용자 오류에는 절대 사용 X

3. assertion이 실해하면 게임은 반드시 멈춰야한다.

### **Complie Time Assertiosn**

지금까지 다룬 ASSERT()는 모두 런타임에서만 조건을 확인한다.

그 의미는 프로그램이 실행되어야하고, 해당 코드 경로가 실행되어야만 조건이 검사된다.

**하지만 어떤 조건은 컴파일 타임에 이미 판단이 가능한 경우가 있다.**

**그런 경우 static\_assert를 사용하면 된다.**

```
struct NeedsToBe128Bytes {
    U32 m_a;
    F32 m_b;
    // ...
};

static_assert(sizeof(NeedsToBe128Bytes) == 128, "wrong size");
```

과연 이게 어떻게 가능할까??

**1/0 을 매크로로 만들어주면된다. (와우.. 이런 방법이..)**

```
#define _ASSERT_GLUE(a, b) a ## b
#define ASSERT_GLUE(a, b) _ASSERT_GLUE(a, b)
#define STATIC_ASSERT(expr) \
    enum { ASSERT_GLUE(g_assert_fail_, __LINE__) = 1 / (int)(!!(expr)) }

STATIC_ASSERT(sizeof(int) == 4);    // 통과
STATIC_ASSERT(sizeof(float) == 1);  // 실패
```