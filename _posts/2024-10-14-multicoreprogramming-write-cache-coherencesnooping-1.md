---
title: "[MultiCoreProgramming] Write Cache Coherence(Snooping)-1"
date: 2024-10-14
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

## **Snooping** 캐시 일관성 프로토콜 개요

공유 매체(버스 또는 스위치)를 통해 **캐시 컨트롤러가 모든 트랜잭션을  Snooping(감시) 하는 방식**으로 작동합니다

* **캐시 컨트롤러**는 자신이 포함한 블록에 대한 관련 트랜잭션을 **Snooping(감시)**합니다.
* 일관성을 보장하기 위해 **invalidate,** **update, supply value** 제공 등의 조치를 취합니다.
* 구체적인 동작은 **블록의 상태(ex. MESI)**와 **프로토콜(~일 때~해라)**에 따라 다릅니다.
* 쓰기 전에 반드시 내가 쓴다는 것을 다른 프로세서(내가 쓸 데이터를 소유하고 있는)에게 알리고 써야한다.
  + **소유하고 있던 다른 프로세서들에게 Invalidate라고 알리기만 한다. (일반적으로 사용되는 방식)**
  + 소유하고 있던 다른 프로세서들에게 Write 후에 값을 알려준다.(Wrtir-thr)

## Architectural  Building Blocks

1. **FSM(Finite State Machine)**: 블록의 상태 변화가 어떻게 변화하는 지정해준다.
2. **Broadcast Medium Transactions**: 
   * Logically, design abstraction(프로세서들이 한 개의 버스로 모두 연결된 그림으로 설명하여도, 실제로는 1개의 버스로 연결된 것이 아니라 연결이 되어있다는 의미로 추상적으로 표현한 것이다.
3. **Serialization(write Serialization)**
   * 쓰기 작업을 위해서 가창 먼저 소유권을 얻어 낸다
   * 쓰기 작업이 끝날 때까지 접근하지 못한다
   * cache block에 대해서 serializing을 해야한다. (invalidata or update data)
4. **Need to find up-to-date copy of cache block:** 가장 최신의 캐쉬 블럭을 사용한다.

## **Locate up-to-date copy of data(최신 데이터)**

**Write-through**

* 캐시에 쓰기 작업이 발생할 때마다 즉시 메인 메모리에도 쓰기를 수행한다. (소유하고 있는 프로세서에 값을 업데이트를 해준다)
* 장점
  + 구현이 단순하다
  + 메모리와 캐시의 데이터가 항상 일치하므로, 최신 데이터를 쉽게 찾을 수 있다.
* 단점: 메모리 대역폭을 많이 사용합니다.

**Write-back**

* 캐시에 쓰기 작업이 발생해도 즉시 메모리에 쓰지 않고, 캐시에만(tag에 기록한다) 변경을 기록한다.
* 나중에 **캐시 변경이 일어날 때(Snooping 중이기 때문에 누가 접근하는지 알 수 있다)** 업데이트를 해준다.
* 장점
  + 메모리 대역폭을 적게 사용합니다
  + 더 많은 수의 빠른 프로세서를 지원할 수 있습니다.
* 단점
  + 구현이 더 복잡합니다.(프로그래머가 하면 되니 소비자 입장에서는 단점이 아님)

#### **Write-back(더 자세히, Snooping)**

* 버스에 올라오는 모든 주소를 Snooping(감시)한다.
* 만약 프로세서가 요청된 캐시 블록의 복사본(내가 write를 해서 값이 바뀐)을 가지고 있다면
* 읽기 요청에 대해 해당 데이터를 제공하고, state를 변경한다.
* 메모리에서 가져오는 것 보다 복잡성이 증가해서, 시간이 더 오래걸릴 수도 있다.

## **대부분의 멀티프로세서 시스템은 Write-back 방식을 사용합니다.**

* 메모리 대역폭을 적게 사용하여 시스템 성능을 향상시킬 수 있다..
* 더 많은 수의 빠른 프로세서를 지원할 수 있어 확장성이 좋다.

## **Cache resources for WB Snooping**

#### **Cache Tag**

* 기존의 캐시 태그 구조를 스눕핑에 활용할 수 있다.
* 각 블록마다 있는 Valid 비트를 이용해 invalidation를 쉽게 수행한다.
* Read misses는 Snooping에 의존하기 때문에 처리가 쉽다.

#### 

#### **캐시 블록 공유 상태 추적**

* **공유 상태 추적**
  + 각 캐시 블록에 추가적인 상태 비트를 할당한다. (Valid 비트, Dirty 비트와 유사)
  + 이 비트는 해당 **블록이 공유 여부를 나타낸다**.
* ****공유 블록에 대한 쓰기 처리****
  + 다른 복사본이 **없는 경우:** Write-Back에서 버스에 쓰기를 올릴 필요가 없다.
  + 다른 복사본이 **있는 경우:** 버스에 Invalidate를 보내야 한다.
  + 그리고 private상태로 변경한다.
* **Invalidation 최소화**
  + 블록이 private 상태가 되면, 해당 블록에 대한 추가적인 Invalidations는 발생하지 않는다.
* **Owner** 개념
  + 이 과정을 수행한 프로세서를 해당 캐시 블록의 **Owner**라고 부른다.
* **State** 변경
  + Owner는 캐시 블록의 State를 Shared에서 Unshared(Exclusive)으로 변경한다.

## 

## **Cache Behavior in Response to Bus**

#### 모든 버스 트랜잭션은 Cache-Address Tags를 검사해야 한다

* 프로세서의 캐쉬 접근에 **interference (간섭)을 일으킬 수 있다.**

* **interference(간섭) 감소를 위한 방법**
  + **태그 복제**
    - 태그를 두 세트로 복제한다. 하나는 **캐시 접근용,** 다른 하나는 **버스 접근용**
    - **프로세서와 버스**의 **캐시 접근이 서로 독립적**으로 이루어질 수 있다.
    - 하지만 추가적인 Memory OverHead가 발생한다. ( Tag가 2배가 되기 때문에)
  + **L2 캐시 태그**
    - **L2 캐시**는 L1 캐시보다 **덜 사용된다**.
    - **Inclusion property**(포함 속성) : **L1 캐시의 모든 항목은** 반드시 **L2 캐시에도 존재**해야 한다.
    - **L2 캐시에 없다면 L1캐시에 찾아봐야된다.**
    - **L2 캐시에서 히트(hit)**를 얻으면.
    - L1 캐시의 데이터, 상태를 업데이트하가위해서 **arbitrate(중재)해야한다.**
    - **arbitrate:** 상태 업데이트와 데이터 검색을 위한 것으로, 보통 프로세서의 지연(stall)을 유발합니다.