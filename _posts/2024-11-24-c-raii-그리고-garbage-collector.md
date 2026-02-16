---
title: "[C++] RAII 그리고 Garbage Collector"
date: 2024-11-24
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

<https://stackoverflow.com/questions/44325085/raii-vs-garbage-collector>

[RAII vs. Garbage Collector

I recently watched a great talk by Herb Sutter about "Leak Free C++..." at CppCon 2016 where he talked about using smart pointers to implement RAII (Resource acquisition is initialization) - Concep...

stackoverflow.com](https://stackoverflow.com/questions/44325085/raii-vs-garbage-collector)

### 

### **RAII와 GC비교**

RAII는 객체의 생명 주기와 자원 관리가 결합되어있다. **객체가 소멸되면 자원이 즉시 해제되므로, 자원 해제 시점이 결정적(deterministic)이다**. (swap and copy에서 사용된것을 확인한 적이 있다.  <https://tithingbygame.tistory.com/122> )

( 그렇기 때문에

RAII는 특정 시점에 파일을 닫거나 네트워크 연결을 해제하는 것처럼, 중요한 작업을 수행한 뒤 자원을 해제해야 할 때 적합하다. )

Java와 같은 GC는 자**체적인 오버헤드**가 있으며, **자원 해제 시점이 비결정적(nondeterministic)이다.** GC는 순환 참조(circular reference)를 자동으로 처리할 수 있다는 장점이 있지만, 결정적 해제를 제공하지 못한다.

하지만, GC는 작은 메모리 블록을 여러 번 해제하는 대신, 큰 메모리 블록을 한꺼번에 해제할 수 있어 효율적일 수 있다.