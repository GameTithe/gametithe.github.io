---
title: "[MultiCoreProgramming] Directory Protocol (1)"
date: 2024-10-18
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

#### **캐시 일관성 시스템의 필수 요소**

set of state, state transition diagram, action 을 제공한다.

Manage Coherence Protocol

(0) Coherence Protocol을 호출할 시기 결정

(a) 다른 캐시의 블록 상태 정보 찾기

(b) 다른 복사본 위치 찾기

(c) 해당 복사본들과 통신 (invalidate/update)

**일관성 프로토콜 호출 (0, 공통 수행)**

* **모든 시스템에서 동일**하게 수행된다.
* 캐시 내에서 state of line을 유지한다.
* "access fault"가 발생하면 프로토콜 호출

**접근 방식의 차이는 (a)부터 (c)에서 나타남**

1. Bus Based Coherence
   * **(a), (b), (c) 모두 bus를 통한 브로드캐스트**로 수행
   * 오류 발생 프로세서가 "search" 신호 전송
   * 다른 프로세서들이 search에 응답하고 필요한 조치 수행
   * **확장 가능한 네트워크에서도 사용 가능** **(모든 프로세서에 브로드캐스트)**
   * 개념적으로 단순하지만 프로세서 수 증가에 따른 확장성 문제
   * 버스 대역폭 확장의 한계
   * 프로세서가 p개 있으면 한개의 오류에 대해서 **최소 p개의 트랜잭션 발생**
2. Directory based Coherence  
   * 각 메모리 블록은 디렉터리 정보를 가진다.
   * 캐시된 블록의 복사본과 상태를 추적한다.
   * miss 발생 시 디렉터리 항목 찾아 조회 후 필요한 노드와 통신한다.
   * 확장 가능한 네트워크에서 디렉터리 및 복사본과의 통신은 네트워크 트랜잭션을 통해 수행한다.
   * 디렉터리 정보 구성에 다양한 방법이 존재한다.

### **차이점**

버스 기반 시스템

* 간단하지만 확장성 제한
* 모든 프로세서에 브로드캐스트하여 통신 부하 증가

디렉터리 기반 시스템:

* 확장성이 뛰어남
* 필요한 노드와만 선택적으로 통신하여 효율적
* 디렉터리 관리에 따른 추가 복잡성, 오버헤드