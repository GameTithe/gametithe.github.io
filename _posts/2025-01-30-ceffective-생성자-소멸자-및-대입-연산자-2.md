---
title: "[C++/Effective] 생성자, 소멸자 및 대입 연산자 (2)"
date: 2025-01-30
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **1. 참조 멤버 변수를 다시 재할당할 수 없다.**

```
class Name
{
public:
	Name(  string& name) : myName(name) {}

	string& myName; 
};

int main()
{
	string nameA("a");
	string nameB("b");
	
	Name a(nameA);
	Name b(nameB);

	a = b;

}
```

C++에서 참조자는 원래 자신이 참조하던 객체 이외의 것을 참조할 수 없다!!

근데 이건 되던데요..?

```
	int n = 1;
	int& m = n;

	int k = 2;
	m = k;

	cout << m << endl;
```

이건 참조자를 변경한게 아니라 참조하고 있는 것의 값을 변경한 것이다. n을 출력해보면  n의 값도 바뀌어있을 것이다.

#### **결론: C++에서 참조자는 원래 자신이 참조하던 객체 이외의 것을 참조할 수 없다!!**

**( 만약 부모 클래스에서 대입연사자를 private로 라도 선언했다면, 자식 클래스에서는 암시적 대입연산자를 사용할 수 없게 된다. )**

### 

### **2. 생성자, 복사, 복사 대입연산자 파괴...(ㅎ)**

#### **사본이 없는 객체에 대하여..**

부동산, 자산 등등을 관리하는 것으로 예를 들어 생각하면 사본이 있는 것이 이상하다.

이런 class를 만들 때 어떻게 사본이 생기는 것을 방지할까?

**부모 클래스에서 대입연사자를 private로 라도 선언했다면, 자식 클래스에서는 암시적 대입연산자를 사용할 수 없게 된다는 사실을 이용하면 된다.**

이렇게 private에 복사, 복사 대입 연산자를 만들어주면 된다. 여기서 한 가지 문제!

friend class 에서는 접근이 가능하다는 점... 그러니 **정의(구현)하지 않고 선언만 해준다.**

**그럼 컴파일은 호출을 허용하지만 정의(구현부)를 찾지 못해 링커 단계에서 에러가 발생합니다.**

```
class MyHouse
{
public:
	MyHouse(string& add) : myAdd(add) {}

	string myAdd; 
private:
	MyHouse(const MyHouse&);
	MyHouse& operator=(const MyHouse&);
};
```

