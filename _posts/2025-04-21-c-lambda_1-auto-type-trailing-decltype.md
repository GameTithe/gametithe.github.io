---
title: "[C++] Lambda_1 (auto, type trailing, decltype)"
date: 2025-04-21
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

이번에는 lambda를 알아보기 전에 알면 좋은 문법들에 대해서 소개하겠다.

### 첫 번째는 auto type이다.

auto는 컴파일러가 우변(expression)을 보고 type을 추론하도록 지시하는 타입 추론키원드이다.

이렇게 auto를 사용할 수 있다.

```
int main()
{
	int a = 3, b = 2;

	auto c = a + b; 
	
	return 0; 
}
```

그리고 c를 정수형을 잘 할당했다.

![](https://blog.kakaocdn.net/dna/Tsla7/btsNteJJm7J/AAAAAAAAAAAAAAAAAAAAAD-KLCrbucBUHnPT1p1zMU5JYU691-Rer1EvPvp1YNgo/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Nc2rPnf7wO6tilrAA64yR1LpImc%3D)

### 두 번째는 type trailing이다.

아래와 같이 Add함수가 존재할 때

```
int Add(int a, int b)
{
	return a + b;
}
```

이렇게 변경할 수 있다.

```
auto Add(int a, int b) -> int 
{
	return a + b;
}
```

처음 반환 값을 auto로 설정하고 ->연산자를 통해서 반환 값을 지정할 수 있다.

기존 함수와 type trailing이 다른 점은

type trailing은 함수의 반환자를 params를 보고 결정할 수 있다는 것이다.

그럼 이걸 어디에 사용할 수 있냐...

세번째 문법까지만 배우고 알아보자

(위에처럼 param을 안보고도 return type을 정할 수 있을 때는 type trailing을 사용하지마라)

### 세번째 decltype

decltype의 괄호안에 사용되는 expression에 대한 type을 컴파일러 단에서 결정할 수 있다.

이렇게 i가 int형인 것을 decltype으로 확인하고, j를 int형으로 생성할 수 있다.

```
int main()
{ 
	auto i = 3;
	decltype(i) j;
	j = 4;

	return 0;
}
```

### 위에서 배운 것들을 합쳐보자

아래와 같은 함수의 반환 값을 어떻게 정해줘야 될까?

a + b를 type T로 할 지 U로 할 지 고민이 될 것이다.

```
template<typename T, typename U>
Add_template(T a, U b)
{
	return a + b;
}
```

이런 상황에서 decltype이 생각이 날 것이다.

![](https://blog.kakaocdn.net/dna/bTmGce/btsNqrptsCq/AAAAAAAAAAAAAAAAAAAAAJPYz_10cOOLsBI7RRTF1Bm_58ZDbn-iYdUBrzN-5i27/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=CYqhKcnOgqwKuLxsp%2FVMBF5ZiuM%3D)

하지만 오류가 나는 것을 볼 수 있다.

반환타입을 param전에 설정하고 있다. 하지만 이때는 우리가 a, b를 모르는 상황이다.

param을 보고 return type을 설정해야되는 것이다.

이때 typetrailing을 사용하면 우아하게 풀 수 있는 것이다.

![](https://blog.kakaocdn.net/dna/cGgGSQ/btsNtt0JhRm/AAAAAAAAAAAAAAAAAAAAAPjJbM6aoZcpG-DeaDxRZ1-vjrCIBKv9qz3KID_xcMa_/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=jjkzuL0CwI%2B5DlbwC1eHbCs3VK0%3D)

```
template<typename T, typename U>
auto Add_template(T a, U b) -> decltype(a + b)
{
	return a + b;
}


int main()
{ 
	printf("%d\n",Add_template(1, 2));
	printf("%.2f\n",Add_template(1.2 , 2));
	printf("%.2f\n",Add_template(1.2 , 2.2));

	return 0;
}
```

![](https://blog.kakaocdn.net/dna/kD3Zt/btsNtgU5uBh/AAAAAAAAAAAAAAAAAAAAAM34uFPTNjNFC1Q4hiqTrmV_iwVLhsNCjSgsj-Tu5im7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=RaJdLKbqKnZXmoPLuZh%2FVKFFm%2BM%3D)

마지막으로 다시 한 번 말하지만 auto, decltype을 난사하는 것은 좋은 행동이 아니다.

type이 복잡해서 알기 어렵거나 decltype이 아니면 해결하기 어려울 때만 사용해야된다.( ex template )

### 이제 람다를 사용해보자

아래가 기본적인 형식이다.

```
[]() {}
```

이름없는 함수 람다

람다는 함수 포인터가 아니라 함수 그 자체이다. 각각의 람다에 대해서 유니크한 데이터 타입을 생성한다. 그렇기 때문에 데이터 타입을 특정을 못한다.

이런 상황에서 위에서 배운 auto를 사용하면 된다.

(누누히 말하지만 이와 같이 date type을 알기 어려울 때만 auto를 사용하자) 

```
int main()
{
	auto f = [](int a, int b) { return a + b; }; 
	printf("%d", f(2, 3));
}
```

어떤한 이유 때문에 lamda 함수를 복사해야 된다면, 어떻게 받아 줄 수 있을까?

1. auto

2. decltype

을 사용해서 복사를 할 수 있다.

```
int main()
{
	auto f = [](int a, int b) { return a + b; }; 

	auto g1 = f; 
	decltype(f) g2 = f;

	printf("%d\n", g1(2, 3));
	printf("%d", g2(2, 3));
}
```

### 

### capture list

lambda 함수 안에서 i, j에 접근할 수 있을까?

```
int main()
{
	int i = 1, j = 2; 

	auto f = [](int a, int b) 
	{ 
		return a + b + i; 
	};

	auto g1 = f; 
	decltype(f) g2 = f; 
}
```

lambda도 함수이다. ( Anonymous Function )

함수에서 다른 지역변수에 접근할 수 있었나?

add 함수가 있다고 할 때 main에 있는 지역변수에 접근할 수 있었나?

lamda함수에서도 똑같다. 접근할 수 없다.

아래 이미지 처럼 오류로 표시된다.

![](https://blog.kakaocdn.net/dna/NzVDX/btsNsDXjF8V/AAAAAAAAAAAAAAAAAAAAACoifdhbRBI-bEJl8NuNeoMoZ7f8UySe8WSzkwKO4T97/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=j6IZkd%2BmHzC%2Bh9q8m%2B0jLvTpY%2Bw%3D)

다행히 접근할 수 있는 방법이 있고, 이를 capture list를 사용하면 된다.

```
auto f = [i](int a, int b) 
{ 
    return a + b + i; 
};
```

2개 이상의 변수에도 접근 가능하다.

```
auto f = [i, j](int a, int b) 
{ 
    return a + b + i + j; 
};
```

또한 위의 방법들을 값을 복사하는 방법이다.

우리는 value 복사, ref 복사 두 가지 방법을 안다.

ref 복사도 당연히 존재하고, 사용하는 방법도 동일하다.

```
auto f = [&i](int a, int b) 
{ 
    return a + b + i; 
};
```

그럼 value 복사, ref 복사를 섞어서 사용 가능한가? 당연하다

```
auto f = [i, &j](int a, int b) 
{ 
    return a + b + i + j; 
};
```

그럼 100개를 복사하고 싶어!! 그럼 어떻게 해!!

= 을 넣어주면 모든 지역 변수를 value 복사로 사용할 수 있다

&를 넣어주면 모든 지역 변수를 ref 복사로 사용할 수 있다.

```
auto f = [&](int a, int b) 
{ 
    return a + b + i; 
};
```

```
auto f = [=](int a, int b) 
{ 
    return a + b + i; 
};
```

이것도 가능하다.

모든 지역변수를 value 복사를 하는 i만 ref 복사를 하는 방법

```
auto f = [=, &i](int a, int b) 
{ 
    return a + b + i; 
};
```