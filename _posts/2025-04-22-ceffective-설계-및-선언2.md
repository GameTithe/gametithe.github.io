---
title: "[C++/Effective] 설계 및 선언(2)"
date: 2025-04-22
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **함수에서 객체를 반환해야 될 때 참조자를 반환하려고 하지말자**

지금까지 참조자가 좋다는 말을 많이하니 함수 반환도 참조자로 하려고 들 수 있다.

함수 수준에서 메모리에 새로운 객체를 만드는 방법은 두 가지 이다.

1. stack memory 사용

2. heap memory 사용

( static memory도 있지만 함수 단으로 보면 2가지만 있는게 맞다. )

아래와 같은 코드가 있다고 가정하자.

```
#include <iostream>

class Rational
{
public:
	Rational(int numerator = 0, int denominator = 1) : n(numerator), d(denominator) {}

	friend
	const Rational operator* (const Rational& lhs, const Rational& rhs)
	{ 
		Rational rtn( lhs.n * rhs.n, lhs.d * rhs.d);
		return rtn;
	}

	int GetN() { return n; }
	int GetD() { return d;  }
private: 
	int n, d;
};
int main()
{  
	Rational a(2, 2);
	Rational b(3, 3);

	Rational c = a * b;
	 
	printf("%d ,%d", c.GetD(), c.GetN());

	return 0;
}
```

여기서 아..!

우리는 지금까지 참조자가 아니면 다 벌레...(?) 로 봤으니, 반환값에 있는 값 전달도 벌레다!! 라고 생각할 수 있다.

그리고 반환을 객체로 하니까 생성자, 소멸자가 호출되네? 그것 참 별로구나 라고 생각할 수 있다.

그럼 차근차근 뜯어보자

### 1. stack memory를 사용하면서 참조자 반환 해보자

```
class Rational
{
public:
	Rational(int numerator = 0, int denominator = 1) : n(numerator), d(denominator) {}

	friend
	const Rational& operator* (const Rational& lhs, const Rational& rhs)
	{ 
		Rational rtn( lhs.n * rhs.n, lhs.d * rhs.d);
		return rtn;
	}

	int GetN() { return n; }
	int GetD() { return d;  }
private: 
	int n, d;
};
```

**문제 1**  
생성자를 줄이고 싶었지만 결국 생성자는 호출이 된다.

**문제 2**

함수에서 참조자를 반환했지만, 함수가 끝날 때 객체의 소멸자가 호출이되서 반환한 Rational 객체는 이미 소멸된 객체이다..

문제2번은 굉장히 심각한 문제다. 언제 다른 값이 덮어씌어질 지 모른다. 이런 짓은 하지말도록 하자

### 2. Heap memory를 사용하면서 참조자를 반환해보자

```
class Rational
{
public:
	Rational(int numerator = 0, int denominator = 1) : n(numerator), d(denominator) {}

	friend
	const Rational& operator* (const Rational& lhs, const Rational& rhs)
	{ 
		Rational* rtn = new Rational(lhs.n * rhs.n, lhs.d * rhs.d);
		return *rtn;
	}

	int GetN() { return n; }
	int GetD() { return d;  }
private: 
	int n, d;
};
```

**문제1**

여전히 생성자가 호출되고 있다 ^^

**문제2**

new를 해준 것은 OK, delete는? 아~ 나중에 해줄거야?

그럼 아래와 같을 때는??

```
Rational k = x * y * z;
```

delete[] k를 해줘도, x \* y를 할 때 생긴 객체는 delete를 못하는데?

메모리 누수가 질질ㅈ맂맂ㄹ질ㅈ맂ㄹ리 생기고 있는 모습이다..

### 3. 그럼 static을 사용해볼게...!

```
class Rational
{
public:
	Rational(int numerator = 0, int denominator = 1) : n(numerator), d(denominator) {}

	friend
	const Rational& operator* (const Rational& lhs, const Rational& rhs)
	{ 
		static Rational* rtn = new Rational(lhs.n * rhs.n, lhs.d * rhs.d);
		return *rtn;
	}

	int GetN() { return n; }
	int GetD() { return d;  }
private: 
	int n, d;
};
```