![](https://blog.kakaocdn.net/dna/7JhV0/btsL2TmJfu8/AAAAAAAAAAAAAAAAAAAAAFegXvQu8TyWjLC1uqlMk4yNSOyuPnZ8M73j8Y3u_Olt/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=DTqggB%2B2Er28WaLmbxpFpQXB83k%3D)

결론: 컴파일러에서 자동으로 만들어주는 함수를 사용하기 싫다면, private에 선언만 하고, 정의(구현)은 하지 않는다. Uncopyable이라는 baseClass를 생성해서 구현하는 것도 하나의 방법이다.

### 

### **3. 다형성을 가진 기본클래스에서는 소멸자를 가상 함수로 선언하자**

Base class, Derived class있고, Derived가 Base를 상속 받았을 떄..

```
class Base
{
public:
	int a;
   	virtual Printf() { cout << "Hello" << stdl; }
};

class Derived: public Base
{
public:
	int b;
    virtual Printf() { cout << "World" << stdl; } override;
};
```

Derived의 소멸자를 virtual 로 선언하지 않으면 Base가 정상적으로 소멸되지 않고, 메모리 누수가 발생하겠죠?

+ 다형성 또는 상속을 받지 않는 class에는 virtual로 선언하지 맙시다.

만약 클래스가 32비트 환경에서 32비트 크기일 때 virtual 때문에 64비트로 class의 크기가 커질 수 있습니다!

### **4. 예외가 소멸자를 떠나지 못하도록 붙들어 놓자!**

소멸자에서 예외(Exception)이 1번 이상 발생했을 때,

불완전 종료 ( 객체의 정리가 끝나지 않고) , 예기치 않은 동작이 발생할 수 있습니다.

그렇기 때문에 소멸자에서는 예외가 일어나지 않게 만들어야 합니다.

이렇게 예외를 발생시킬 수 있는 함수를 따로 호출을 해야합니다.

```
struct A {
    void CleanUp() noexcept {
        try {
            // 예외가 발생할 가능성이 있는 작업
            DangerousFunction();
        } catch (const std::exception& e) {
            // 예외를 기록하거나 무시
            std::cerr << "Exception caught during cleanup: " << e.what() << std::endl;
        }
    }

    ~A() noexcept {
        CleanUp();
    }

    void DangerousFunction() {
        // 예외 발생시킬 수 도 있어요... 미안
    }
};
```

이렇게 해야지

위험한 함수가 try-catch 블록으로 감싸져 있어 예외를 소멸자에서 예외를 안전하게 처리할 수 있고,

프로그램이 예기치 않게 종료되는 문제를 방지하고, 로그나 대체 작업을 수행할 수 있는 기회를 얻을 수 있습니다!

### **5. 객체 생성 및 소멸 과정 중에는 절대로 가상 함수를 호출하지 마!!!**

아래와 같이 거래시스템을 만들고 있다고 해보자.

BuyTransaction을 사용할 때는 buy로그를, Sell Transactiond을 사용할 때는 sell 로그를 출력하는 코드이다.

근데 우아하게 코딩하고 싶은 마음에 로그를 출력해주는 logTransaction이라는 순수 가상함수를 만들었고,

이를 class에 맞게 override해주었다.

중요한건 이 순수 가상함수를 Transaction class에서 호출을 한 것이다.

Sell Transaction을 만들면 Transaction에서 호출되는 logTransaction이 sell을 출력해주겠지라는 마음인 것이다.

아래의 코드와 같이 말이다...

```
class Transaction
{
public:
	Transaction() 
	{
		//.....
		logTransaction();
	}

	virtual void logTransaction() const = 0; 
};

class BuyTransaction : public Transaction
{
public: 
	BuyTransaction();
	virtual	void logTransaction() const override { cout << "buy" << endl; };

	 
};
class SellTransaction : public Transaction
{
public: 
	SellTransaction();
	virtual	void logTransaction() const override { cout << "sell" << endl; };
	 
};
```

이렇게 코드를 짤 경우,,,, 우리가 예상한 것과 다르게 진행될 것이다... 최악이라고 볼 수 있다.

에러가 나면 감사한 것이다. 에러 없이 우리가 예상한 것과 다르게 흘러갈 수 있기 때문이다.

BuyTransaction으로 예를 들어보겠다.

BuyTransaction의 생성자가 만들어지기 전에 Transacion 생성자가 호출이 될 것이다.

Transaction생성자에 있는 logTransaction은 가상함수이지만 아직 BuyTransaction 생성자가 호출되지 않았다. 그래서 logTransaction함수에게는 가상함수 테이블이 없고, 그렇기 때문에 그냥 Transaction의 함수로서 사용된다.

논리적으로도 이게 옳다고 생각할 것이다.

우리가 예상한 것은 BuyTransaction의 logTransaction이 호출되는 것이지만, 현실은 Transaction의 logTransaction가 호출이 되는 것이다.

그러니 !!! 생성자에서는 절대절대 가상함수를 호출해서는 안된다.

그럼 소멸자에서는요???

소멸자에서도 동일하다, BuyTransaction이 소멸될 때의 순서는 BuyTransaction-> Transaction순으로 소멸된다 (Stack이기 때문에)

Transaction의 소멸자에서 가상함수를 호출했을지라고, BuyTransaction은 이미 소멸자를 호출해서 사라진 상태이기에

어떤 상황이라도 Transaction의 함수를 호출하는 상황이 발생할 것이다....

### **그러니까!! 생성자, 소멸자에서는 가상함수를 호출해서는 안된다!**

그렇다면 위에서 짠 코드를 어떻게 옳바르게 짤 수 있을까

아래의 코드를 봐보자

```
class Transaction
{
public:
	explicit Transaction(const string& logString) 
	{
		//.....
		logTransaction(logString);
	}
	
	// 더 이상 가상함수가 아니다.
	void logTransaction(const string& logString) const
	{
		cout << logString << endl;
	}
};

class BuyTransaction : public Transaction
{
public: 
	BuyTransaction(const string& logString) : Transaction(logString) {};
	
	static const string& createString(const string& log) { return log; }

};
```

이렇게 가상함수를 사용하지 않고, 일반 함수를 사용하지만

파생 클래스에서 필요한 정보는 base class에게 넘겨주는 방식을 사용하면 우아하게 해결할 수 있습니다.

그리고 createString을 static으로 선언한 것에 대해서 더 이야기를 하고 싶은데요

base class에 멤버 초기화 리스가 너무 복잡하다면 유용한 방법입니다.

static으로 선언해서 인자를 만들기 때문에 BuyTransaction이 초기화 됐는지, 안됐는 지를 따질 필요가 없기 떄문이죠 : )

### 

### **6. 대입 연산자는 \*this의 참조자를 반환하게 하자**

여기에 대한 특별한 내용은 없습니다. C++의 관례(convention)라고 생각하면 됩니다.

C++에서는 아래와 같이 여러개의 변수를 초기화하는 코드가 동작합니다.

```
x = y = z = 10;
```

실제로 동작하기 위해서는 아래 와 같이 분석될 것입니다.

```
x =( y = (z = 15));
```

위의 코드가 작동하기 위해서는 대입연산자의 반환값이 참조 연산자로 구현되어 있을 것입니다.

#### **어떤 형태든지 대입 연산자를 구현할 일이 있다면, \*this를 반환하는 관례(convention)를 따릅시다!**

