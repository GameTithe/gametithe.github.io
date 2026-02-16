---
title: "[MultiCoreProgramming] Cache Coherence & Cache Consistency"
date: 2024-10-04
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **Application parallelism은 병렬 처리 알고리즘이 굉장히 중요하다.**

**remote latency는 컴퓨터의 구조와 프로그래머에게 달려있다.**

**예를 들면**

![](https://blog.kakaocdn.net/dna/mhhHR/btsJNflownz/AAAAAAAAAAAAAAAAAAAAAA96pa8klCH_5ChsnA_ztBlOx7p-u8p76QMZZdXghEfq/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=WAghaXKex4oXOcg8Q%2BKtzYcR%2Bj4%3D)

보라색 선(공유메모리의 범위)은 프로그래머가 설정할 수 있다. 공유하는 메모리 범위가 넓어질 수록 속도는 느려질 수 밖에 없다. 찾아야할 곳이 넓어지는 것이니...

Hardware: Caching shared data

Software: Restructuring the data layout to make more access local

또한 메모리를 같이 사용할 때 주의해야 될 점이 두가지가 존재한다.

### **1.** **Cache Coherence**

**Coherence는** 여러 캐시가 같은 메모리 주소에 대한 복사본을 가지고 있을 때, 그 복사본들이 서로 **일관성을 유지하는지**에 관한 문제를 다룹니다. 이 문제는 다중 프로세서 시스템에서 특히 중요한데, 각 프로세서가 자신의 로컬 캐시를 사용하기 때문에 동일한 데이터가 여러 프로세서의 캐시에 분산되어 있을 수 있습니다.

Migration, Replication

#### 예시:

* 두 개의 프로세서가 같은 메모리 위치 X를 참조하고, 그 위치의 값이 10이라고 가정합니다.
* 프로세서 1이 메모리 위치 X의 값을 20으로 변경합니다. 이때 프로세서 2가 여전히 X의 값을 10이라고 생각하고 읽어버리면 문제가 발생합니다.
* **캐시 일관성** 프로토콜은 이런 문제가 발생하지 않도록 보장합니다. 가장 일반적인 프로토콜로는 **MSI**, **MESI**와 같은 상태 기반 프로토콜이 있습니다.

### **2.** **Cache Consistency**

**Consistency는** 시스템 전체에서 메모리 접근 순서가 일정한 규칙을 따르도록 보장하는 것입니다. 여기서는 메모리에 대한 읽기/쓰기 작업이 여러 프로세서나 스레드에서 발생할 때, 그 접근이 **순차적**으로 보이는지를 다룹니다.

#### 예시:

* 프로세서 1이 메모리 위치 A에 10을 쓰고, 그다음에 B에 20을 쓴다고 가정합니다.
* 프로세서 2가 이를 읽을 때, A의 값이 10이고 B의 값이 20이라는 것을 **순서대로** 읽는 것이 보장되어야 합니다.
* **캐시 일관성**에서는 프로세서 2가 A와 B를 일관된 순서대로 읽을 수 있도록 해야 하며, 읽기/쓰기 순서의 규칙을 정의한 모델이 중요합니다.

### **주요 차이점 비교**

  

|  |  |  |
| --- | --- | --- |
|  | **Cache Coherence** | **Cache Consistency** |
| **핵심 목적** | 여러 캐시에 저장된 동일 데이터의 일관성 유지 | 메모리 접근 순서와 일관된 읽기/쓰기 동작 보장 |
| **다루는 문제** | 동일 메모리 위치에 대한 각 캐시의 값이 다를 때 해결 | 메모리 접근이 여러 프로세서에서 일관되게 보이는지 |
| **사용되는 프로토콜** | MSI, MESI, MOESI 등의 상태 기반 프로토콜 | 메모리 일관성 모델 (Sequential Consistency 등) |
| **중점** | 데이터 값의 즉각적인 동기화 | 메모리 접근 순서의 일관성 |
| **적용 환경** | 멀티캐시 시스템에서 발생하는 데이터 불일치 해결 | 멀티프로세서 시스템에서 메모리 순서 보장 |

### 

### **요약:**

* **Cache Coherence**: 여러 캐시가 같은 데이터에 대한 **동일한 값**을 유지하도록 보장하는 것.
* **Casche Consistency**: 메모리 접근이 시스템 전체에서 **일관된 순서**로 발생하고 그 결과가 일관되게 보이는지 확인하는 것.