---
title: "[C++] PerfectForwarding(5): std::forward"
date: 2024-11-20
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

![](https://blog.kakaocdn.net/dna/cdsrDj/btsKPVMgBdS/AAAAAAAAAAAAAAAAAAAAAP1C4eNusWsgjrS-JeILKD4T6cCHBS8M7OwjCFMWyMWZ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=rnnOiKLEs5MIZiOH2%2F11REeqIj4%3D)

![](https://blog.kakaocdn.net/dna/bmTdEB/btsKQgbyQ3d/AAAAAAAAAAAAAAAAAAAAAHMGXrOv-0kHF9LyeDAKibvOUBhIZU4WuKU04EmX-DUf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=T0rV8xHhw5agdu9%2BjjJczoI8GO8%3D)
![](https://blog.kakaocdn.net/dna/wy1ss/btsKOMivZHU/AAAAAAAAAAAAAAAAAAAAACsKV54318mjkyfBQYxgfzDxz_8eGekA1AOieyiP9qzg/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=NUtVy7ZhsQGijR6DlLcE3u2%2BGlc%3D)

아래의 코드를 보자

template는 &&(r-value)를 받아주는 것으로 했고,

위에서도 r-value 인자를 받는 함수만 있다면, 오류가 생겼었다.

하지만,, template는 잘 실행이 된다.

```
#include <iostream> 
  

void IntOverload(int& i)
{
	std::cout << "l-value" << std::endl;
}

void IntOverload(int&& i)
{
	std::cout << "r-value" << std::endl;
}

template <typename T>
void Test(T&& t)
{
	IntOverload(t);
}
void main()
{
	int i = 3;

	//이게 안되는게 정상...
	Test(i);
}
```

![](https://blog.kakaocdn.net/dna/c8fTLT/btsKPDrypzD/AAAAAAAAAAAAAAAAAAAAAO1VyKTElbfYO5YsS5QRYIiQ5sabNXsnm5fsvPDJptqP/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=eFRsFBPciRUUu565y7Fs6Zwfew8%3D)![](https://blog.kakaocdn.net/dna/dwAsjY/btsKPCTIors/AAAAAAAAAAAAAAAAAAAAAD_eMzgB6r5xHC8CkYPR3spvU_f--9forFrHExUMOolL/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=vKwXqqykEj5Rk4czAqa1H0A8fro%3D)

이렇게

**template에서 r-value를 받는 인자가 있을 때, l-value도 받을 수 있다.**

**Universal ref 라고 불린다.**

**(반대로는 동작 안해요!  : 왼쪽 사진)**

std::move만을 가지고는 아래와 같은 상황을 해결할 방법이 없다.

![](https://blog.kakaocdn.net/dna/xPAx0/btsKOmYQ90P/AAAAAAAAAAAAAAAAAAAAACiLS2NvRxh-IAyq1Fb-Ti_Nu_vxGbztns33IrqRdk-p/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=mezNPhi5Yx9Ds1icGexbmRuIkyo%3D)![](https://blog.kakaocdn.net/dna/6RxWO/btsKOSQxqUH/AAAAAAAAAAAAAAAAAAAAAHXU470lHXranxRyEKmk0FKui6bc-qX0ADLBkSOpAIFs/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=QpxNEpt90mregOxHgjDnFYbluMQ%3D)

std::move를 안 쓰면 전부 l-value로 인식하고,

std::move를 쓰면 전부 r-value로 인식한고,,,

이것을

std::forward는 반드시 template에서 사용해줘야한다. ( template parameter를 명시해한다.)

![](https://blog.kakaocdn.net/dna/ezDUTR/btsKOzQ99LW/AAAAAAAAAAAAAAAAAAAAAOur__5wsF1BTnTgXI4K14tLmsiaXV7RJ-4-n8QTH56y/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=RwAYuMOsY7AKC0eSLMlE9anoyBY%3D)

## **이렇게하면 Perfect Forwarding을 할 수 있다!!**

**근데.. std::forward는 어떻게 구현된거예요??**

![](https://blog.kakaocdn.net/dna/kMFZ7/btsKVJdAxVP/AAAAAAAAAAAAAAAAAAAAACnT-njpq48WuSLLIK1gEQbmox1udVGhg6UI6GdlJqQU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=HtY6XLoSs0i9%2B5nUODfq7hkSboI%3D)

move를 배울 때 봤던 문법들이 보인다.

```
// L-Value
_NODISCARD _MSVC_INTRINSIC constexpr _Ty&& forward(remove_reference_t<_Ty>& _Arg) noexcept 

// R-Value
_NODISCARD _MSVC_INTRINSIC constexpr _Ty&& forward(remove_reference_t<_Ty>&& _Arg) noexcept
```

L-value 와 R-value를 따로 받아준다, 근데 반환형은 똑같은데요?

이것도 move를 배울 때 나왔던 것은데 &&은 template에서 universal reference로 쓰인다.  
때문에 l-value, r-value를 동일하게 처리할 수 있는 것이다.

std::forward는

remove\_reference를 하고, l-r value 모두 처리가능한 universal reference로 반환하고 있는 것이다.