```
class Widget
{ 
//...
	Widget& opertaor= (const Widget& rhs)
    { 
    	//	...
    	return *this;
    }
    
    Widget& operator+= (const Widget& rhs)
    {
    	// ...
    	return *this;
    }
}
```

### **7. operator= 연산자에서는 자기 대입에 대한 처리가 빠지지 않도록 하자**

**자기 대입을 할 일 있나?**

누가 이런 코드를 짜겠어 ㅋㅋ

```
x = x
```

라고 생각할 수도 있지만, 자기 대입이 일어나는 일이 꽤 있다.

아래와 같은 상황도 변수 이름이 다르지만, 가리키고 있는게 같은 대상이면, 자기 대입이 일어난다.

```
a[i] = a[j];
*px = *py;
```

우선 겉보기에는 멀쩡해보이는 대입연산자이다.

하지만 여기서 자기대입을 한다면 어떻게 될까? delete[] pb에서 rhs의 bitmap이 사라지는 것이다.

대입할 대상이 사라지니 아래의 코드는 오류를 일으킬 것이다.

```
class Bitmap
{
public:
	Bitmap();

//...
};
class Widget
{
public:
	Widget();

	Widget& operator=(const Widget& rhs)
	{
		delete pb;
		
		pb = new Bitmap(*rhs.pb);

		return *this;
	}
	Bitmap* pb;
};
```

전통적으로 일치성 검사(identity test)를 통해서 자기 대입 연산자인지 판별을 한다.

```
	Widget& operator=(const Widget& rhs)
	{
    	//자기 대입 연산인지 판별
		if (this == &rhs) return *this;

		delete pb;
		
		pb = new Bitmap(*rhs.pb);

		return *this;
	}
```

위의 방법도 좋지만 만약에 new Bitmap에서 메모리가 부족하다는 사유로 예외가 발생하면 어떻게 될까?

이미 pb를 delete를 시켰지만 새로 할당을 받지 못하는 상황이다....  
다행히도 코드 순서를 바꿈으로서 간단히 해결할 수 있다.

```
Widget& operator=(const Widget& rhs)
{ 
	Bitmap* origin = this->pb;
	pb = new Bitmap(*rhs.pb);
	delete[] origin;

	return *this;
}
```

(참고: new 에서 예외가 발생하면 예외를 던지고, 함수 종료이다. )

하지만 더 좋은 방법이 존재한다!! 최최최최최종이다.

copy and swap이라는 방법이다. 예외 안전성, 자기 대입 안전성 모두 챙길 수있습니다.

제가 과거에 정리했었던.. ㅎ

<https://tithingbygame.tistory.com/122>

[[C++] shared\_ptr구현(1): Non-Throwing-Swap, Copy and Swap

Non-Throwing-SwapCopy and Swap을 위한 base code이다.#include #include templatestruct shared\_ptr\_traits{ typedef T& reference;};templatestruct shared\_ptr\_traits{ typedef void reference;};class KTest{public : int\* px;public: KTest(int\* p) : px(p) { } KT

tithingbygame.tistory.com](https://tithingbygame.tistory.com/122)

```
	Widget& operator=(const Widget& rhs)
	{ 
		Widget temp(rhs);

		swap(*this, temp);

		return *this;
	}
```

### 

### **8. 객체의 모든 부분을 복사하자**

컴파일러가 재공하는 복사 생성자, 복사대입연산자말고, 우리가 따로 만들겠다고하면

컴파일러는 우리가 코드를 잘 못짜도 크게 신경을 안씁니다.. 삐졌을 수도 있죠 하하

아래의 코드를 봅시다. 이렇게 됐을 때 컴파일러는 무언가 잘 못되었다고 이야기해주지 않습니다.

**아래의 복사는 완전 복사가 아닌 부분 복사(partial copy)가 이뤄지고 있습니다.**

```
class Custom
{
public:
	Custom();

private:

	int num; 
};

class ACustom : public Custom
{
public :
	ACustom();

	ACustom& operator=(const ACustom& rhs)
	{
		name = rhs.name;
		return *this;
	}
	string name; 
};
```

우리가 선택한 길이니, 우리가 계속 신경쓰면서 코드를 짜야됩니다.  
그래도 생각보다 간단히 해결할 수 있습니다.

만약 ACustom에서 Custom의 변수에 접근하기는 어렵습니다.( private로 선언되는 경우도 많으니)

그러니 아래와 같이 부모 클래스의 복사대입연산자를 같이 호출해주면 행복하게 해결할 수 있습니다.

```
class Custom
{
public:
	Custom();

	Custom& operator=(const Custom& rhs)
	{
		num = rhs.num;
		return *this;
	}
private:

	int num;
};

class ACustom : public Custom
{
public:
	ACustom();

	ACustom& operator=(const ACustom& rhs)
	{
		name = rhs.name;

		Custom::operator=(rhs);
		return *this;
	}
	string name;
};
```

**항상 완전복사를 신경씁니다!**