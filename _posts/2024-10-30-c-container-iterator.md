---
title: "[C++] Container & Iterator"
date: 2024-10-30
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### 1. **Container (컨테이너)**

컨테이너는 데이터를 일정한 구조로 저장하는 자료구조이다. (ex. arraym, linked list, tree ... )

(분홍색으로 그린부분을 컨테이너라고 볼 수 있다.)

![](https://blog.kakaocdn.net/dna/21s2F/btsKqBuhmmY/AAAAAAAAAAAAAAAAAAAAANON3P6Z02KGVJJWlWuVCzcuGVN1O7umiqJJXYTk7zQ8/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=7x%2B9Mfd%2BmM2MAZDYoqDkeTBkX4w%3D)

### 2. **Iterator (이터레이터)**

Iterator는 Container**에 저장된 요소들에 대해 외부에서 접근할 수 있는 방법**을 제공한다.

Iterator를 사용하면 컨테이너의 종류에 상관없이 **동일한 방식으로 데이터에 접근할 수 있다**. (코드로 예시를 듦)

![](https://blog.kakaocdn.net/dna/u6TzK/btsKp2TgLfK/AAAAAAAAAAAAAAAAAAAAAM4x3I8KnqoGoGBDSIy7K1Ri5qTvsqBz8QqBqLRx-MER/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=axbPZMJCFdBZB%2BYWzcEY%2Bx%2B%2F3s4%3D)
![](https://blog.kakaocdn.net/dna/TTZjs/btsKq0mMd2C/AAAAAAAAAAAAAAAAAAAAAJQE6PMSWw2u1N4RVuPfN_ZI2Atz1svDgw9jPo1I1tE0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=VVBvBOVmQ3J6JqvNdCOPV073jnE%3D)

**std::vector<int>::iterator**

**->int 타입의 vector Container의 Iterator라는 의미이다.**

위의 코드와 같이

iterator로 접근이 가능하다.

#### 

#### **컨테이너 종류에 상관없이 접근이 가능하다는게 무슨의미예요?**

아래 코드는 vector<int> 를 list<int>로만 바꾼것이다

![](https://blog.kakaocdn.net/dna/b8x4kY/btsKqIUgrIE/AAAAAAAAAAAAAAAAAAAAAFmi1zbRNrsBPwVOGHO5QzkuCoHRF6jv1KgjDn9mzC1w/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=q6wsRYMlRtbOfyF4xAQtnNDJol0%3D)
![](https://blog.kakaocdn.net/dna/cQPGKZ/btsKq163lGW/AAAAAAAAAAAAAAAAAAAAAMgog8m_V6EwuVlz70ljhx_2SPmItCkma1MV0uE2Ux-A/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=pZzU4IBaXxUT2ifg35q7s3O1oes%3D)

vector<int>와 동일하게 작동한다!!

Begin():  **첫번째** 데이터의 주소

End()   : 마지막 데이터의 **다음 주소**

**N이 3일 때를 예시로 보자**

![](https://blog.kakaocdn.net/dna/bBqZgF/btsKoV8TbeS/AAAAAAAAAAAAAAAAAAAAAAbbQzGtjiOnJva6u-S60rs0vBKXHrJE5BWQraka_qGX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hKF4CpjiCZ9xAqyvrN3rZoYDg8g%3D)

**N이 0일 때를 예시로 보자**

![](https://blog.kakaocdn.net/dna/bGlFne/btsKpV7XtWP/AAAAAAAAAAAAAAAAAAAAAIfz9x2ueDPFhHlqHmese4DKWN-ep1H2fccNgGjFvQ6c/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=MSOnG4e8V8dlo5ZfG8GSNt%2FYEHg%3D)

#### 

#### MyVector를 만들면서 구조를 다시 한번 보면 정리가 잘 될 것이다!

위에서 vector<int>를 사용해서 순회했던 for문을 그래도 써도 작동이 된다!

![](https://blog.kakaocdn.net/dna/bhFeE0/btsKrcOkvtm/AAAAAAAAAAAAAAAAAAAAAJ_8I5PoUoEIEGLtP0fKIN_HKX1swwLOmmZBeTDi7Gru/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=z%2FDaoI85m2gPRMJGSEAJi3cgZ%2Fk%3D)