---
title: "[C++] shared_ptr구현(2): 구현시작"
date: 2024-11-25
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

**생성자, 복사생성자, 복사연산자, release, swap, reset, 소멸자  순서로 구현을 해보겠습니다.**

스마트포인터에는 기본적으로 4가지고 구성이 되어있다.

this\_type: 본인 타입

value\_type: 값(대상이 되는 타입)

pointer: row pointer (\* 로 쓰이는 포인터)

reference: pointer의 reference

```
#include <iostream>
#include <vector>
#include <algorithm>  

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

template<typename T>
class my_shared_ptr
{
public:
	typedef my_shared_ptr<T> this_type;
	typedef T value_type;
	typedef T* pointer;
	typedef typename shared_ptr_traits<T>::reference reference;

private:
	T* px;
	int* pn;

public:

};



void main()
{

}
```

### **생성자**

**(weak\_ptr은 생각하지 않고 만들었습니다.)**

우리가 알듯이 shared\_ptr은 refCount를 사용한다.(이전 글에서 포스팅했습니다.) 그렇기 때문에 nullptr가 아니면 refCount를 늘려주는 코드입니다.

```
	my_shared_ptr(T* p = nullptr) :px(p), pn(nullptr)
	{
		// 실제로는 ref count가 weak ptr, shared_ptr 따로 있다.
		if (px != nullptr)
		{
			pn = new int;
			*pn = 1;
		}
	}
```

### **소멸자 , release**

**소멸자:**

release를 호출한다. 

**release:**

px에 값이 있고 pn(refCount)가 1보다 크거나 같으면, pn을 1줄인다.

pn을 줄였더니 0이 되면 ( 아무도 px를 참조하지 않는다. ) px, pn을 동적할당 해제시킨다.

px,pn은 nullptr (이 부분은 어떤 조건없이 실행된다.)

```
~my_shared_ptr()
{
	release();
}

void release()
{
	if (px != nullptr && *pn >= 1)
	{
		(*pn)--;
		if (*pn == 0)
		{
			delete px;
			delete pn;
		}
	}
	px = nullptr;
	pn = nullptr;
}
```

### **복사생성자, 복사연산자**

**복사생성자:**

값할당 + refCount 늘리기. 간단합니다.

**복사연산자:**

주석으로 처리된 부분이 정직하게(?)으로 구현하는 방법이다

**하지만 우리는 copy-and-swap방법을 이전에 글에서 배우고 왔으니! **조금 더 우아하게 구현할 수 있다.****

**(자연스럽게 RAII 기법까지 사용되어지는~)**

그래도 간단히 설명하면

this\_type(rhs): rhs로 임시객체를 만들고

임시객체와 \*this가 swap을 한다.

그럼 \*this에는 원하는 값이 복사가 되었을 것이고, 임시객체는 operator가 끝나면 소멸자를 호출하면서 자연스럽게 사라진다.

```
	my_shared_ptr(const my_shared_ptr<T>& rhs)
	{
		px = rhs.px;
		pn = rhs.pn;
		if (px != nullptr) (*pn)++;

	}
    
    
	my_shared_ptr<T>& operator=(const my_shared_ptr<T>& rhs)
	{
		/*release(); 
		px = rhs.px;
		pb = rhs.pn;

		if (px != nullptr)
		{
			(*pn)++;
		}*/

		this_type(rhs).swap(*this); // copy-and-swap idiom  
		return *this;
	}
```

### **swap, reset**

**swap:**

std::swap을 사용해서 값, refCount를 교체해주자.

std::swap은 Non-Throwing-Swap을 가능하게 해주기 때문에 믿고 쓰면 된다.

(move로 성능 최적화, exception 처리)

**reset:**

정직하게 구현하는 법은

본인을 release하고, 받은 \*p로 값을 초기화하고, pn을 1로 초기화하는 방법이다.

**이것 또한 copy-and-swap방법으로 우아하게 구현할 수 있다.**

**포인터 p를 가지고 있는 my\_shared\_ptr(임시객체)**을 만든다. 그리고 **\*this와 swap**을한다.

그러면 \*this는 p로 만들어진 my\_shared\_ptr을 가지고 있고, 임시객체는 reset이 끝나면서 소멸자를 호출시키고 동적할당 해제가 될 것이다.

```
void swap(my_shared_ptr<T>& rhs)
{
	std::swap(px, rhs.px);
	std::sawp(pn, rhs.pn);
}
void reset(T* p = nullptr)
{
	//release();
	//px = p;
	//pn = nullptr;
	//if (px != nullptr)
	//{
	//	pn = new int;
	//	*pn = 1; 
	//}

	this_type(p).swap(*this);
}
```