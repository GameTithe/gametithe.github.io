---
title: "[C++/Effective] 설계 및 선언(1)"
date: 2025-04-16
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### 인터페이스 설계를 제대로 쓰기에는 쉽게 엉터리로 쓰기에는 어렵게 하자

월 / 일 / 년을 입력해야 되는 프로그램이 있다고 하자.

```
class Date
{
public:
	Date(int month, int day, int year) {}
}
```

당연히 아래와 같이 입력하겠지 하하 호호라고 생각하면 안된다는 것이다.

```
Date(01,  31, 2025)
```

이렇게 입력을 해도 오류를 밷지않는 프로그램은 엉터리 프로그램이다.

```
Date(31, 01, 2025)
```

우리는 월 / 일 / 년 형식으로 입력이 오지 않으면 오류는 발생시켜야된다.

아래와 같이 한다면 사용자가 실수할 일은 없을 것이다.

```
#include <iostream>

struct Day
{
	explicit Day(int d) : val(d) {}
	int val;
};

struct Month
{
	explicit Month(int m) :val(m) {} 
	int val;
};

struct Year
{
	 explicit Year(int y) : val(y) {}
	int val;
};

class Date
{
public:
	Date(const Month& m, const Day& d, const Year& y) {}
};

int main()
{
	// Date d( Day(1), Month(1), Year(1));
	// Date d(1,2,3);
	Date d(Month(1), Day(1), Year(1));
		
}
```

이렇게까지 제한을 했지만 13월 이라고 입력할까봐 무섭다면 이런 우아한 방법도 존재한다.

```
class Month
{
public:
	static Month Jan() { return Month(1); }
	static Month Feb() { return Month(2); }
	// ... 
	static Month Dec() { return Month(12); }

private:
	explicit Month(int m) :val(m) {} 
	int val;
};
```

또한 자원 누수도 고려를 해야된다.

Investment라는 class가 존재할 때,

Investment를 생성하고 포인터를 반환하는 함수가 있다고 하자.

```
Investment* createInvestment();
```

이렇게 됐을 때 우리 손으로 delete를 해줘야된다.

이것을 잊으면 자원 누수가 일어나는 것이다.

만약 delete를 2번한다면 그것 또한 사고다...

이런 일을 방지하기 위해서

스마트 포인터를 사용하자.

```
std::shared_ptr<Investment> createInvestment();
```

스마트 포인터는 사용자 지정 destructor(파괴자)를 사용할 수 있기 때문에 cross dll문제 또한 피할 수 있다.

Cross dll을 간단하게 설명하면

A DLL: 생성자 사용

B DLL: destructor사용

이렇게 버전이 다르면 충돌이 이러날 수 있지만, shared\_ptr로 변수를 선언할 때 A DLL의 destructor를 명시적으로 지정하면 Cross DLL 문제를 피할 수 있다는 의미이다.

### 클래스 설계는 타입 설계와 똑같이 취급하자

클래스를 설계할 때에는

1. 문법이 자연스러워야한다.

2. 의미구조(semantics)가 직관적이여야한다.

3. 효율적이여여 한다.

이 3가지를 고려해야된다.

위에서 말한 3가지를 지키는 올바른 설계를 위해 신경써야 하는 것을 알아보자

**새로 정의한 타입의 객체 생성 및 소멸은 어떻게 이루어지게 할 것인가**

생성자, 소멸자 뿐만 아니라 동적할당 문법을 사용할 때에도 신경을 써야된다.

**객체 초기화는 객체 대입과 어떻게 달라야 하는가?**

생성자를 호출해서 초기화하는 것과 대입연사자를 호출하는 것과의 동작을 잘 규명해야된다.

새로운 타입이 가질 수 있는 적법한 값에 대한 제약은 무엇으로 잡을 것인가?

클래스의 데이터 멤버의 몇 가지 조합 값만은 반드시 유효해야스 설계를 제대로 쓰기에는 쉽게 엉터리로 쓰기에는 어렵게 하자

월 / 일 / 년을 입력해야 되는 프로그램이 있다고 하자.

```
class Date

{

public:

 Date(int month, int day, int year) {}

}
```

당연히 아래와 같이 입력하겠지 하하 호호라고 생각하면 안된다는 것이다.

```
Date(01, 31, 2025)
```

이렇게 입력을 해도 오류를 밷지않는 프로그램은 엉터리 프로그램이다.

```
Date(31, 01, 2025)
```

우리는 월 / 일 / 년 형식으로 입력이 오지 않으면 오류는 발생시켜야된다.

아래와 같이 한다면 사용자가 실수할 일은 없을 것이다.

또한 자원 누수도 고려를 해야된다.

Investment라는 class가 존재할 때,

Investment를 생성하고 포인터를 반환하는 함수가 있다고 하자.

Investment\* createInvestment();

이렇게 됐을 때 우리 손으로 delete를 해줘야된다.