이렇게 static 을 추가하면 처음 한 번만 생성자를 호출하고, 그 이후에는 생성자 호출은 안할거야!!  
너무 행복하잖아~~ 라고 생각하고 있다면 다시 그 생각을 접는 것을 추천한다.

비교연산자를 추가해보자

```
	friend
	bool operator== (const Rational& lhs, const Rational& rhs)
	{
		if (lhs.n == rhs.n && lhs.d == rhs.d)
			return true;
		return false;
	}
```

그리고 아래처럼 연산을 해보면

```
Rational a,b,c,d;

//...

if( (a*b) == (c*d) )
{
	printf("same");
}
```

항상 same이 출력될 것이다...

이해가 안된다고요?

위의 연산은 아래와 같이 진행된다. static을 사용한 순간,,, 하하 알겠죠?

```
if( operator==( operator*(a,b), operator*(c,d) )
```

이제 수긍이 되시겠죠? 필요한 비용은 내면서 코딩합시다...!!!

### **멤버 데이터가 선언될 곳은 private 영역임을 명심하자**

멤버 변수는 private에 선언되어야한다.

public 안된다. protected도 안된다.

### public에 선언하면 안되는 이유

#### 1. 문법적인 일관성

멤버 변수를 public에 선언하게 되면 문법적 일관성을 해치게 된다.

```
class Num
{
public:
    int one;
    int two;
    
    int GetThree() { return three; } 
private:
    int three;
    int four; 
}
```

이런 class가 있다고 할 때, 언제는 변수에 직접 접근할 수 있고, 언제는 함수로 접근해야된다.

이렇게 일관성이 깨지는 문제가 발생한다.

#### 2. read, write 설정

```
class Num
{
public:
    int one;
    int two;
    
    int GetThree() { return three; } 
    int SetThree(int a) {three = a; }
    
    int GetFour() { return four; }
    // NO Setter
private:
    int three;
    int four; 
}
```

priavet에 멤버변수를 선언한다면 write를 헝용하지 않고 read만 허용하는 등 직접 조절할 수 있다.

하지만 public에 멤버 변수를 선언한다면? 이를 통제할 수 없다.

#### 3. 캡슐화

```
class SpeedDataCollection
{
public:
	// ....
	void addValue(int speed) {}

	double averageSoFar() const {}

};
```

속도 평균을 구하는 class가 존재한다고 가정하자.

평균을 구하는 방법이 여러가지가 존재할 것이다.

1. 매초 memory에 저장하다가 함수가 호출되면 그 때 1번 계산하는 방법  
메모리가 많이들지만, 속도는 **빠를** 것

2. 매초 계산하다가 함수가 호출하면 그 때 값을 return하는 방법

속도는 느리지만, 메모리는 적게 들 것

1번이 맞냐, 2번이 맞냐를 논하는게 아니다

public에 averageSpeed를  넣는 것이 아니라**함수를 통해서 평균을 구하도록 해야된다는 것을 말하고 싶은 것이다.**

1. public에 평균 변수를 둔다면,

평균을 구하는 규칙을 바꿀 때 굉장히 번거로울 것이다.

평균 사용하는 곳에서 계속 바꿔줘야하니...

2. 하지만 함수를 통해 접근한다면?

함수 내부 동작만 바꿔주면 함수를 사용하는 모든 곳에 적용된다.

**이렇게 캡슐화는 현재의 구현을 나중에 바꿀 수 있는 권한을 예약하는 셈이다!**

### Protected에 선언하면 안되는 이유

지금까지 이야기한 것과 일맥상통하다.

클래스에서 제거되면 깨길 수 있는 양 과 캡슐화는 반비례한다.

클래스에서 어떤 것을 제거했을 때 깨지는 양이 많으면 캡슐화가 적게 된것이고.

클래스에서 어떤 것을 제거했을 때 깨지는 양이 적으면 캡슐화가 잘 되었다는 의미이다.

그럼 public 멤버 데이터를 지웠다고 생각해보자. 오마이갓 아마 사방에서 오류가 튀어 나올 것이다.

그럼 protected 멤버 데이터를 지웠을 때는?

파생 클래스에서 protected 멤버 데이터를 잘 사용하고 있을 것이고, 이것 또한 파악하기 어려울 정도로 양이 많을 것이다.