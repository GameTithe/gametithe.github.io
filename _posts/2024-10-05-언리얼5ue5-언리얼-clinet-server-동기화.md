---
title: "[언리얼5/UE5] 언리얼 clinet, server 동기화"
date: 2024-10-05
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **1. UFUNCTION(Server, Reliable)**

* **클라이언트에서 서버로** 호출된다.
* **Reliable**: 패킷 전송이 보장됩니다. 네트워크 상에서 손실되지 않고 반드시 서버에서 실행되도록 보장한다.
* 서버에서만 실행된다.
* **클라이언트에서** 어떤 동작을 **서버에게** 요청해야 할 때 사용된다. (ex 재장전 요청, 공격 명령 등)

### **2. UPROPERTY(ReplicatedUsing = 함수이름)**

* 등록한 변수가 **변경될 때** 클라이언트에게 자동으로 **복제**된다.
* ReplicatedUsing를 통해 **콜백 함수**를 지정한다.
* **서버에서** 해당 변수 값이 변경되면 **클라이언트가 이 변수의 값을 동기화**하고, 동기화가 완료된 후에 등록한 함수가 호출된다.
* 서버에서 변경된 값을 클라이언트가 정확하게 동기화해야 할 때 사용한다.
* 복제할 변수 등록 방법 ![](https://blog.kakaocdn.net/dna/WxJ4c/btsJVZv1kCr/AAAAAAAAAAAAAAAAAAAAAOViyEeIRRr7BwAGzYgR4b5cXPon-Ru4ROEA_JVEHMeE/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=h3etH0SVKk%2FLPnDNSxc4VW9fNSo%3D)

### **3. UFUNCTION(NetMulticast, Reliable)**

* 이 함수는 **서버에서 호출**되며, **서버**와 **모든 클라이언트**에서 실행된다.
* **Reliable**: 패킷 전송이 보장되며, 모든 클라이언트에서 반드시 실행된다. 즉, 네트워크 상에서 패킷 손실 없이 모든 클라이언트에 전달된다.
* **모든 클라이언트**에게 특정 동작을 **동기화**할 때 사용된다.

### 

### **정리**

|  |  |  |
| --- | --- | --- |
| **UFUNCTION(Server, Reliable)** | 클라이언트 → 서버 | 서버에서 실행 |
| **UPROPERTY(ReplicatedUsing)** | 서버 → 클라이언트 | 값이 복제될 때마다 클라이언트에서 콜백 실행 |
| **UFUNCTION(NetMulticast, Reliable)** | 서버 → 서버 및 모든 클라이언트 | 서버와 모든 클라이언트에서 실행 |