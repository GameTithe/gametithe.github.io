---
title: "[C++] shared_ptr구현(1): Non-Throwing-Swap, Copy and Swap"
date: 2024-11-23
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

Non-Throwing-Swap

Copy and Swap

을 위한 base code이다.

```
#include <iostream>
#include <vector>

template<typename T>
struct shared_ptr_traits
{
	typedef T& reference;
};

template<>
struct shared_ptr_traits<void>
{
	typedef void reference;
};

class KTest
{
public	:
	int* px;

public:
	KTest(int* p) : px(p) { }
	 
	KTest(const KTest& rhs)
	{
		px = new int;
		*px = *rhs.px;
	}
	KTest& operator= (const KTest& rhs)
	{
		Release();
	
		px = new int;
		*px = *rhs.px;
	
		return *this;
	}
	~KTest()
	{
		Release();
	}
	
	void Release()
	{
		if (px != nullptr)
		{
			delete px;
			px = nullptr;	
		}
	}

	int GetData() const
	{
		return *px;
	}

	void swap(KTest& rhs)
	{ 
		KTest t = *this;
		*this = rhs;
		rhs = t;
	}
}; 
void main()
{  
	KTest t(new int(2));
	KTest u(new int(3));
 

	std::cout << u.GetData() << std::endl;
}
```

### **Non-Throwing-Swap**

여기서 중점으로 볼 부분은 Swap이다.

```
	void swap(KTest& rhs)
	{
		KTest t = *this; //복사생성사
		*this = rhs;     //복사대입연산자
		rhs = t;     
	}
```

큰 문제가 없는 코드이지만, 몇가지 아쉬운 점이있다.

**1.** **Swap이 호출되면, 복사생성자, 복사대입연산자가 호출될 것이다. => 성능을 더 최적화 할 수 있을 것이다.**

**2. 동적할당할 때 exception이 일어나지 않는다는 보장이 되지 않는다.**

**이 부분을 해결해준 함수가 std::swap 함수이다. ( #include <algorithm> 해야됩니다. )**

아래는 std::swap의 구현 방식입니다.

![](https://blog.kakaocdn.net/dna/bmi3eg/btsKVaphfLW/AAAAAAAAAAAAAAAAAAAAAIkDaDua1WAWDJqFdSTYaDcYefE4fXleYO-ayh7JZX5n/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=w65EmZ8Q9SMcwJgljHCbmAn3bnc%3D)

이렇게 move연산자를 이용해서, 불필요한 복사를 줄일 수 있다.

 noexcept로 예외가 일어나지 않음을 보장한다.

그렇기 때문에 Swap은 아래와 같이 구현하자.

```
void swap(KTest& rhs)
{
	//KTest t = *this;
	//*this = rhs;
	//rhs = t;

	std::swap(px, rhs.px);   
}
```

### **copy and swap idiom (temparay object and swap)**

대입연사자를 잘 보면된다.

원래는 아래와 같이 구현이 되어있지만,

위에서 배운 swap을 사용하면 더 효율적으로 구현할 수 있다.

```
class KTest
{

public:
	typedef KTest this_type;
    
public: 
	KTest(int* p) : px(p) { }
    
    
	KTest& operator= (const KTest& rhs)
	{
		Release(); 
		px = new int;
		*px = *rhs.px; // copy	 
	}
    
    ...
    
}
```

swap을 사용하면 아래와 같이 바꿀 수 있다.

```
class KTest
{

public:
	typedef KTest this_type;
    
public: 
	KTest(int* p) : px(p) { }
    
    
	KTest& operator= (const KTest& rhs)
	{
		this_type(rhs).swap(*this);
		return *this;
	}
    
    ...
    
}
```

우선 this로 사용하기 위해서 본인 class형으로 typedef를 만든다.

```
typedef KTest this_type;
```

코드가 어려울 수 있으니 차근차근 설명해보겠다.

```
this_type(rhs).swap(*this);
```

this\_type = KTest라고 보면된다.

this\_type(rhs)는 **rhs와 동일한 값을 가진 임시객체 1개를 만들어준 것이다.**

**그리고 임시객체와 \*this가 swap을 한 것이다.**

this\*와 임시객체과 바뀌게 되는 것이다.

**대입연산자가 종료되면서** **임시객체의 소멸자가 호출**되면서

임시객체가 가리키고 있던 \*this 값들이 사라질 것이고, **\*this는 임시객체가 준 데이터를 잘 가지고 있을 것이다!**  
  
완변한 swap이다!

위의 방법을 RAII방식이다!

**RAII**  
**객체가 명시적으로 release하지 않아도**   
**생성자, 파괴자가 자동으로 호출되는 특징을 이용해서, 자동으로 memory release를 해주는 방식이다.**

**RAII와 GC를 비교한 글이다.**

<https://tithingbygame.tistory.com/123>

[[C++] RAII 그리고 Garbage Collector

https://stackoverflow.com/questions/44325085/raii-vs-garbage-collector RAII vs. Garbage CollectorI recently watched a great talk by Herb Sutter about "Leak Free C++..." at CppCon 2016 where he talked about using smart pointers to implement RAII (Resource

tithingbygame.tistory.com](https://tithingbygame.tistory.com/123)

**다음번에는 shared\_ptr 구현에 진짜로 들어가보겠다!**