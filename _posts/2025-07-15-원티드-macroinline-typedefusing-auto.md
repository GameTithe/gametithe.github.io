---
title: "[원티드] Macro/Inline + Typedef/Using + Auto"
date: 2025-07-15
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **Macro**

컴파일 전에 문자를 코드 조각으로 치환하는 전처리 지시문

```
#include <iostream>
#define Square(x) ((x) * (x))

int main()
{
	std::cout << Square(3) << "\n";
}
```

전처리 과정을 밟으면 아래와 같이된다. ( #define은 일단 냅둔다고하더라 )

```
#include <iostream>

#define Square(x) ((x) * (x))
int main()
{
	std::cout << ((3) * (3)) << "\n";
}
```

### 장점

매크로 함수의 호출 구문이 함수의 본문으로 완전히 대체되는데,

이렇게 함수 본문으로 대체되면, 함수의 호출 과정이 사라지기 때문에 성능 상의 이점을 얻을 수 있다.

(함수 호출에 필요한 콜 스택(Call Stack)을 사용하지 않기 때문이다).

### 하지만 가독성이 안좋다는...

그래서 C++로 넘어오면서 macro는 지양하자는 업계

가독성은 개발자들에게는 굉장히 중요한 부분이다. ( 여러 명이서 코딩을하고 다른 사람의 코드를 읽을 줄 알아야하니까 )

(하지만... macro가 안좋긴한데 언리얼의 reflection 기능을 사용하기 위해서는 macro를 뺄 수가 없음.. 그냥 최대한 사용하지말고 버텨 )

### **Inline Keyward**

C에서는 Marco 문법이 C++로 오면서 인라인( in-line ) 함수로 바뀌었다고 보면된다.

하지만 주요하게 다른 것은 실행시점이라고 볼 수 있다.

**macro는 전처리 단계에서 실행되지만,**

**inline keyward는 컴파일러 단계에서 실행된다.**

이 부분이 은근히 크리티컬한게 macro는 일단 바꿔놓고 컴파일러 단계에서 오류가 발생하면 문자가 이미 바뀌어버린 후 해당 문자로 오류를 출력한다.

이게 무슨말이냐하면, 아래의 코드를 보자

Square에서 난 오류인데 0나누 문제라고 로그가 뜬다. 오류 메세지가 내 코드와 매칭이 안된다. 이런 치명적인 상황이 발생한다는 것이다.

```
#include <iostream>

#define Square(x) ((x) * (x) / 0) 
int main()
{
	std::cout << Square(10) << "\n";

	std::cin.get(); 
}
```

![](https://blog.kakaocdn.net/dna/cuHj1Q/btsPiIi8QLI/AAAAAAAAAAAAAAAAAAAAAPvGtb_vYr3JYOX4JT0BIYllSO1Y1SgPoJ4ksZFcGJbh/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KhcAimjq1MEaP1bm%2BWZKCE%2FHCa0%3D)

macro, inline keyward와 같은 inline 함수는 물론 함수를 호출하는 것보다 속도는 빠르다.

왜?

더보기

콜 스택을 사용하지 않기 때문에 실행파일의 속도는 증가 ( code 본문이 길어지면 컴파일하는데 오래걸린다. )

하지만 용량은 더 사용 ( code 본문이 길어지니까 )

속도와 용량은 trade off 관계. 둘 다 만족하는 최적화 기법은 없수

### **단점**

가독성을 해친다.  (위에서 계속 말했으니 패스)

### **typedef / using**

type alias(타입 별칭)으로 내가 새롭게 naming을 해주는 것이다.

typedef이 등장했지만 또 가독성 이슈로 using이 재등장

우리는 using으로 사용하면 된다.

사용법은 아래와 같다. (레거시가 많으니 typedef를 읽을 줄은 알아야한다.)

```
using IntPtr = int*;

typedef int* IntPtr
```

함수 포인터로도 사용이 가능하다.

```
using Fun = int (char, double);
using Fun2 = int(*) (char, double);

typedef int(Fun3)(char, double);
typedef int(*Fun4) (char, double);
```

### **Auto**

auto를 사용하면 변수를 정의할 때 명시적으로 타입을 지정하지 않아도 **컴파일 시점 때** 타입을 추론해주는 키워드이다. 

auto는 값을 보고 자료형을 지정하는 것이기 때문에, 반드시 초기화를 해줘야 한다.

(포인터, 참조는 인식을 못할 때가 있어서, auto\*, auto& 해주는게 좋다)

auto를 설명할 때 **컴파일 시점 때만** 볼드처리했다.

그 이유는

사실 auto도 쓰지 않는게 공식 컨벤션이기도하고.. (그래도 가끔 쓰긴하니까... 읽을 수는 있어야하니까...)

auto를 난사해도 실행 성능에는 영향이 없다는 것을 말하고 싶었기 때문이다.

**컴파일 시점에** 자료형을 추론하는 것이기 때문에 실행파일에서는 자료형이 이미 지정되어있는 것과 동일하다.

이렇게 난사를 해도

```
auto a = 1;
auto b = "Asd";
auto d = 3.14
```

실행파일에서는 이렇게 동작하는 것이다.

```
int a = 1;
const char* b = "Asd";
float d = 3.14;
```

정리하면

Auto를 많이 사용하면 성능에 문제가 된다?

-> NO, 런타임인데 실행할 때 성능 저하는 없다.

그럼 난사하면 되겠네~~

-> 앙?  
  
물론 런타임에 대한 성능 저하는 없다. 완벽히 동일해 근데 근데 근데 근데

가독성이 오마이갓 떙이다.

우리는 1인 개발만 하는게 아니지 않습니까!

여러 명의 개발자들이 모여서 코딩을 하는데, auto를 난사하면 오른 쪽의 값을 정확히 보지 않으면 자료형을 알 수가 없다.

auto 난사는 자제하십시요...

언리얼 코딩 표준에서도 말하고 있죠? :)

![](https://blog.kakaocdn.net/dna/cNpsfm/btsPiKgQYV0/AAAAAAAAAAAAAAAAAAAAAL83-VFpGmF3W5PUXDsgISKUlccaapBw9UHun30wQw68/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hzPGXRWf%2FqH%2F5I0BQdzYk8qTOaw%3D)

여담

더보기

class 멤버 변수 자료형으로 auto를 사용할 수 없다.

(멤버변수를 CLASS에서 바로 초기화하는 것이 등장한지 얼마 안되었다. 원래는 바로 초기화가 안됐음, 그래서 역사적으로 auto를 사용 못해서 지원안하는 듯)

### **기억해둘 것:**

### **1.**

macro 자제해, inline이 낫지 (이친구는 그래도 컴파일단에서 코드 교환이 일어나긴해)

### **2.**

auto 자제해 ( 이 녀석도 컴파일단에서 자료형을 추론한다. )

## **3.**

typedef보다 using을 사용하는 것이 표준이다.