이것을 잊으면 자원 누수가 일어나는 것이다.

만약 delete를 2번한다면 그것 또한 사고다...

이런 일을 방지하기 위해서

스마트 포인터를 사용하자.

std::shared\_ptr<Investment> createInvestment();

스마트 포인터는 사용자 지정 destructor(파괴자)를 사용할 수 있기 때문에 cross dll문제 또한 피할 수 있다.

```
#include <iostream>



struct Day

{

 explicit Day(int d) : val(d) {}

 int val;

};



struct Month

{

 explicit Month(int m) :val(m) {} 

 int val;

};



struct Year

{

  explicit Year(int y) : val(y) {}

 int val;

};



class Date

{

public:

 Date(const Month& m, const Day& d, const Year& y) {}

};



int main()

{

 // Date d( Day(1), Month(1), Year(1));

 // Date d(1,2,3);

 Date d(Month(1), Day(1), Year(1));

  

}





이렇게까지 제한을 했지만 13월 이라고 입력할까봐 무섭다면 이런 우아한 방법도 존재한다.



class Month

{

public:

 static Month Jan() { return Month(1); }

 static Month Feb() { return Month(2); }

 // ... 

 static Month Dec() { return Month(12); }



private:

 explicit Month(int m) :val(m) {} 

 int val;

};
```

Cross dll을 간단하게 설명하면

A DLL: 생성자 사용

B DLL: destructor사용

이렇게 버전이 다르면 충돌이 이러날 수 있지만, shared\_ptr로 변수를 선언할 때 A DLL의 destructor를 명시적으로 지정하면 Cross DLL 문제를 피할 수 있다는 의미이다.

### 클래스 설계는 타입 설계와 똑같이 취급하자

클래스를 설계할 때에는

1. 문법이 자연스러워야한다.

2. 의미구조(semantics)가 직관적이여야한다.

3. 효율적이여여 한다.

이 3가지를 고려해야된다.

위에서 말한 3가지를 지키는 올바른 설계를 위해 신경써야 하는 것을 알아보자

**새로 정의한 타입의 객체 생성 및 소멸은 어떻게 이루어지게 할 것인가**

생성자, 소멸자 뿐만 아니라 동적할당 문법을 사용할 때에도 신경을 써야된다.

**객체 초기화는 객체 대입과 어떻게 달라야 하는가?**

생성자를 호출해서 초기화하는 것과 대입연사자를 호출하는 것과의 동작을 잘 규명해야된다.

**새로운 타입이 가질 수 있는 적법한 값에 대한 제약은 무엇으로 잡을 것인가?**

클래스의 데이터 멤버의 몇 가지 규약이 있고 이를 반드시 지켜야하는 속성을 invariant (불변속성)이라고 한다.

 ( ex. month는 1~12 이다 )

이를 생성자, 대입연산자, setter함수는 invariant에 많이 좌우된다.

**기존의 클래스 inheritance graph(상속 그래프)에 맞출 것인가?**

상속을 받는 클래스를 선언한다면, 부모 클래스의 영향을 받을 것이다.

부모 클래스의 함수가 가상함수인가 비가상함수에 따라 자식 클래스의 가상함수의 여부가 정해진다. ( 특히 소멸자가 그렇다 )

**어떤 종류의 타입 변환을 허용할 것인가**

만약 T1타입의 객체를 T2로 implicit(암시적으로)하게 변환하고 싶다면, operator T2 또는 인자 하나를 받는 non-explicit  생성자를 만들어야 할 것이다.

explicit한 변환만 허용하고 싶다면, 변환을 맡는 별도의 함수를 만들되 타입 변환 연산자 혹은 비명시 호출 생성자는 만들지 말아야한다.

explicit, non - explicit  생성자 예시

```
#include <iostream>
using namespace std;

class MyInt1 {
    int value;

public:
    // non-explicit 생성자
    MyInt1(int v) : value(v) {}

    void print() const {
        cout << "value: " << value << endl;
    }
};

class MyInt2 {
    int value;

public:
    explicit MyInt2(int v) : value(v) {}  // 명시적으로만 변환됨

    void print() const {
        cout << "value: " << value << endl;
    }
};

void printMyInt1(MyInt1 mi) {
    mi.print();
}

void printMyInt2(MyInt2 mi) {
    mi.print();
}

int main() {
    printMyInt1(42);  // O 암시적 변환 가능
    
    printMyInt2(42);  // X 암시적 변환 불가능
    printMyInt(MyInt2(42));  // O 명시적 변환은 가능
    return 0;
}
```

더보기

**어떤 연산자와 함수를 두어야 의미가 있을까?**

어떤 함수를 멤버 함수로 둘까

표준 함수들 중 어떤 것을 허용하지 말아야 할까?

private에 어떤 함수에 넣어서 작동되지 않도록...

