---
title: "[DirectX12] RootSignature"
date: 2024-10-28
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

DirectX 12의 Root Signature과 관련된 다양한 개념.

Root Signature는 GPU 쉐이더가 데이터를 접근할 수 있게 해주는 방식이며, 다양한 방법으로 리소스를 바인딩할 수 있다.

### 1. **Empty Root Signature**

![](https://blog.kakaocdn.net/dna/bw1y3t/btsKl10K1yb/AAAAAAAAAAAAAAAAAAAAAGQHaVZqkM1mjSAkzkw_U99ADtT36Cx9aFCbsse9zfOF/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Pdb61A9nuOWDAln7Z0l5LmZY0hA%3D)

* **유용하지 않을 가능성이 높다.**
* **빈 RootSignature**은 바인딩된 항목이 전혀 없는 루트 서명이다.
* 기본적으로 **Input Assembler 단계**와 최소한의 **Vertex, Pixel Shader**가 활용 가능하지만, 쉐이더가 어떠한 디스크립터에도 접근하지 않는 간단한 렌더링 패스에 사용될 수 있다.
* **블렌드, 렌더 타겟, 깊이 스텐실** 단계도 사용할 수 있습니다.

### 2. **Root Constant (One Constant)**

![](https://blog.kakaocdn.net/dna/RUQyV/btsKmyYgiMA/AAAAAAAAAAAAAAAAAAAAAD0QPveuM-uV3YJVvAZq_rseN4y-TlX11Akktly3Hwou/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9Z0EHe8qJVIZh9mQQtoIYNvmqI0%3D)

* Root Signature에 포함된 단일 값(uint로 보내지만 Hardward쪽에서는 DWARD로 읽는다.)으로, CPU가 명령 리스트를 기록할 때 특정 값을 GPU에 전달한다.
* 매우 가볍고 빠르게 접근할 수 있어, 데이터 크기가 작고 자주 변경되는 경우에 적합하다.

### 3. **Root Constant Buffer View (Root CBV)**

![](https://blog.kakaocdn.net/dna/do6yyD/btsKktjZUKk/AAAAAAAAAAAAAAAAAAAAAERloFnjoHsUzQtmiH-EWcYm77jqpFReMoatrqtJRFgD/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=J1HxWIinJDxkSYhzbJcyB98I8%2Fg%3D)

* **Root CBV**는 Constant Buffer의 주소를 RootSignature에 바인딩하여, 특정 슬롯에 데이터 배열을 전달하는 방식이다.
* CPU에서 설정한 Constant Buffer가 GPU에서 바로 접근할 수 있도록 하는 효율적인 방식이다.

### 4. **Descriptor Table**

![](https://blog.kakaocdn.net/dna/bMqIwC/btsKmv8hZgt/AAAAAAAAAAAAAAAAAAAAAGI8eiFY5wcCRavYmS0mV9Dw3_X8Bim-Z3j1oVDYEbGm/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2Btc8DDtkMROEKDwQJ7DYtqN%2B6H0%3D)

* **Desc Table**은 Desc Heap의 포인터를 Root Siganature에 바인딩하여 여러 리소스를 한 번에 설정할 수 있는 방식이다.
* **CBV, SRV, UAV**와 같은 다양한 리소스의 배열을 한 번에 바인딩할 수 있다. **(Sampler Desce도** 포함할 수 있다.)