---
title: "[C++/EffectiveC++] #define VS const, enum ,inline"
date: 2024-11-20
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

**부제:** **선행처리자보다는 컴파일러를 더 가까이하자**

#define을 쓰기보다는 const를 사용하는 것을 추천한다.

```
#define ASPECT_RATIO 1.653
```

만약  이렇게 선언하고 오류가 났다면,

**선행처리가자 컴파일러에게 코드를 보내기 전에 ASPECT\_RATIO를 1.653으로 바꿔놓는다.**

**때문에 오류 목록을 봐도 영어 대신 1.653를 만나서 디버깅하기 어려운 상황에 처할 수 있다.**

```
const double AspectRatio = 1.653;
```

오류가 났을 때 변수 명으로 만날 수도 있고 :) + 사본이 한 개만 존재하기 때문에 메모리 측면으로도 좋다고 볼 수 있다. ( 매크로와 다르게)

#### 

#### **주의해야될 점이 있다.**

**1. 상수 포인터 ( contant pointer )**

상수 정의는 대부 헤더파일에서 쓰인다. 이때 포인터는 꼭 const로 선언하고, 포인터가 가리키는 대상도 const로 선언하는 것이 일반적이다.

```
const char * const authorName = "Jang Jae Bum";
```

**2. 클래스 멤버로 상수를 정의하는 경우**

클래스의 상수의 정의는 구현 파일(cpp)에 둡니다. 헤더파일에 두지 않습니다.

**클래스 상수의 초기값은**

해당 상수가 **선언된 시점에서 주어지기** 때문에 **정의에는 상수의 초기값이 있으면 안된다.**

```
class GamePlayer
{
private:
	static const int NumTurns = 5;	// 상수 선언
	int scores[NumTurns];
    ...
};
```

```
const int GamePlayer::NumTurns; //정의
```

나는 정의를 헤더에서 해야겠어!!! 라는 사람들에게 살짝의 트릭을 소개한다.

```
class GamePlayer
{
	enum {NumTurns = 5};
    
	int socres[NumTurns];
    
    ...
}
```

const 보다는 #define에 가깝다.

const 는 주소에 접근가능하지만, #define과 enum은 사용자가 주소에 접근하지 못하게 막아놓았다.

혹시.. #define으로 클래스 상수를 만들 생각은...?

#define은 유효범위가 없다.

애초에 선언도 안될 뿐더러, 된다그래도 어떤 형태의 캡슐화 해택을 받을 수 없다. (접근지정자가 private라도 무의미하다는 말)

아직 #define 매크로의 단점은 끝나지 않았다..!

#define에서는 ()를 꼭 붙혀줘야된다는 말을 많이 들었을 것이다.

```
#define CALL_WITH_MAX(a,b) f( (a) > (b) ? (a) : (b) )
```

이 코드에

```
int a =5 , b = 0;
CALL_WITH_MAX(++a,b);
CALL_WITH_MAX(a++,b);
```

이렇게만 해줘도 a의 증가횟수가 달라진다!

이를 대체하기 위해 여기서는 inline이 등장한다. ( 언리얼에서는 FORCEINLINE입당..ㅎ )

```
template<typename T>
inline void callWithMax(const T& a, const T& b)
{
	f(a > b ? a : b);
}
```

이렇게하면 괄호도, 연산자들도 고민없이 사용할 수 있다.