새로운 타입에 대한 접근권한을 어느 쪽에 줄 것인가?

public, proctected, private, friend class 등등 어떻게 설정할 것인가

선언되지 않은 인터페이스로 무엇을 둘 것인가?

**새로 만드는 타입이 얼마나 일반적인가?**

새로운 클래스를 만드는 것인가? template로 커버 가능한것이 아닌가?를 생각해보자

**정말로 꼭 필요한 타입인가?**

기능 몇 개가 아쉬워서 파생클래스를 새로 뽑고 있다면, 간단히 비멤버 함수라든지 템플릿 몇 개 더 정의하는 편이 낫다.

클래스를 정의한다는 것은 위의 내용들을 모두 고려한다는 의미이다.

### "값에 의한 전달" 보다는 상수객체 "참조자에 의한 전달" 방식을 택하는 편이 대개 낫다

아래와 같은 코드가 있다고 하자

현재 Scan을 할 때 값에 의한 전달을 하고 있다.

Scan을 할 때 얼마나 많은 비용이 들까?

```
#include <iostream>
 
class Person
{
public:
	Person() {}
	virtual ~Person() {};
	std::string name;
	std::string birth;
};

class Student : public Person
{
public:
	Student() {}
	virtual ~Student() {} 
	std::string id; 
	std::string major;
};

void Scan(Student p)
{
	///....
}

int main()
{
	Student s;

	Scan(s);
}
```

p에 s를 할당하기 위해서  복사 생성자가 등장하 것이다.

근데 Student를 생성하기 전에 Person을 생성자를 먼저 호출할 것이다.

벌써 복사 생성자가 2번이 발생했다.

그리고 우리는 string을 Person에서 2개, Student에서 2개 총 4개를 사용중이다.

string 생성자도 4번 발생할 것이다.

이대로 끝인가?

Scan함수가 끝날 때는 각각의 소멸자들을 또 호출할 것이다.

이런 비용을 없애고 싶다면 참조자 전달을 사용하는 것이 좋을 것이다.

const는 사용자에게  값을 바꾸지 않을 것이라는 안심을 주는 것이다.

```
void Scan(const Student& p)
{
	//...
}
```

그럼 class의 사이즈가 작으면 상관없다는 거죠??

라는 생각은 안하겠죠??

우선 class가 계속 커질 가능성이 있으니 그냥 참조자를 사용하는 것이 좋다.

그리고 포인터 1개만 들고 있는 class를 보고 사이즈가 작네 그냥 복사 연산자 쓸게 라고 했을 때

만약 포인터가 가리키고 있는 데이터가 컸을 때는 어쩔거냐..!

깊은 복사를 하게 될 것 이고, 또 다시 엄청난 양의 데이터를 복사야된다.

그러니 그냥 조용하고 참조자 복사를 해라

#### Slicing Problem

또힌 오버헤드를 줄일 수 있을 뿐아니라

slicing problem문제도 해결해줄 수 있다.

아래 코드를 보면서 slicing problem문제도 같이 이해하자

```
#include <iostream>
 
class Window
{
public:
	Window() {}

	virtual void display() { std::cout << "Window" << std::endl; }
};

class WindowWithScrollbars : public Window
{
public:
	WindowWithScrollbars() {}

	virtual void display() { std::cout << "Add ScrollBars"  << std::endl;}
};

void printSystem(Window w)
{
	w.display();
}
int main()
{ 
	WindowWithScrollbars wws;

	printSystem(wws);
	//wws.display();

}
```

printSystem에서 뭐가 출력될 것 같나?

printSystem함수가 호출될 때는 Window class로 복사 생성자가 호출 될 것이다. 생성을 Window로 했으니 Window가 출력될 것이다.

하지만 우리는 WindowWithScrollbars를 만들고 보내지 않았는가...!!! 이렇게 정보 소실이 생기는 것을 slicing problem이라고 한다.

![](https://blog.kakaocdn.net/dna/cfJXTi/btsNnyt5pZC/AAAAAAAAAAAAAAAAAAAAANKDxdBUqM7JBoSycqu3M-QXkl19xYFTPr9va5k_cv72/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=vh7iarGs0ZSZQDbhpyE5Ba1iTZU%3D)

이를 해결하는 방법은 계속 말하고 있지만

참조자 전달이다.

```
void printSystem(const Window& w)
{
	w.display();
}
```

이렇게 한다면 우리는 주소를 전달했을 뿐이다. w는 WindowWithScrollbars로 만들어졌기 때문에 Add ScrollBars가 출력될 것이다.

![](https://blog.kakaocdn.net/dna/qaCnO/btsNnoEXI0u/AAAAAAAAAAAAAAAAAAAAACtEIBqqqjGIojMTvUX1cq_BIgL49XRxchyFti7h28kn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=bidSHgGQ34wBh0sOludzUyQBEPs%3D)

이제 참조자 전달을 활용해야겠죠?