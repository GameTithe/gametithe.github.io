---
title: "[MultiCoreProgramming] Directory Protocol (2)"
date: 2024-10-21
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **디렉터리 프로토콜의 기본 구조**

* k개의 프로세서가 있는 시스템일 때
* **메모리**의 각 캐시 블록에 연관된 정보
  + k개의 presence 비트
  + 1개의 dirty 비트
* **캐시**의 각 캐시 블록에 연관된 정보
  + valid 비트
  + 1개의 dirty (owner) 비트

1. 프로세서의 메모리 **Read** 동작

a) **프로세서 i가 메인 메모리에서 읽을 때**:

* dirty 비트가 OFF인 경우
  + 메인 메모리에서 읽음
  + **p[i] (presence 비트)를 ON**으로 설정
* dirty 비트가 ON인 경우
  + dirty 프로세서로부터 라인 회수 (캐시 상태를 shared로 변경)
  + 메모리에 데이터 값 업데이트(최신화)
  + **dirty 비트를 OFF**로 끔.
  + **p[i]를 ON**으로 설정
  + 프로세서 i에 데이터를 다시 콜

2. 프로세서의 메모리 **Write** 동작

a) **프로세서 i가 메인 메모리에 쓸 때**

* dirty 비트가 OFF인 경우
  + 데이터를 프로세서 i에게 제공
  + **해당 블록을 가진** 모든 캐시에 무효화 메시지 전송
  + **dirty 비트를 ON**으로 설정
  + **p[i]를 ON**으로 설정

#### **디렉터리 프로토콜**

**Memory( memory이기에 invalidation이 없다, cache 블럭에 invalidation이 저장된다.)**

* Shared: 하나 이상의 프로세서들이 데이터를 가지고  있으며, 메모리는 최신 상태
* Uncached: 어떤 프로세서도 데이터를 가지고 있지 않음 (어떤 캐시에도 유효하지 않음)
* Exclusive: 한 프로세서(소유자)만 데이터를 가지고 있으며, 메모리는 바뀐 상태

1. 추가적인 특징

* Shared 상태일 때 어떤 프로세서가 데이터를 가지고 있는지 추적한다(일반적으로 비트 벡터 사용)

========

단순화된 가정

* non-exclusive 데이터에 대한 쓰기 → 쓰기 미스 발생
* access가 완료될 때까지 프로세서를 블록
* 메시지는 전송된 순서대로 수신 및 처리됨

========

**디렉터리 프로토콜의 통신 특성**

* 버스가 없고 브로드캐스트를 하지 않는다.
* 상호 연결은 더 이상 single arbitration point이 아님
* 모든 메시지는 explicit respose가 필요
  + bus를 잡는다는 개념이 없기 때문에  프로세서간에 communication해야된다.

**관련 용어**

* Local node: **request가 시작되는 노드**
* Home node: 주소의 **메모리 위치가 있는 노드**
* Remote node: 캐시 블록의 **복사본을 가진 노드 (exclusive 또는 shared)**

상태 전이도의 기본 특성

* 스누피(Snoopy) 캐시와 동일한 State를 가짐
* 트랜잭션도 매우 유사함
* 상태 전이를 일으키는 요인:
  + Read miss
  + Write miss
  + Invalidate 요청
  + 데이터 가져오기 요청

메시지 생성

* 홈 디렉터리에서 Read miss와 Write miss 메시지 생성한다
* 버스에서 브로드캐스트되던 미스(Snooping) => 명시적인 Invalidate 및 데이터 가져오기 요청으로 변환됨(Directory)
* 쓰기 시 전체 캐시 블록을 읽어야 한다.

![](https://blog.kakaocdn.net/dna/Bgi2v/btsJ7e7qNUl/AAAAAAAAAAAAAAAAAAAAALfMMHSDMwogLPvQE9IUbpZhLNBCQuCOvU79JnIw-ZIV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=tvnWwv%2FsguJ28huDH7cLIbrXHCs%3D)

두 가지 주요 동작

* 디렉터리 상태 업데이트
* 요청을 만족시키기 위한 메시지 전송

Snooping 프로토콜과의 차이점

* 버스 브로드캐스트 대신 point to point 메시지 사용
* 확장성이 향상되어 대규모 시스템에 적합
* 더 복잡한 프로토콜 관리 필요

### **Synchronization**

동기화의 필요성

* 여러 프로세스가 공유 데이터를 안전하게 사용할 수 있는 시점을 알아야 함

동기화의 주요 이슈

* 메모리를 가져오고 업데이트하는 Uninterruptable 명령 (atomic 연산)
* 사용자 수준에서의 동기화 작업
* 대규모 멀티프로세서 시스템에서 동기화가 병목 현상이 나타날 수 있다.(deadlock)
* 동기화의 경합과 지연을 줄이자

Uniterruptable한 메모리 가져오기 및 업데이트 명령

* + 레지스터의 값과 메모리의 값을 교환하는 연산
  + 동기화 변수 값의 의미
    - 0: 동기화 변수가 자유로운 상태 (lock)
    - 1: 동기화 변수가 잠겨 있고 사용 불가능한 상태 (lock)
  + 작동 방식
    - 레지스터를 1로 설정하고 메모리와 교환
    - 레지스터의 새 값으로 잠금 획득 성공 여부 판단
      * 0: 잠금 설정 성공 (첫 번째로 접근)
      * 1: 다른 프로세서가 이미 접근 권한을 주장한 상태
  + 핵심: 교환 연산이 분할 불가능함( atomic하게 연산을 수행해야된다.)원자적 교환(Atomic exchange)
    - Test-and-set: 값을 테스트하고, 테스트를 통과하면 값을 설정하는 연산
    - Fetch-and-increment: 메모리 위치의 값을 반환하고 원자적으로 증가시키는

mov ~ beqz를 수행한다.

성공하면 move R4,R2로

실패하면 다시 mov R3, R4로

![](https://blog.kakaocdn.net/dna/HfNKP/btsJ5p3ye1u/AAAAAAAAAAAAAAAAAAAAAB-0ARa7TcmEjzLUOPNOvv9xd3IJsY3GIb0njijfU6ky/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=dTagoQWbu2QkpqKtVopjYvMcDQM%3D)

**mov R3, R4**:

* R3에 있는 값을 R4로 이동한다. (교환할 값을 저장)

**ll R2, 0(R1)**

* R1이 가리키는 메모리 주소의 값을 R2에 로드한다.

**sc R3, 0(R1)**:

* R3의 값을 R1이 가리키는 주소에 저장하려고 시도합니다. 성공하면 R3는 1로 설정되고, 실패하면 0으로 설정된다. (sc는 Store Conditional 명령어로, 만약 ll로 로드된 이후 해당 메모리 주소가 변경되지 않았다면 저장이 성공한다.)

**beqz R3, try**:

* R3의 값이 0인 경우, try 라벨로 분기한다. (R3가 0이라면 저장이 실패한 것을 의미)

**mov R4, R2**:

* R2의 값을 R4에 이동시킨다.

### 동작 과정:

* 이 코드는 R1이 가리키는 메모리 주소의 값을 원자적으로 교환하기 위한 시도
* 먼저 ll 명령어로 값을 읽어오고, 그 후 sc 명령어로 원자적 저장을 시도
* 만약 저장에 성공하면, R3는 1이 되어 루프를 빠져나가고, 실패하면 R3는 0이 되어 다시 시도