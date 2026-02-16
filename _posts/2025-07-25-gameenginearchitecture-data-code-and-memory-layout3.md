---
title: "[GameEngineArchitecture] Data, Code and Memory Layout(3)"
date: 2025-07-25
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **C/C++ 프로그램의 메모리 레이아웃**

C나 C++로 작성된 프로그램은 다양한 메모리 영역에 데이터를 저장한다. 저장이 어떻게 할당되고 C/C++ 변수들이 어떻게 동작하는지 이해하려면, 프로그램의 메모리 구조를 파악해야 한다.

실행 파일은 프로그램이 메모리에 로드될 때의 일부 형태(partial image)만 담고 있다.

일부라고하는 이유는, **실행 중 추가로 메모리를 동적으로 할당받기 때문이다.**

실행 이미지(executable image)는 **세그먼트(segment)** 또는 **섹션(section)**이라 불리는 연속적인 블록들로 구성된다.

운영체제마다 배치 방식이 조금씩 다르고, 심지어 같은 운영체제라도 실행 파일마다 약간 다를 수 있다.

하지만 보통은 다음과 같은 **4가지 세그먼트**로 구성된다

![](https://blog.kakaocdn.net/dna/ndWox/btsPxUpWhcJ/AAAAAAAAAAAAAAAAAAAAAA7uNDNEKTyRjiTkJP9sYwcOUrZqpsCpmAYuzbeScVjt/img.jpg?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=WcXPOsjVgRvmn6VeTRAX%2F6kXFpY%3D)

**1. Text Segment ( Code Semgent )**

프로그램의 모든 실행 가능한 기계어 명령어가 이곳에 저장된다.

함수도 여기에 저장되는 것이다.

**2. Data Segment**

초기화된 글로벌 변수 및 정적 변수가 이 영역에 저장된다.

프로그램이 실행될 때 이미 메모리에 값을 채워 넣을 수 있도록, 초기값이 모두 지정된 상태로 구성된다.

**3.BSS Segment ( Block Started by Symbal)**

이 영역에는 초기화 되지 않은 글로벌 변수 및 정적 변수가 저장된다.

C/C++ 언어는 이런 변수들을 기본적으로 0으로 초기화하도록 정의하고 있다.

링커는 얼마나 많은 바이트를 0으로 채울지에 대한 정보만 저정하고 실제로 0을 저장하지 않는다.

프로그램이 실행되면 운영체제가 해당 바이트 수 만큼 메모리를 확보하고, 0으로 초기화한 후 진입점(main)을 호출한다.

**4. Read-Only Data Segment, rodata**

읽기 전용 상수 데이터가 이곳에 저장된다.

( 정수 상수(const int)는 컴파일러가 기계어 코드에 직접 삽입하므로 text segment에 저장된다.)

static은 변수를 다른 번역 단위에서 숨기기 위해 사용되는데,

함수 안에서의 static 변수는 해당 함수 내에서만 접근 가능하지만, Data 또는 BSS  segment에 저장된다.

```
void readHitchhikersGuide(U32 book)
{
    static U32 sBooksInTheTrilogy = 5; // 데이터 세그먼트
    static U32 sBooksRead;            // BSS 세그먼트
}
```

### **Program Stack**

프로그램이 실행되면, 운영체제는 stack이라 불리는 메모리 영역을 예약한다.

함수가 호출되면, 해당 함수의 stack frame이 이 stack에 push된다.

함수가 종료되면 pop된다.

 stack frame에 뭘 저장할까?

**1. 복귀 주소**

호출한 함수로 돌아가기 위한 주소

**2. CPU 레지스터 상태**

새로운 함수가 레지스터를 사용할 수 있도록, 원래 상태를 저장하고, 비켜주는 것이다.

호출된 함수가 끝나면, 저장된 것을 기반으로 원상태 복구

**3. 지역 변수**

일부는 실제로 CPU 레지스터에 저장되기도 하지만, 대부분은 스택 프레임에 저장된 것처럼 동작한다.

아래의 예시 코드와 그림을 보면 이해가 쉬울 것이다.

```
void c()
{
    U32 localC1;
    // ...
}

F32 b()
{
    F32 localB1;
    I32 localB2;
    c();
    return localB1;
}

void a()
{
    U32 aLocalsA1[5];
    F32 localA2 = b();
}
```

![](https://blog.kakaocdn.net/dna/1ExxM/btsPx2nDyAa/AAAAAAAAAAAAAAAAAAAAAPLo9zxuu1xYbLW_S-4FRRlEe3LZtpTg-gZP7lvaMH67/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=caXJLqKl6lMmj696X2bDSAGI5%2Fo%3D)

### **동적 할당 힙 (Dynamic Allocation Heap)**

프로그램의 데이터는 전역 변수나 정적 변수(global/static variables), 혹은 지역 변수(local variables) 형태로 저장될 수 있다.

전역/정적 변수는 실행 파일 이미지 안의 **data 세그먼트** 또는 **BSS 세그먼트**에 할당되고,

지역 변수는 스택(stack)에 할당된다.

이러한 방식은 모두 **정적 할당(static allocation)**이라고 부른다.

**즉, 메모리의 크기와 구조가 컴파일/링크 타임에 이미 결정된다는 뜻이다.**

하지만 **프로그램이 실행될 때까지 메모리 요구량이 완전히 확정되지 않는 경우가 많다.** 따라서 프로그램은 동적으로 메모리를 할당(dynamic memory allocation)할 수 있어야 한다.

이를 위해, 운영체제는 **각 프로세스마다 별도의 메모리 블록**을 유지한다. 이 블록은 malloc() 또는 Windows의 HeapAlloc() 같은 OS 고유의 함수로부터 메모리를 할당받고, free() 또는 HeapFree()와 같은 함수로 해제할 수 있다. 이 메모리 블록을 **힙(Heap)** 또는 프리 스토어(free store)라고 한다.

## 

## **멤버 변수 (Member Variables)**

C의 struct나 C++의 class는 **관련된 변수들을 하나의 논리적 단위로 묶을 수 있게 해준다.**

하지만 중요한 점은 **클래스나 구조체를 선언하는 것만으로는 메모리가 할당되지 않는다.**

즉, 구조는 **데이터 배치를 설명할 뿐**, 메모리는 그 구조체나 클래스를 **실제로 생성(정의)할 때** 할당된다!

### **클래스 정적 멤버 (Class-Static Members)**

static 키워드는 사용되는 문맥에 따라 다양한 의미를 가진다.

**1. file scpe에서 사용될 때**

현재 .cpp 파일 안에서만 보이게 한다는 의미( 외부 linkage 제한 ) 

**2. function scope에서 사용될 때**

전역처럼 유지 되지만, 해당 함수 안에서만 사용가능

**3. 클래스나 구조체 선언 내부에서 사용될 때**

전역 변수처럼 동작하지만 클래스 소속이다 라는 의미

클래스 내부에서 static이 붙은 멤버 변수는

일반적인 인스턴스 멤버와 달리

**각 객체마다 생성되지 않고, 해당 클래스 전체가 공유하는 단 하나의 변수로 동작한다.**

**정리하면**

**클래스 내부 static 변수는 visibility를 제어하는 것이 아니라,**

**클래스 전체에서 공유하는 멤버라는 특성을 부여하는 것이다.**

**주의사항**

1. name scope도 잊지말자

2. 클내스 내부에서의 static 변수는 선언일 뿐, 메모리를 할당하지 않는다. 실제 메모리는 cpp에서 정의할 때 할당된다.

h

```
class Foo
{
public:
	static string sVarName;
}
Foo::sVarName
```

cpp

```
string Foo::sVarName = "JJB";
```

### **Object Layout in Memory**

자신이 정의한 클래스나 구조체가 메모리에서 **어떻게 배치되는지를 시각화**할 수 있다면 굉장히 유용할 것이다.

이 개념은 대체로 단순하다.

구조체 또는 클래스의 **각 멤버 변수를 수평선으로 구분된 박스로 그려보면** 된다.

```
struct Foo
{
    U32 mUnsignedValue;
    F32 mFloatValue;
    I32 mSignedValue;
};
```

![](https://blog.kakaocdn.net/dna/OvRh8/btsPzCumXYk/AAAAAAAAAAAAAAAAAAAAAFjHMyyN0zVRb7zWagmQZMwfvBFMA9OzD9z6pmoQBYHB/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1wAVtiVhSQwTVwRzLh1NPInMKTI%3D)

```
struct Bar
{
    U32 mUnsignedValue;   // 32bit
    F32 mFloatValue;      // 32bit
    bool mBooleanValue;   // 8bit로 가정
};
```

![](https://blog.kakaocdn.net/dna/J1Bey/btsPyLlgk7Z/AAAAAAAAAAAAAAAAAAAAAKsQsZlg6gpD5VelFWN3r4XNgcqK72bckpx3nd3lXzXK/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2BBY6Ztp1PP4gObgcXb%2BwjMysUnc%3D)

### **정렬(Alignment)과 패킹(Packing)**

작은 크기의 멤버 변수와 큰 멤버 변수가 섞여 있을 때 어떤 일이 벌어질까?

```
struct InefficientPacking
{
    U32 mU1;    // 32비트
    F32 mF2;    // 32비트
    U8  mB3;    // 8비트
    I32 mI4;    // 32비트
    bool mB5;   // 8비트
    char* mP6;  // 32비트 (포인터)
};
```

컴파일러가 가능한 한 **모든 멤버를 빈틈없이 붙여서 저장할 것**이라 예상할 것이다.   
하지만 **대부분의 경우, 컴파일러는 그렇게 하지 않는다.**

대신 컴파일러는 멤버들 사이에 구멍을 남긴다.

![](https://blog.kakaocdn.net/dna/bV82yC/btsPxKnrXoK/AAAAAAAAAAAAAAAAAAAAAEy3DfK3eIycANNNmnDtdY34_E8svncG7Sa9AU5pI5LO/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=92t5uFej5Q%2B0Rknh1sZJqI%2BUadE%3D)

구멍을 만드는 이유는 정렬 때문이다.  
CPU가 메모리를 **정확하고 빠르게 읽고 쓰기 위해서는, 데이터가 자신의 크기에 맞게 정렬된 주소에 있어야 한다.**

**정렬이란**, 객체의 주소가 **그 객체의 크기(또는 정렬 요구사항)의 배수**가 되어야 한다.

정렬 요구사항 예

|  |  |
| --- | --- |
| 1바이트 | 아무 주소나 가능 |
| 2바이트 | 짝수 주소만 가능 (0x0, 0x2, 0x4, ..., 0xE 등) |
| 4바이트 | 4의 배수 주소만 가능 (0x0, 0x4, 0x8, 0xC 등) |
| 16바이트 | 16의 배수 주소만 가능 (0x0 등) |

구조체 전체는 가장 큰 멤버의 정렬 요구를 만족해야 한다. 뒤에 예시에서 알아보자

**정렬해야되는 이유**

많은 최신 프로세서는 **정렬된 주소에만 접근**할 수 있다.

예를 들어, 어떤 프로그램이 32비트 정수(int)를 0x6A341174에서 읽으려 하면

=> 주소가 4의 배수군 => **정상적인 aligned read** (성능 좋음)

반면, 0x6A341173에서 int를 읽으려 하면

CPU는 0x6A341170과 0x6A341174 두 블록을 읽고

=> 필요한 비트를 **마스킹 + 쉬프트 + OR 연산**을 통해 조합

=> 성능 저하 발생

예시를 봐보자

```
struct InefficientPacking
{
    unsigned int mU1;    // 32비트
    float mF2;    // 32비트
    int8_t  mB3;    // 8비트
    int mI4;    // 32비트
    bool mB5;   // 8비트
    char* mP6;  // 64비트 (64bit 환경, 포인터)
};
```

아래의 구조체의 크기가 어떻게 될까?

단순 계산해보면 22바이트이다.

**하지만 출력해보면 32바이트가 나온다. 그 이유는 제일 큰 바이트를 정렬대상으로 삼기 때문이다.**

그림으로 보면 아래와 같이 정렬된다.

![](https://blog.kakaocdn.net/dna/bLQdYb/btsPy0ijpWT/AAAAAAAAAAAAAAAAAAAAAB7dtSnk_4hJcyB0-EyYBIc7-qaEBpINePcRV9R3Czih/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=gGfGLt8obbM51FYSYBN7Bp8%2BtJY%3D)

패딩이 많이 된다... 이것을 해결하기 위해서는

**크기 순으로 배치하면 패딩을 최소화 할 수 있다.**

**또한 컴퓨터에게 패딩을 맡기지 않고, 개발자가 직접 추가하는 것이 더 명확하다.**

```
struct InefficientPacking
{
    char* mP6;  // 64비트 (포인터)
    float mF2;    // 32비트
    int mI4;    // 32비트
    unsigned int mU1;  // 32비트
    int8_t  mB3;    // 8비트
    bool mB5;   // 8비트
};
```

이렇게 했을 때 24바이트로 크기가 많이 줄었다!!

```
struct BestPacking
{
    U32 mU1;
    F32 mF2;
    I32 mI4;
    char* mP6;
    U8  mB3;
    bool mB5;
    U8  _pad[2];  // 명시적 padding
};
```

실습 코드입니다. 직접 확인해보세욤

```
#include <iostream>
 
 
using namespace std;
struct InefficientPacking
{
    char* mP6;  // 64비트 (포인터)
    float mF2;    // 32비트
    int mI4;    // 32비트
    unsigned int mU1;  // 32비트
    int8_t  mB3;    // 8비트
    bool mB5;   // 8비트
}; 
struct MoreEfficientPacking
{
    unsigned int mU1;
    float mF2;
    int mI4;
    char* mP6;
    int8_t  mB3;
    bool mB5;
};
int main()
{    
     
	cout << sizeof(InefficientPacking) << endl;
	cout << sizeof(MoreEfficientPacking) << endl;
}
```

### **C++ 클래스의 메모리 레이아웃**

C++ 클래스는 C 구조체와 비교했을 때, 메모리 레이아웃 측면에서 두 가지 차이점이 있다.

1. 상속

2. 가상 함수

### 상속이 미치는 메모리 구조

클래스 B가 클래스 A를 상속할 경우,  
B의 멤버 변수들은 단순히 **메모리 상에서 A의 멤버들 뒤에 바로 이어서 붙는다.**

![](https://blog.kakaocdn.net/dna/bD4sW8/btsPzVHsJMG/AAAAAAAAAAAAAAAAAAAAADYBqsqv-Q--HXN2gX6U_gNfUpO9mVtAIxfVAp9m7z87/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Z6HlOURiMYjs76mVkwdKPaTCSB8%3D)

단, **정렬 요건(alignment requirements)** 때문에 클래스들 사이에 패딩(padding)이 삽입될 수도 있다.

가상 함수가 미치는 메모리 구조

클래스가 하나 이상의 가상 함수(virtual function)를 포함하거나 상속하게 되면,  
클래스의 메모리 레이아웃에 **추가적인 4바이트(32비트)** 또는 **8바이트(64비트)** 공간이 할당된다.

이 공간은 일반적으로 클래스 메모리 레이아웃의 **맨 앞에 위치**하며,  
이를 **가상 함수 테이블 포인터(vtable pointer)** 또는 **vptr**이라고 부른다.