---
title: "[C++] shared_ptr 구현(0): void* , if(expression), safe_bool idiom, ref count"
date: 2024-11-22
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

구현하기 전에 알아볼 내용들이 있다!

shared\_ptr은 모든 포인터에 대해서 처리를 해준다.

**하지만 실제로 구현을 해보려고 하면 void\*가 문제가 된다!**

### **1. void\***

shared\_ptr을 구현할 때 void 반환은 어떻게 처리될까?

아래와 같이 해주면, shared\_ptr\_traits를 통해서 어떤 타입이던지 reference를 얻어올 수 있게된다.

하지만 void형으로 사용하려고 하면 에러가 생긴다.

```
template<typename T> 
struct shared_ptr_traits
{
	typedef T& reference;
};

shared_ptr_traits<int>::reference Test() //int& Test()
{
	static int i = 0;
	return i;
}
```

void형일 때 문제가 생긴다.

![](https://blog.kakaocdn.net/dna/lNIDo/btsKRlFr6Ws/AAAAAAAAAAAAAAAAAAAAAO2IUF5xSlIwPutUWz_HZnToEBkhJTtQMazHFTr5yiY6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=MTWbLhFW%2BkDCZ4LLQm8BP%2BqLTZg%3D)

**이때 template 특화를 이용**해서, void는 이렇게 따로 처리할 수 있도록 해준다.

```
template<>
struct shared_ptr_traits<void>
{
	typedef void reference;
};
```

### **2. if ( expression)**

C/C++에서는 boolean이 true, false로 사용되지만, 사실은 0과 1, 0과 0이 아닌 수 라고 볼 수 있다.

아래의 코드와 출력창을 봐보자

**1. (i < j)  + 1:** ....??? true + 1이라니,, 아까 말했던 것 처럼 true는 사실 1이다. 그렇기 때문에 출력창 처럼 2가 출력되는 것이다.

**2. if(i < j):** 역시 여기소 i<j 가 0 아니기 때문에 if문을 통과해서 설정한 statement가 실행되는 것이다.

**3. if(-1):** 뭔가 -가 있으니 부정 같아 보이지만, 역시 0이 아닌 수 이기에 설정한 statement가 실행된다.

**4. if("Hello World"):** 문자열은 주소를 반환하는데, 주소가 0일리가 없으니 역시 또 if문이 실행된다.

```
void main()
{
	// if(expression)
	// expression이 참일 때 실행되는 statement를 적어주는 것이다. 
	// 사실은 참이아니라 0이 아니라서이다. 
	int i = 2;
	int j = 3;
	std::cout <<  (i < j) + 1 << std::endl;
	if (i < j)
		std::cout << "Hello ";
	if (-1)
		std::cout << "World" << std::endl;
	if ("Hello World") // 문자열의 주소를 반환 
		std::cout << "JJB";
}
```

![](https://blog.kakaocdn.net/dna/YqXij/btsKS5OFEfR/AAAAAAAAAAAAAAAAAAAAALii9e6qBaVM2jLU_Q2Df1ADFIIh6a3bafK5SXxcefW3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=UYy98v6zKy8UtMDSJ80XZHdwCNk%3D)

그렇다면 오버라이드도 살펴보자

아래와 같이 bool을 오버라이드하면 위에서 계속 말했던 것 처럼 ture = 1이니까,

i = true (1)

1이 출력되는게 이제는 어색하지 않다.

```
class KTest
{
private:
	static const int iStatic = 0;

public:
	operator bool() {
		return true;
	}

};
void main()
{
	KTest t;
	bool i;
	i = t;
	std::cout << i << std::endl;
}
```

![](https://blog.kakaocdn.net/dna/yKuk8/btsKQAQH8EG/AAAAAAAAAAAAAAAAAAAAAJLjLHZRaFa-56LKPnby3BQPEGLR0mvGnQh4jp8LubsF/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=M4u9%2FJ6BN4M4NgKEM6gfqjjkKWs%3D)

이제 조금은 어색하다

int 형과 같이 쓰이고 있다..

하지만 boolean도 사실은 정수형이기에 boolean과 int가 호환이 된다. 그렇기 때문에 1로 잘 출력이된다.

두번 째 사진은 int를 오버라이드 했다. 당연히 int형이니 int형 오버라이드가 사용되서 2가 출력된다.

```
class KTest
{
private:
	static const int iStatic = 0;

public:
	// bool이 정수호환
	operator bool() {
		return true;
	}

	//operator int()
	//{
	//	return 2;
	//}
};
void main()
{
	KTest t;
	//이거 안되야되는데..?
	int i;
	i = t;
	std::cout << i << std::endl;
}
```

![](https://blog.kakaocdn.net/dna/yKuk8/btsKQAQH8EG/AAAAAAAAAAAAAAAAAAAAAJLjLHZRaFa-56LKPnby3BQPEGLR0mvGnQh4jp8LubsF/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=M4u9%2FJ6BN4M4NgKEM6gfqjjkKWs%3D)![](https://blog.kakaocdn.net/dna/cjiInF/btsKRfL9CGF/AAAAAAAAAAAAAAAAAAAAAJUFTDoxCvMDtQfmWpIcrk0zd9pjVWZAGlZrhala5fTM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3jcr7exlWJOGekHPF0yyx71B8jU%3D)

이제 예상이 되겠죠?  
주소나와야겠죠..?

여기 잘 되는 것을 볼 수 있습니다.

![](https://blog.kakaocdn.net/dna/b0PDC0/btsKRhiJGh0/AAAAAAAAAAAAAAAAAAAAADhN_Dvv_cwZ_WV05P_HOC62ht3AbHDiVHaAxnrO2CEX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=66ht92bzKJZ%2BdpG5FYg%2BBCf2MhQ%3D)

그럼 여기서 궁금하게 아래처럼 3개가 다 오버라이드 되고 있으면 어떻게 되나요??

![](https://blog.kakaocdn.net/dna/bizjML/btsKQ71JPqb/AAAAAAAAAAAAAAAAAAAAAK21YSDBf3ZP5HkEwQqEqGhNJkvn92XRGJOHKagWTiCK/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=zYneqzoNI%2BzC%2Fzvcct46ydEFWPk%3D)

![](https://blog.kakaocdn.net/dna/WU5H3/btsKQDGzr4Y/AAAAAAAAAAAAAAAAAAAAABssCmt1h5_3xuscnKEqysHEfF9g6Ty-pjnQUvhHD8sA/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=5Zmk2eB528FZ8OaPk8SMC60zcxo%3D)

당연히 가장 비슷한(?) 것 순서대로 오버라이드 됩니다. boolean은 (boolean-> int -> 주소) 이렇게 되겠죠??

3. safe\_bool idiom

아래의 코드를 빌드 시켜보면, 빌드가 성공적으로 된다. (당연히 실행도 잘 된다.)

```
#include <iostream>
 
class KTest
{
private:
	static const int iStatic = 0;

public:
	// bool이 정수호환
	operator bool() {
		return true;
	}
	
	//operator int()
	//{
	//	return 2;
	//}
	
	//operator const int* ()
	//{
	//	return &iStatic;
	//}
	  
};
void main()
{ 
	KTest t;
	KTest u;


	if(t < u)
		std::cout << "hello" << std::endl;
}
```

(주석 처리한 2가지 형태들도 모두 사용가능하다)

실행되는 이유는 t < u를 보면 t와 u에 대해서 int 호환 타입이 있는 지 확인한다.

근데 boolean도 int화 호환되기 때문에 boolean operator 가 호출이되고,

if( true < true)  => if( 1 < 1 ) => false

이렇게 실행이 되는 것이다.

우리가 생각했을 때는

if(t < u) : 이건 안되야지  
if(t) : 이건 되야지   라고 생각할 것이고,

( operator bool로 평가는 가능하지만 비교는 불가능한 어떤 데이터 타입이여야된다. )

이것을 가능하게 해주는 것이 safe\_bool idiom이라고 볼 수 있다.

share\_ptr 초기에는 이렇게 구현이 되어있었다.

```
	typedef void (KTest::*unspecified_bool_type)();
	
 	operator unspecified_bool_type()
	{
		return &KTest::unspecified_bool;
	}
	void unspecified_bool()
	{

	}
```

typedef void (KTest::\*unspecified\_bool\_type) ():

"void 반환,인자가 없는 함수 포인터를 unspecified\_bool\_type으로 선언할 수 있다"라는 말이다.

그리고 그 함수를 operator oveload해서 멤버 함수의 주소를 반환해준다.

멤버 함수의 주소는 비교할 수 있는 대상이 아니므로

아래의 연산을 막아줄 수 있다.

```
if(t < u)
	std::cout << "hello" << std::endl;
```

현대에는 간단히 처리하고 있다.

explicit 키어드를 붙혀준다면, 명시적으로 bool일 때(bool일 때만) 호출이 되기 때문에 비교연산이 불가능하다.

```
	explicit operator bool() {
		return true;
	}
```

4. Reference Count

아래의 그림과 같이 Delete를 한다면,

1번이 delete를 했을 때, 2번 3번은 Dangling 포인터 신세를 면치못한다... ㅠㅠ

![](https://blog.kakaocdn.net/dna/bqeMA0/btsKR9E7zCk/AAAAAAAAAAAAAAAAAAAAAIF6Aqll444PUfLZhEt_oPQN33vfdR6G1Gqc3vDhjPPu/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=pUkU%2B4hbtm%2BWWbpyfVejWF9r8t0%3D)

하지만 나를 참조하고 있는 객체의 수를 세고 있다면 ? (-> ref count)

ref Count가 0 이 됐을 때만 실제 Delete를 실행시켜준다.

그러면 Dangling 포인트가 되는 상황을 피할 수 있다!~!

![](https://blog.kakaocdn.net/dna/HXAEu/btsKTBUpCuy/AAAAAAAAAAAAAAAAAAAAAJLu7TJijLx4GEXziob_hBOyLEz3mdst3pAj0FgMhKkR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Eyv%2BObY48mj8aDjToYaII8as8X4%3D)

여기까지가 shared\_ptr을 구현할 때 까다로운 것들이었고,   
다음 포스팅에서는 shared\_ptr에서 사용되는 기법들을 알아보겠다.