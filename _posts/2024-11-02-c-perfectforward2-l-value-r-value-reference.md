---
title: "[C++] PerfectForward(2): l-value, r-value reference"
date: 2024-11-02
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### 

### **0. Call by Value**

![](https://blog.kakaocdn.net/dna/ClhE2/btsKuQSej2r/AAAAAAAAAAAAAAAAAAAAALcHus_FIEN2o6xv9xbkVFN3wVzcfFhIF-r7agRDLnRd/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=qrCdg2M0RK%2B2yCpuf1Nza4SbMSo%3D)![](https://blog.kakaocdn.net/dna/yG3yu/btsKtrl46TS/AAAAAAAAAAAAAAAAAAAAAHFydADPvq1UrCDqBrD-f_3vlCPbfc0AHPtBAMSXvviP/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9WmfvNcywW9k%2FEA0YbPv3MGCgck%3D)

![](https://blog.kakaocdn.net/dna/cc4k2P/btsKtpPiu2P/AAAAAAAAAAAAAAAAAAAAAEzOWzxn5Wh9k4VJyVFGC-LBhZ3qVfwhclNSGwo85KIZ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=5Reqe4sBwmk7vi0sj7XaXOdW2dE%3D)

## **1. l-value reference**

![](https://blog.kakaocdn.net/dna/bPCBj8/btsKtJUgUPQ/AAAAAAAAAAAAAAAAAAAAAAZH7OiCqD5JYObYsNt5ehDcXtL9QoAoWaHz1yA3R1s9/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Yf1sLnYoLotqk3npArftIFvOxcI%3D)

* Test(KTest& t) 함수는 **l-value reference**를 인자로 받기 때문에, **l-value(이름이 있는 객체)만을** 인자로 받을 수 있다.
* Test(t)는 t라는 l-value를 전달하므로 정상적으로 작동한다.
* Test(KTest())는 임시로 생성된 r-value를 전달하므로 컴파일 오류가 발생한다. (실제로 해보면 빨간줄이 생긴다.)
* **l-value reference는 r-value를 받을 수 없다.**

### 

### **3. r-value reference**

![](https://blog.kakaocdn.net/dna/eFjPvJ/btsKtqOdAJJ/AAAAAAAAAAAAAAAAAAAAALetQQoqGRArqZdXWMkj7fdTq7rtgUKrQGOVt7yXyLOT/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=qvxAIFms1s7sBQQKTtmMAp06K1Y%3D)

* Test(KTest&& t) 함수는 **r-value reference**를 인자로 받는다.
* Test(t)는 l-value를 전달하기 때문에 컴파일 오류가 발생한다. (r-value reference는 l-value를 받을 수 없다)
* Test(KTest())와 같이 r-value(임시 객체)를 전달하면 함수가 정상적으로 호출된다.

### 

### **그냥 Call by value해서 다 복사하면 되는거 아닌가요.!**

만약에 함수로 보내는 값이 매우 매우 매우 매우 크다면...?  그런데 자주 호출된다면...?  
이런 상황에서 값을 복사하는 것만큼 최악은 없을 것이다.

이럴 때 l-value, r-value  ref를 이용해서 최적화를 해보자!

call by value(파랑, 보라) : 값복사

call by ref(빨강)              : 주소만 복사

![](https://blog.kakaocdn.net/dna/dMEc82/btsKtHvoUys/AAAAAAAAAAAAAAAAAAAAAOT9Fq9GN9_LYgbjH7tOaYLgjjMO2Kr6DvDJxMclgJqp/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=D5cMuxfc0yz9Y5OOTO1QJnLNcMc%3D)