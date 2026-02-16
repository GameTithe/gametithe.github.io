---
title: "[MultiCoreProgramming]Write Cache Coherence(Snooping)-2"
date: 2024-10-15
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

## **Example Write Back Snoopy Protocol**

* 프로토콜 특징:
  + Invalidation 프로토콜을 사용
  + Write-back 버퍼링 캐시 사용
  + 버스의 모든 주소를 Snooping(감시)
* 메모리 블록의 상태 (셋 중 하나):
  + 모든 캐시에서 clean하고 메모리에서 최신 상태 (Shared)
  + 정확히 하나의 캐시에서 dirty 상태 (Exclusive)
  + 어떤 캐시에도 존재하지 않음
* 캐시 블록의 상태 (추적 대상)
  + 공유(Shared): 블록을 읽을 수 있음
  + 배타적(Exclusive): 캐시가 유일한 복사본을 가지며, 쓰기 가능하고 dirty 상태임
  + 무효(Invalid): 블록에 데이터가 없음 (단일 프로세서 캐시에서도 마찬가지)
* 읽기 미스 처리
  + 모든 캐시가 버스를 스누핑하도록 함
* 클린 블록에 대한 쓰기:
  + 미스로 취급됨 (shared 하지 않아도 Memory가 사용중임을 알려야 하기 때문에, clean(처음write할 때)한 곳에 쓸 때는 먼저 쓴다고 bus에 알리고 써야한다.)

![](https://blog.kakaocdn.net/dna/uqUEj/btsJ3PUMAAx/AAAAAAAAAAAAAAAAAAAAACx2Y5te0TnYwUAmtz1XNIxH9FDaLTQYouDNTHWHegqG/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=qQ3OcVFwUJAK6HoULOg0Sk%2BcVGI%3D)