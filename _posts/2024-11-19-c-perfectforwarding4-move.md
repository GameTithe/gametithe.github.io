---
title: "[C++] PerfectForwarding(4): move"
date: 2024-11-19
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

이전 글에서 copy constructor와 복사 대입  연산사를 사용해봤다.

이제 복사 대입 연산자를 사용했을 때 생기는 문제를 보면서 move연산자의 필요성을 느껴보자

아래의 코드에서는 사실 t 하나만 사용하고 있다. (심지어 주소까지 같은)

근데 생성자(복사까지 합쳐서) 2번이나 호출된다. 불필요한 생성자가 호출이되고 있는 것이다.

![](https://blog.kakaocdn.net/dna/HjUeE/btsKN4RisV0/AAAAAAAAAAAAAAAAAAAAACXqK4ka7g7W4lhqerg4j6DKgAbBNh0ZwEbYc2XqkE2z/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=HoC2pX8K%2BnK%2BHBVGfwp6M4FZG9Y%3D)

불필요한 생성자 호출을 줄이기 위해서 move constructor가 등장했다.

move를 사용할 때 문법은 &&이니 알아두자

자!

(move constructor 부분을 발췌한 후 풀 코드는 마지막에 기제해놓겠다.)

move가 내부적으로 어떻게 작동하느냐면

dataSize를 넘겨주괴, pData도 전달하고 ( rhs의 값들을 모두 전달하고)  
**rhs는 소멸된다.**

복사연산자들은 어땠나?  
내 것을 전달해주기만하지 rhs를 건들지는 않았다. 하지만 move는 과감하게 전달하고 사망한다.

```
    // 복사가 없이 일어난다.
    KTest(KTest&& rhs) //move constructor
    {
        //rhs 값을 전달하고
        dataSize = rhs.dataSize;
        pData = rhs.pData;
    
        //rhs의 데이터를 소멸시킨다.
        rhs.dataSize = 0;
        rhs.pData = nullptr;
        cout << "move Constructor" << endl;
    }
```

```
    KTest& operator=(KTest&& rhs) //move assignment operator
    {
        if (this == &rhs)
            return *this;

        Release();

        dataSize = rhs.dataSize;
        pData = rhs.pData;

        rhs.dataSize = 0;
        rhs.pData = nullptr;

        cout << "move operator=()" << endl;
        return *this;
    }
```

허접하지만 그림으로 한 번 더 살펴보자

(파란색)이렇게 GetTest 에서 값이 만들어진다.

그리고

(보라색) 그 값이 main으로 전달된다.

(지우개) 다 지우고나면 소멸~

![](https://blog.kakaocdn.net/dna/bHaI8G/btsKPbvxBdU/AAAAAAAAAAAAAAAAAAAAANdITy3jHkGcgUSIXyejdqt7A750SlX4IVnb7sA2bXJV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=CWTwtN8B06xtZmjilBaxv0Pb57E%3D)![](https://blog.kakaocdn.net/dna/8kmt8/btsKQeSk8Ed/AAAAAAAAAAAAAAAAAAAAAJM9Iphny7q4-Z4TdbEMzF1j6R-KOVjoW2vawnQjzXJh/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=y8S68PqjTraCnRkd%2FzNvYiu%2Bpig%3D)![](https://blog.kakaocdn.net/dna/mc6Mu/btsKPAawksN/AAAAAAAAAAAAAAAAAAAAAEEYlbM5DKaaK6Sb0J4bjbUwMDLMI8YHMcIpJcfQFR1N/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=t8nFycUCOQq4VSX1xdJCE%2F%2F5G48%3D)

말로만 하면 못 믿겠죠? 직접 출력해보면 그림과 같이 동작하는 것을 알 수있습니다!

![](https://blog.kakaocdn.net/dna/skKV9/btsKN1HqhHB/AAAAAAAAAAAAAAAAAAAAAM5UN-gXKw-Xo_0K4XOis0mGwce9GYQWN_vmGrcpMbUw/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=c9N3W4uzGpDIV7LRRtfT25KIHN4%3D)

근데 왜 우리가 만든 move연산자들은 출력이 안되죠...?

사실 그것때문에 포스팅이 늦어졌는데

RVO(Return Value Optimization), NRVO(Named Return Value Optimazation) 떄문이다.

간략히 말하면 t (GetTest에서 만들어진) 가 t (main에 있는) 로 갈 것을 미리 인지하고 main t에다가 값을 할당해버려서 복사, move연산자가 생략된다...

오늘은 이론을 알아본 것으로 만족하자.. :)

이제 모든게 완벽해보이지만,,,!  
한 가지가 남았다. move로 넘겨준 r-value ref는 넘겨준 다음에도, 그 성질이 유지가 되어야한다.  
하지만 이 코드를 보면, 그 이후까지 신경쓰진 않을 것 같다.

#### **이것을 해결하는 것이 PerfectForwarding이다!**

C++11부터 도입된 move는 불필요한 복사를 줄이고 성능을 최적화하는 데 중요한 역할을 한다.

아래서 복사연산자 부분을 잘 봐보자.

기껏 && 사용해서 r-value로 보내줬구만, 내부에서 l-value로 쓰면서 copy contructor가 호출된다.

```
class KContainer
{
private:
    KTest t;

public:
    KContainer() {}
    KContainer(const KContainer& rhs) {} //copy
    KContainer(KContainer&& rhs) // move
    {
    //여기를 보면 또 copy가 일어날 것이다.
        KTest t = rhs.t; // call copy contructor 
    } 
    ~KContainer() {} 
};
void Test(KTest t)
{
    cout << "Test" << endl;
} 
KTest GetTest()
{
    KTest t; 
    return t;
}

KContainer GetContainer()
{
    KContainer c;
    return c;
}
int main()
{  
    KContainer c = GetContainer();


    return 0;
}
```

이를 막기위해서,

**정확히 말하면 r-value ref 로 값을 보내줬으면, 내부에서도 그것을 유지하기 위해서!! move를 사용해야된다!!**

```
   KContainer(KContainer&& rhs) // move
   { 
       KTest t = std::move(rhs.t); 
   }
```

이렇게 만들어주면, 내부에서도 r-value ref를 유지하는 것을 볼 수 있다 :)

**//move 코드**

```
class KContainer
{
private:
    KTest t;

public:
    KContainer() {}
    KContainer(const KContainer& rhs) {} //copy
    KContainer(KContainer&& rhs) // move
    {
    //여기를 보면 또 copy가 일어날 것이다.
        KTest t = rhs.t; // call copy contructor 
    } 
    ~KContainer() {} 
};
void Test(KTest t)
{
    cout << "Test" << endl;
} 
KTest GetTest()
{
    KTest t; 
    return t;
}

KContainer GetContainer()
{
    KContainer c;
    return c;
}
int main()
{  
    KContainer c = GetContainer();


    return 0;
}
```