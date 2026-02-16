---
title: "[C++/Effective] 생성자, 소멸자 대입연산자 (1)"
date: 2025-01-21
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

C++의 변수 초기화 보장에 대한 규칙은 조금 복잡하다.

아래와 같이 선언했을 때

```
int x;
```

x가 0으로 보장받을 때도 있고, 아닐 때도 있다.

외우기에는 복잡한 감이있다. 일반적인 사항부터 정리하면

**C++에서 C부분만 쓰고있으며, 초기화에 런타임 비용이 소모될 수 있는 상황이라면 값이 초기화된다는 보장이없다**.

배열(C++에서의 C부분)은 항상 초기화된다는 보장이 없지만, vector(C++의 STL부분)은 초기화 보장을 갖게 되는 이유이다.

이렇게 여러 복잡한 규칙들이 있다. 그러니 그냥 마음편이 모두 초기화를 해서 사용하면 마음이 편하다.

초기화를 할 때 대부분의 상황은 모두가 잘 알고있고 옳은 방법일 것이다.

```
int x = 0;
const char* text = "Hello, World" 

double d;
std::cin >> d; // 립력 스트립에서 읽음으로 std::cin으로 초기화 수행
```

하지만 많은 사람들은 "대입"과 "초기화"를 혼동해서 사용하고 있다.

아래의 예시를 보자

```
class PhoneNumber { /* ... */};
class ABEntry
{
public:
	ABEntry(const std::string& name, const std::string& address, const std::list<PhoneNumber> phones)
	{
		theName = name;
		theAddress = address;
		thePhones = phones;
		numTimesConsulted = 0;
	}
private:
	std::string theName;
	std::string theAddress;
	std::list<PhoneNumber> thePhones;
	int numTimesConsulted;
};
```

위와 같이 했을 때, 우리가 원하는 값을 잘 가지고 실행될 것이다. 하지만

**C++ 규칙에 의하면 어떤 객체이든 그객체의 데이터 멤버는 생성자의 본문이 실행되기 전에 초기화되어야 한다고 명기되어 있다.**

위의 방법은 "초기화"가 아니라 "대입"이다.

theName, theAddress, thePhone의 초기화는 이미 지나가고 대입을 하고 있을 것이다. (numTimeConsulted는 기본제공 타입의 데이터 멤버이기 때문에 대입되지 전에 초기화가 된다는 보장은 없다.)

아래의 방법인 **멤버 초기화 리스트**를 사용하면 "대입"이 아닌 "초기화"를 할 수 있다.

```
class PhoneNumber { /* ... */};
class ABEntry
{
public:
	ABEntry(const std::string& name, const std::string& address, const std::list<PhoneNumber> phones) : theName(name), theAddress(address), thePhones(phones), numTimesConsulted(0)
	{
	}
private:
	std::string theName;
	std::string theAddress;
	std::list<PhoneNumber> thePhones;
	int numTimesConsulted;
};
```

기본 생성자를 호출 후에 복사 대입 연산자를 연달아 호출하는 이전의 방법보다 복사 생성자를 한 번 호출하는 후자가 더 효율적이다. 어쩔 때는 훨씬 더 그렇다.

만약 변수들을 기본생성자로만 초기화 하고 싶을 때에도 멤버 초기화 리스트를 사용해서, 인자를 넘겨주지 않고 초기화하는 습관을 들이자

```
class PhoneNumber { /* ... */};
class ABEntry
{
public:
	ABEntry(const std::string& name, const std::string& address, const std::list<PhoneNumber> phones) : theName(), theAddress(), thePhones(), numTimesConsulted(0)
	{
	}
private:
	std::string theName;
	std::string theAddress;
	std::list<PhoneNumber> thePhones;
	int numTimesConsulted;
};
```

C++ 초기화는 변덕스럽다는 이야기를 하고 있었는데, 어떤 컴파일러에서도 고정된 규칙이있다.

1. 기본 클래스는 파생 클래스보다 먼저 초기화 된다.

2. 클래스 데이터 멤버는 그들이 선언된 순서대로 초기화 된다.

ABEntry로 예를 들면 초기화 되는 순서는 theName -> theAddress -> thePhones -> numTimesConsulted이다.

순서로 인한 버그를 방지, 잘 찾기 위해서는 초기화 리스트 순서도 선언 순서대로 해주자.

마지막으로 다룰 내용은

비지역 정적 객체(non-local static)의 초기화 순서는 개별 번역 단위(tranlation unit)에서 정해진다!

비지역 정적 객체(non-local static)의 초가화 순서는 정해져 있지 않다!

이런 내용이다...

static object는 자신이 생성된 시점부터 프로그램이 끝날 때까지 살아있는 객체를 일컫는다.

static object의 범주에는

1. 전역객체

2. 네임스페이스 유효범위에서 선언된 객체

3. 클래스 안에서 static으로 선언된 객체

4. 함수 안에서 static으로 선언된 객체

5. 파일 유효 범위에서 static으로 선언된 객체이다.

여기서 함수안에서 static으로 선언된 객체 4번은 local static object이고, 나머지는 non-local static object이다.

non-local static object간에는 어떤 것이 먼저 초기화 될 지 보장되지 못한다.

이를 보장하기 위해서는, 보장해야만하는 상황에서는 함수를 사용해서 순서를 보장한다. (local static object는 초기화 순서가 보장이 되기 때문에) singleton pattern의 전형적인 방식이다.

```
class FileSystem { 
public:
	/* ... */
	std::size_t numDisks() const;
	/* ... */ 
};

FileSystem& tfs()
{
	static FileSystem fs;
	return fs;
}

class Directory { Directory();/* ... */ };

Directory::Directory(params)
{
	/*...*/

	std::size_t disks = tfs().numDisk();

	/*...*/
}
Directory& tempDir()
{
	static Directory td;
	return td;
}
```

이렇게 객체를 초기화하고 참조자를 반환해준다면 초기화가 되지 않아서 오류가 생길일은 없습니다. 최소한 싱글 스레드에서는...

요약하면

1. 멤버가 아닌 기본제공 타입 객체는 여러분의 손으로 직접 초기화하기

2. 객체의 모든 부분에 대한 초기화에는 멤버 초기화 리스트를 사용한다.

3. 별개의 translation unit에 정의된 non-local static object에 영향을 끼치는 불확실한 초기화 순서를 염두하면서 프로그램을 설계해야된다.