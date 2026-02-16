---
title: "[C++] PerfectForwarding(4): move(2)"
date: 2024-11-20
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

move를 구현해보면서 move가 어떤 일을 하고 있었는 지 알아보자

실제 move를 봐도 remove\_reference를 하고 && 로 캐스팅해서 반환하고 있는 모습을 볼 수 있다.

![](https://blog.kakaocdn.net/dna/cv4ru4/btsKN6hCFDV/AAAAAAAAAAAAAAAAAAAAAGkepIjJXcytBNR0O0KhVQKPpZuh4TECTGyB2451cDDD/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=j7wazfzY%2Fv0ukjiBWCH1KE1RHxE%3D)

아래의 코드와 같이 remove\_reference가 구현된다.

type들을 다 제거하고 원본을 반환하는 것이다.

거기에 move는 && 붙혀서 내보내는 것

```
template <typename T>
struct remove_reference {
    typedef T type;  // 참조가 없는 타입 그대로 반환
};

template <typename T>
struct remove_reference<T&> {
    typedef T type;  // T& -> T로 변환
};

template <typename T>
struct remove_reference<T&&> {
    typedef T type;  // T&& -> T로 변환
};
```

move의 한계점을 보자

아래의 코드 처럼 l-value, r-value를 인자로 받는 Test(), Test2()가 있다.

Test2()에서는 Test()를 한 번 더 호출해준다.

```
void Test(KTest& t)
{
    std::cout << "l-value Test()" << std::endl;
};
void Test(KTest&& t)
{
    std::cout << "r-value Test()" << std::endl;
}
```

```
void Test2(KTest& t)
{
    std::cout << "l-value Test2()" << std::endl;
    Test(t);
};
void Test2(KTest&& t)
{
    std::cout << "r-value Test2()" << std::endl;
    Test(t);
}
```

```
KTest GetTest()
{
    KTest t;
    return t;
}
int main()
{   
    KTest t;
    Test2(t);
    Test2(GetTest());

    return 0;
}
```

우리가 지금까지 배운게 있으니

여기까지 예측하는건 어렵지 않다.

**Test2(t)는** l-value니까

"l-value Test2()"

"l-value Test()"

가 호출되겠구나

Test2(GetTest())에서 GetTest()는 r-value를 반환하니까

"r-value Test2()"

그리고 함수 내부에서 이름이 생기면서 l-value 가 됐으니까

"l-value Test()"

가 호출되겠구나

![](https://blog.kakaocdn.net/dna/s07TY/btsKPE43Nbo/AAAAAAAAAAAAAAAAAAAAANssVgxx1tm7qqiFRS6H0e8JaokmVL76y-aAvY49qA04/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KcNqnBUPvs2FOS0%2BKbORybY1Iyw%3D)

당연히 예측한대로 잘 호출된다.

그리고   
"r-value Test2()"   
"r-value Test()"

로 출력이 되게 만들기 위해서는 move를 사용하면 된다.

![](https://blog.kakaocdn.net/dna/qUdr0/btsKPIzD1tZ/AAAAAAAAAAAAAAAAAAAAANLZZsig2aK0qWpQ3AWQfdK0Yyw9sdLGYu3be68e75r0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=A68j7IMSmHGY04Jr3%2FOhG6IDimg%3D)![](https://blog.kakaocdn.net/dna/bTLAOn/btsKO7mnwuV/AAAAAAAAAAAAAAAAAAAAAICaYlMsbITGmlk7eTN3ArslILMw6jcC4HrsZO_ozbwV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ZhhP0reRVsFrbPod7fq2qjGUlM8%3D)

여기서 생각해볼 점은

template함수를 작성하다보면 인자로 넘어온 것이 **l-value인지 r-value인지 모르는 상황이 생긴다.**

그럼 그때는 어떻게 할까...?

너무 길어지니 다음 글에서 이어서 설명하겠습니다.