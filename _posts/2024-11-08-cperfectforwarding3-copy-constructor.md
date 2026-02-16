---
title: "[C++]PerfectForwarding(3): copy constructor"
date: 2024-11-08
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

```
#include <iostream> 

using namespace std;
 
class KTest
{
private:
	int* pData;
	int dataSize;

public:
	KTest() : dataSize(3) 
	{
		pData = new int[dataSize]; 
		cout << "Constroctor" << endl;
	}

	void Release() { dataSize = 0; delete[] pData; }
	~KTest() 
	{
		Release(); 
		cout << "Destroctor" << endl;
	}
};

int main()
{
	KTest k;
}
```

이 상태에서 시작해보자.

```
void Test(KTest t)
{
	cout << "Test" << endl;
}
```

여기서 이 코드만 추가하고 실행시켜보면 크래쉬가 난다.

![](https://blog.kakaocdn.net/dna/bom6Q2/btsKB5aqjl9/AAAAAAAAAAAAAAAAAAAAAAV-Diujjo3Q2xZVBMAEzJpwNlYx7vxjfaIDcAmkOQEt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=m1jGwgzsBwebj8DdgKpWHoctIpo%3D)

크래쉬가 나는 이유를 보기 위해서

소멸자의 Cout 코드를 Release 위로 올려보자

```
~KTest() 
{
	cout << "Destroctor" << endl;
	Release(); 
}
```

생성자는 1번 소멸자는 2번 호출되는 모습을 볼 수 있다.

![](https://blog.kakaocdn.net/dna/cvc152/btsKAK59nho/AAAAAAAAAAAAAAAAAAAAAKunT57R8O36xYNAD4lS5FNrzrZYuvPrRLTAoZeQF5GN/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fSwzJtj7lBeuDg6cT%2F1tMyHYNZM%3D)

#### **복사 생성자**

우리에게 필요한건

Test함수로 값을 복사 시킬 때 호출될 생성자가 필요한것이다.

```
//복사 생성자 
KTest(const KTest& rhs)
{
	dataSize = rhs.dataSize;
	pData = new int[dataSize];
	memcpy(pData, rhs.pData, sizeof(int) * dataSize);

	cout << "Copy Constroctor" << endl;
}
```

dataSize를 복사하고,

pData도 새롭게 동적할당해준다.

그리고 pData의 값을 그대로 가져와준다.

![](https://blog.kakaocdn.net/dna/baQsxY/btsKBpmTkJw/AAAAAAAAAAAAAAAAAAAAADbRI0_k2QlZk071gW_9__3sIgzkymgLabOH74lN1m5c/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=cdMPqJvn2sLSgPFgANIL4%2FNnxF0%3D)

우리가 원하는대로 크래쉬가 안나고 잘 출력되는 것을 볼 수 있다.

복사생성자는 함수로 복사할 때 뿐만 아니라

![](https://blog.kakaocdn.net/dna/YDEDU/btsKB4o3b3E/AAAAAAAAAAAAAAAAAAAAADlM1vhrADb5fShcH03cWz1bnhMeGY34S_EBu9pmW3r8/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=jadSykeEJ0QtdbqcbJe53ikNeG4%3D)![](https://blog.kakaocdn.net/dna/4monv/btsKzxNALP5/AAAAAAAAAAAAAAAAAAAAANJ2M2RWgqbyvDUnEx8oMSkmk0LBmMEspCb0E4ahQt0U/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=798IgNQnytSsk2Lvvyi9mfA7a6E%3D)

이런 상황에서도 Copy Constroctor가 호출되는 것을 볼 수 있다.

**동적으로 내부에서 데이터를 관리하고 있는 상황이라면 Copy Controctor 만들어줘야된다!**

이것도 당연히 될 줄 알았겠지만, 2줄로 나눠서 코딩했을 뿐인데 크래쉬가 나는 모습을 볼 수 있다.

e=t 부분에서 e가 가르키는 pData 포인터와 t의 pData포인터가 일치되면서 생기는 버그이다.

![](https://blog.kakaocdn.net/dna/SBhT2/btsKzWzu9Gy/AAAAAAAAAAAAAAAAAAAAADjDdhB0XRdfZGB4VHDZdlKcThNlqMR_49m3nRlAlOz8/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=YW61m9u9p8RgemkOCorcIgnsC%2Fk%3D)![](https://blog.kakaocdn.net/dna/bxv39m/btsKB4WUuVa/AAAAAAAAAAAAAAAAAAAAAA2YxDF71cXyuJyaE2IIS9t-apAv4ypvaHzg3WVlf6At/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=M9PR3hW6XHHFHIUymT%2FQ4r%2Fuce4%3D)![](https://blog.kakaocdn.net/dna/EQNF0/btsKBIO6iX1/AAAAAAAAAAAAAAAAAAAAAJZfocXllc2QjRtokLbtXv5EGrLaQyzQn7Du0qtXgMqV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=s0RscxEVgEOt28o3eYIDM0j1h4c%3D)

```
	void Release() { 
		dataSize = 0;
		cout << pData << endl;
		delete[] pData; 
	}
	~KTest() 
	{
		cout << "Destroctor" << endl;

		Release(); 
	}
```

주소를 출력해서 보면 소멸자에서 똑같은 주소를 2번 호출 하는 것을 볼 수 있다.

```
	KTest& operator=(const KTest& rhs)
	{ 
		dataSize = rhs.dataSize;
		pData = new int[dataSize];
		memcpy(pData, rhs.pData, sizeof(int) * dataSize);

		cout << "operator=()" << endl;
		return *this; 
	}
```

이렇게 복사대입연산자를 통해서 새롭게 동적할당을 해주면서 버그를 피할 수 있다.