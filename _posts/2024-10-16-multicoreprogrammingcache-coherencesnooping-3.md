---
title: "[MultiCoreProgramming]Cache Coherence(Snooping)-3"
date: 2024-10-16
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

## **Implementation Complications**

### Write Races

1. 캐시 업데이트 제약

* 버스를 획득하기 전까지 캐시를 업데이트할 수 없다.
* 그 이유는 다른 프로세서가 먼저 버스를 획득하여 동일한 캐시 블록에 write할 수 있기 때문이다.

2. Two Step Process

* arbitrate(중재) for bus
* bus에 miss를 배치하고 작동 완료

3. bus 대기 중 miss 발생 시:

* miss를 처리하고(필요시 invalidate), 재시작한다.

4. 분할 트랜잭션 버스

* 버스 트랜잭션이 원자적(atomic)이지 않기 때문에 하나의 블록에 대해 여러 미완료 트랜잭션이 가능하다.
* 여러 miss들이 interleave(끼어들수)될 수 있어 두 캐시가 동시에 Exclusive 상태의 블록을 가져갈 수 있습니다.
* 하나의 블록에 대한 다중 미스를 추적하고 방지해야 합니다

### intervention과 invalidation를 반드시 지원해야한다.

Implementin Snooping Caches

* 멀티프로세서 버스 요구사항
  + 프로세서들은 bus에 연결되어있어야 하고, 주소와 데이터에 접근 가능해야 한다.
  + coherency을 위한 새로운 명령어가 필요하다.(read와 write 외에도)
  + 프로세서들은 지속적으로 주소 버스를 snooping한다.
    - broadcasting 되고 있는 정보의 주소가 태그와 일치하면 invalidate하거나 updat한다
* 캐시 태그 문제
  + 해결 방법1: L1 캐시를 위한 중복 태그 세트를 만들어 CPU와 병렬로 확인 (Duplicate를 한다.)
  + 해결 방법2: L2 캐시를 이용한다. L2 캐시가 L1 캐시와 inclusion property 관계를 유지하도록 함
    - L2의 블록 크기와 associativity(연관성)이 L1에 영향을 미침

## 

## **Limitations in SMP and Snooping Protocols(SMP의 한계점)**

* 단일 메모리의 한계와 다중 메모리 뱅크
  + 단일 메모리로는 모든 CPU의 요구를 수용하기 어렵다 -> 다중 메모리 뱅크 사용
  + 메모리 접근 병목 현상이 발생할 수 있다. ->여러 메모리 뱅크를 사용해서 접근을 가능한다.
* 버스 기반 멀티프로세서의 한계와 해결책
  + 단일 버스는 일관성 트래픽과 일반 메모리 트래픽을 모두 처리해야 합니다. => Multiple buses사용
  + 이는 버스의 대역폭 제한으로 인한 성능 저하를 초래할 수 있습니다. =>interconnection network(cross bar or small point-to-point)사용
* Opteron   
  + 각 듀얼 코어 칩에 메모리가 직접 연결된다. 로컬 메모리 접근 시간을 크게 줄여준다.
  + 최대 4개의 칩까지 점대점 연결을 지원한다.
  + 프로세서 간 직접 통신이 가능해져 데이터 전송 효율성이 향상된다
  + 원격 메모리와 로컬 메모리의 접근 지연 시간이 유사하다

## 

## **Performance of Symmetric SMP**

1. **Uniprossesor cache miss traffic:** 일반적인 캐시 미스로, 단일 프로세서 시스템에서도 발생한다.

2. **통신으로 인한 트래픽**

* 여러 프로세서 간의 데이터 공유로 인해 발생한다.
* 이로 인해 캐시 invalidations와 추가적인 캐시 미스가 발생합니다.

기존의 3C(Compulsory, Capacity, Conflict)미스에서 새로운 유형의 미스가 추가된다.

네 번째 C: Coherence Miss

* Compulsory: 처음 데이터에 접근할 때 발생
* Capacity: 캐시 크기가 부족해서 발생
* Conflict: 캐시 구조로 인해 발생
* Coherence: 멀티프로세서 환경에서 캐시 일관성 유지를 위해 발생
  + X블럭이 a,b,c,e (word, 단위)를 포함한다고 가정하자.
  + True Coherence(True Sharing Miss)   
    - 공유 블록의 **a(word, 단위)에 쓰기 작업하기 위해서 a가 속해 있는 블럭 전체를 무효화**
    - 다른 processor가  **a(word, 단위)에서 작업하기를 원함**
    - True Coherence 발생
  + False Coherence(False Sharing Miss)
    - 공유 블록의 **a(word, 단위)에 쓰기 작업하기 위해서 a가 속해 있는 블럭 전체를 무효화**
    - 다른 processor가**b(word, 단위)에서 작업하기를 원함**
    - False Coherence 발생
* Processor의 수가 많아 질 수록 많이 발생한다.

![](https://blog.kakaocdn.net/dna/cnj9K4/btsJ7boYEse/AAAAAAAAAAAAAAAAAAAAAAAXk1EB_VZ8OR47Awzmg-qq8So4jCoz6dIgWHNUt5hZ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=IDFTrSiOdhaItRQvA499Y0tCRyk%3D)