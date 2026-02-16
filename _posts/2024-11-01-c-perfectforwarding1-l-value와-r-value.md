---
title: "[C++] PerfectForwarding(1): l-value와 r-value"
date: 2024-11-01
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

int i;

int j;

i = 3;

j = i;

의 동작과정을 그림으로 나타낸 것이다.

![](https://blog.kakaocdn.net/dna/dMMSQN/btsKryFJlEQ/AAAAAAAAAAAAAAAAAAAAANE43btxZxwFR8wRB1mAdvBM5Lt5L90em_qmNmh3qMXl/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1HZLH%2B72MpNt0cEqVrxGpzKwtj0%3D)

int i 와 j = i에서 동일하게 i를 쓰고 있는데, **i가 실제로는 다른게 의미하고 있다. (파란색 하이라이트)**

**i=3은 [5000]번지 주소에 3을 할당하겠다.**

**j=i는 [**4900]번지 주소에 [5000]번지에 있는 값을 할당하겠다. 라는 의미이다****

여기서 r-value와 l-value가 등장한다.

**l-value(등호의 왼쪽)**

int i:  i의 주소

**r-value(등호의 오른쪽)**

j = i:  i가 가르키고 있는 값

**Ex**

**i + 1에서 주소를 가져 올 수 있을까?**

값만 존재한다 =>  **l-value(주소)는 존재하지 않고 , r-value(값)만 존재한다.**

(물론 i + 1의 값이 어딘가에 저장되어있을 것이다. 하지만 그 주소를 우리에게 알려주진 않는 상황이다.)

**등호의 왼쪽에는 항상 주소를 구할 수 있는(l-value) 표현식이어야 한다.**

(i + 1)= j; 가 잘못된 이유이다.

아래의 코드를 다시 그림으로 나타냈다.

![](https://blog.kakaocdn.net/dna/bhENoo/btsKr7HGzFC/AAAAAAAAAAAAAAAAAAAAAB14OawTJjcm13J29TlF7zN1A3Xi1SMUYe0iuQKEXu1J/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=p5o7rFFNq7SOYnWW%2BYK%2F7y74sj4%3D)![](https://blog.kakaocdn.net/dna/uNtIx/btsKrz5Ef6k/AAAAAAAAAAAAAAAAAAAAAPTXtIypsNeZP0KZJqVGBwpclfdmA3okTxlJ0FbRswqV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KWXNNmVY5XHjxFfPwx67bXJ3FLg%3D)

![](https://blog.kakaocdn.net/dna/cOELQP/btsKr9Fk5dd/AAAAAAAAAAAAAAAAAAAAAGeOL8RUujPZ0AzWsL_b4Ec2c82UKSgQDcisNhBR2wnb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=FUJm7QI28xYj1UvM5ku0BFsxQzM%3D)

4가 이닌 3이 출력되는 것은 알고 있을 것이다.

이 이유가 Test(int) 함수의 인자에 r-value(값)을 주었기에 main에 있는 i의 값는 영향이 없는 것이다.

main에 있는 i의 값을 바꾸고 싶다면 r-value가 아닌 l-value를 넘겨줘야 한다.

Test(int &)로 해결할 수있다.