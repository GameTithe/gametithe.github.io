---
title: "[GameEngineArchitecture] Data, Code and Memory Layout(2)"
date: 2025-07-25
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **Translation Units Revisited(번역 단위 다시보기)**

C/C++ 프로그램은 번역 단위(translation unit)로 구성된다.

.cpp 파일 하나가 **번역 단위**가 되며, 컴파일러는 이 파일을 **하나씩 따로 번역**해서 오브젝트 파일(.o, .obj)을 만든다.

이 오브젝트 파일은 해당 **.cpp 파일에 정의된 함수의 기계어 코드, 전역 변수, static 변수 등을 포함한다.**

동시에 **다른 .cpp 파일에 정의된 외부 함수나 전역 변수**에 대한 미해결된 참조(unresolved references)도 남아 있게 된다.

### 

### **링커(Linker)의 역할**

컴파일러는 오직 **하나의 번역 단위만**을 볼 수 있기 때문에,  
외부 참조에 대해서는 **존재할 거라 믿고** 처리한다. 이 미해결 참조들을 **해결하는 게 링커의 역할**이다.

링커는

1. 모든 오브젝트 파일을 읽고,

2. 그 안에 있는 함수, 전역 변수, static 변수들을 연결하여,

3. 최종 실행 파일을 생성한다.

### 링커가 발생시키는 두 가지 오류

1. 정의를 못 찾음 => unresolved symbol 에러

2. 이름이 중복된 정의가 여러 개 있음 => multiply defined symbol 에러

### 

### **선언 vs 정의 (Declaration vs Definition)**

C/C++에서는 **모든 함수와 변수는 선언되거나 정의되어야만 사용 가능**하다.  
이 둘의 차이를 명확히 알아야 한다.

#### 선언 (Declaration)

함수나 변수의 **존재를 컴파일러에게 알리는 것이다.**이름과 **자료형/시그니처 정보만 제공한다.**

**메모리는 할당되지 않는다.**

```
extern int max(int a, int b);   // 함수 선언
extern int gValue;              // 변수 선언
```

#### 정의 (Definition)

함수나 변수에 대해 **실제 메모리를 할당하거나 구현 내용을 제공하는 것이다.**

프로그램 내에서 **유일하게 존재해야한다.**

```
int max(int a, int b) { return (a > b) ? a : b; } // 함수 정의

int gValue = 42;      // 변수 정의
```

### **Multiplicity of Declararions and Definitions (중복 선언과 중복 정의)**

C/C++ 에서는 동일한 선언은 여러번 가능합니다. 하지만 동일한 정의는 단 하나만 존재해야 합니다.

하나의 .**cpp 파일에 두 개 이상의 정의가 있는 경우**

 => 컴파일 오류

**서로 다른 .cpp 파일에 동일한 정의가** 있을 경우

=>컴파일러는 각 .cpp파일만 독립적으로 처리하기 때문에 컴파일은 문제를 인식하지 못한다.

=> 링커가 multiply defined symbol 에러를 발생시킨다.

**일반적으로는 정의를 헤더 파일에 두면 위험험한 이유이다.**

cpp파일에서 동일한 헤더를 #include하면 동일한 정의가 여러번 반복되서 링크에러가 발생한다.

### 예외!

**inline 함수는 호출하는 곳마다 복사된 기계어 코드가 삽입되므로(컴파일러가 해줌) 링커가 다중 정의로 간주하지 않는다.**

컴파일러가 inline을 처리하려면, **h에 선언/정의가 전부 존재해야된다. cpp랑 나눠져있으면 일반 함수 선언으로 보고 inline화를 안시켜준다.**

(inline은 컴파일러에세게 추천서를 써주는거지, inline으로 처리할지 안할지는 컴파일러가 알아서 처리할 것이다.

=> 강제로 바꾸고 싶다면 \_\_forceinline이라는 키워드도 존재하긴 한다.)

```
// 제대로 된 인라인 정의
inline int max(int a, int b) {
    return (a > b) ? a : b;
}

// 선언만 존재하므로 인라인 불가능
inline int min(int a, int b);
```

### **Templates and Header Files**

**template도 inline함수처럼 정의가 모든 번역 단위에서 보여야한다.**

즉, 템플릿 함수/클래스 선언과 정의를 모두 헤더에 써야한다.

**.cpp에 정의를 숨겨두면 다른 .cpp에서 사용할 때 정의가 안보이므로 컴파일 에러 발생**

=> 이 말로 유추가능한건 template도 컴파일러가 처리하니까 그런건가? 라고 생각할 수 있다.

=> 실제로 맞음, 컴파일러가 처리해준다..

### **Linkage**

모든 C/C++ 정의는 Linkage라는 속성을 갖는다.

(쉽게 설명하면 다 변수/함수가 다른 파일에서도 볼 수 있냐?

Yes: linkage 있음, No:linkage 없음)

#### **external linkage (외부 링크)**

기본 설정이다. 다른 번역 단위에서 접근 가능하다.

링커가 cross-reference 를 허용한다.

### **internal linkage (내부 링크)**

정의된 파일 내에서만 겁근 가능하다.

static 키워드를 사용해서 설정한다.

예시 정리

foo.cpp

```
U32 gExternalVariable;           // 외부 링크
static U32 gInternalVariable;    // 내부 링크

void externalFunction() {}       // 외부 링크
static void internalFunction() {} // 내부 링크
```

bar.cpp

```
extern U32 gExternalVariable;     // 외부 변수 선언

static U32 gInternalVariable;     // foo.cpp와 무관한 별개 변수
static void internalFunction() {} // foo.cpp와 무관한 별개 함수

void externalFunction() {}        // XX 중복 정의 → 링커 오류!
```

#### **선언은 링크 속성이 없다.**

**기술적으로 선언은 링커가 추적할 대상 (메모리 공간)이 없기 때문에 linkage 속성도 없다. 그래서 다중 선언도 허용된다.**

하지만 실무에서는 간단히 "선언은 internal linkage처럼 동작"한다고 말하기도 한다.

.h 파일에 선언을 넣어도 .cpp파일마다 각자 내부 복사본을 갖는 것과 같다.

#### **인라인 함수는 내부 링크처럼 동작**

그래서 인라인 함수는 **헤더에 정의해도 다중 정의 에러가 나지 않는다.**

=> 각 번역 단위가 그 함수의 개별 복사본을 갖기 때문

=> 마치 static 함수처럼 내부 링크를 가지는 셈이다.

### 

### 

###