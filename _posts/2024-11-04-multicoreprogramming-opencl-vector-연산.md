---
title: "[MultiCoreProgramming] OpenCL vector 연산"
date: 2024-11-04
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

![](https://blog.kakaocdn.net/dna/bTYxrL/btsKsWTpsM9/AAAAAAAAAAAAAAAAAAAAAHYwbywce9K1tYfC9MU8rzTYJrYIB3-ZQ9FlLn9-Hs0I/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=2DqyJpCjTjDtV33GhRjrttv%2Fdhc%3D)![](https://blog.kakaocdn.net/dna/SGKvQ/btsKspau1mi/AAAAAAAAAAAAAAAAAAAAAP1B--b4pMpBwLZ34Zt5G9TsA0nkOIjItiE41rE2yAjS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=XiHggS7QUPWsmFPKEpHBe6FbrkM%3D)![](https://blog.kakaocdn.net/dna/bcTxpU/btsKtgYaXLg/AAAAAAAAAAAAAAAAAAAAAGItvoZIGrjdUlhHdWDUA4mh8J56Mw9X7SPSL6xbQ7q0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=AYz52CdPez8mMmcBtuhHjkx9Hdg%3D)

Processing Elemet(PE, workItem): 연산을 담당한다.

Compute Unit(CU, workGroup): PE의 집합을 CU라고 생각하면 된다.

CU를 합겨서 OpenCL Devce라고한다. (local memory, global memory도 포함이다.)

Device(GPU)와 Host(CPU)가 Communication을 할 수 있도록 세팅하자

Context는 Queue에 명령을 넣어서 Device와 Communitation을 한다.

(OpenCL runtime이 큐에 들어있는 커널 커맨드를 꺼내어 타겟 디바이스에 알려준다)

기본적인 OpenCL의 흐름도이다.

![](https://blog.kakaocdn.net/dna/bnhhM5/btsKtJMlAT1/AAAAAAAAAAAAAAAAAAAAAJwT32z9am_Ywfa4y_yEVp4bL8mXT8gcg2f8Xz1VbFib/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=DuUG%2FK7vNj%2F3T71glyE%2F0t2rnJA%3D)

순서대로 한다면 vector 연산을 할 수 있을 것이다.

**플랫폼 디바이스에서 정보얻기**

![](https://blog.kakaocdn.net/dna/oBRHQ/btsKswHoAQV/AAAAAAAAAAAAAAAAAAAAANQI-a487YyxYCCh-SF8lqf6x2jRIGQSKBj_wc1Nc3Pv/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=i3QJ7PCcaMNo1CSHGk46Aer5yyg%3D)

**커널코드 실행에 필요한 객체생성**

0. 디바이스 정보가져오기(위 이미지에 빠져있음..)

![](https://blog.kakaocdn.net/dna/d2dbFQ/btsKsfsxYA1/AAAAAAAAAAAAAAAAAAAAABOlehSedU3yuUbZilvIPg_oTUFqHb9RpvdlGv1u71nj/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=w%2BfQvwshPVKNa43240X3%2BfqEH2k%3D)

1. 컨텍스트 생성

![](https://blog.kakaocdn.net/dna/b1YbSy/btsKs0nNQtF/AAAAAAAAAAAAAAAAAAAAAE0RjqPEWiye9QTdX20WtDNQ6qFdnrC-7hcoZ5UB9TK4/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=18W7NNC7E%2BukJvMhpmqG4Vy2Uw0%3D)

2. 커맨트-큐 생성

![](https://blog.kakaocdn.net/dna/LhXDw/btsKsl0fQou/AAAAAAAAAAAAAAAAAAAAADBvVc6mpqvZldczozXb2KF9FeudHPux4FuWH235528u/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=TUToIFxhpNP21plBm8mCMv3wEMA%3D)

3. OpenCL프로그램 컴파일

![](https://blog.kakaocdn.net/dna/92Qqw/btsKtgRtf3h/AAAAAAAAAAAAAAAAAAAAAN8sl7yqhfgGPU0XjfqTUd8ihVdGUlklSQ4yF2WV6yym/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2BolAoxo1CuiRo48npp4d3eicB68%3D)

4. 메모리 오브젝트 생성

![](https://blog.kakaocdn.net/dna/bVMShY/btsKtHOCkgi/AAAAAAAAAAAAAAAAAAAAAOpvugJIHXkFmd33y50uoVwRQvC2lD_N7EVlrCr90koX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=5zwSB3m0S%2FHOOR14dgGXdr7yPcU%3D)

**커널코드실행**

1. 입력 데이터를 글로벌 메모리로 보냄

![](https://blog.kakaocdn.net/dna/buQMEq/btsKtohEG10/AAAAAAAAAAAAAAAAAAAAABn4A5sEbJw-5pATw5Bci1SB4NADDBGcbMxAhTXg-xuS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ete%2FHk27NLS6RMmGzD6y%2Bui5Ow4%3D)

2. 커널 실행

![](https://blog.kakaocdn.net/dna/bgcSPS/btsKtVZ5Cbq/AAAAAAAAAAAAAAAAAAAAACQyx8POoxT8teZ0X52i94zFits3NFWq_b3YM-4MHUKh/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=SZmqbZ1mZ7NvqW5PbpEbJMOV9EY%3D)

3. 출력데이터를 글로벌 메모리에서 받음

![](https://blog.kakaocdn.net/dna/xx8pS/btsKtiIyM5R/AAAAAAAAAAAAAAAAAAAAAJ19e0PbVaY3ph6akWiuwf1bI8EIDBwj5fhTFCq8axdu/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=MVmdknp1BBBwDk0FyRIUj4AiPSs%3D)

여기까지는 kernel이 아래와 같을 때, Device에 값을 넣기만 해주는 코드이다.

input + input2 = output을 할 수 있도록 코드를 작성해보자

![](https://blog.kakaocdn.net/dna/bCTxye/btsKtfZrdhg/AAAAAAAAAAAAAAAAAAAAAJ95AuUPed4aLeu5EaP24zAxJsUKtiKzAbvF69NgExz8/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=7xuYQEfTZLxyPW5Bjf5I5JnENUg%3D)
![](https://blog.kakaocdn.net/dna/bqC6xZ/btsKseNUp2x/AAAAAAAAAAAAAAAAAAAAAMfJHI0D8RbeG3t58S0muOLxFuakULbivkeqzUcPyrUN/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=XapO11weUniCRU9tYjzVN6iMhGo%3D)

이렇게! 합하면 위의 결과의 2배인 것을 볼 수 있다

![](https://blog.kakaocdn.net/dna/TkU6Y/btsKtref6t0/AAAAAAAAAAAAAAAAAAAAAILyKTtc6XORkXeIp9DzSuHmEOF0DsaOjv59WqBAfjrg/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=NxCnRvyviLmqLO5dVYPbZ7XFbF8%3D)