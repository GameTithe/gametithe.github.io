---
title: "[CUDA기반 GPU병렬 처리 프로그래밍] CUDA프로그램의 기본 흐름"
date: 2024-10-04
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

CUDA프로그램

* Host 코드
* Device 코드

GPU가 사용하는 메모리는 Device메모리이지만, 모든 데이터는 기본적으로 호스트 메모리에 저장되어있다.

순서

1. Host메모리에서 Device 메모리로 입력 데이터 복사

2. 커널 호출을 통해 GPU연산을 시작한다. 모든 데이터는 디바이스 메모리에서 관리한다.

3. Device메모리에서 Host메모리로 결과 데이터 복사

## 

## **1. Device 메모리 할당**

Device 영역에 동적할당은 cudaMalloc을 사용하면 된다.

cudaMalloc 후에 print를 해보면

하지만 아래의 코드는 오류가 날 것이다.

![](https://blog.kakaocdn.net/dna/1fWLN/btsJTCVo7sK/AAAAAAAAAAAAAAAAAAAAAGhpMXDt3Pkz3t__94N0XiMUBGExDWa2E39S6DNICW4s/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=T58yng2v0r4y3jmCoyM0p236s6Y%3D)
![](https://blog.kakaocdn.net/dna/dt4LQV/btsJSn5W2kx/AAAAAAAAAAAAAAAAAAAAANTBIO-dAyos2Qke8EnFunrFQOokhBc9FLpc-3bwU6MT/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=bIno410b1ie0Ktr0OgoDZV35m%2FM%3D)

(인덱스 0에 값을 넣어줘도 오류가 나는 것은 똑같다.)

![](https://blog.kakaocdn.net/dna/bHXJM0/btsJThjE34F/AAAAAAAAAAAAAAAAAAAAAIRjQrwQLuvmnd1czdtkMQNrZdHTsu5PM5a6c8I_mB5u/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=SZXmS928myQtyjJyG89MfTiiIwc%3D)

이유는 **Host코드에서 Device데이터에 접근하려고 하는 것이기 때문이다.**

## 

## **2. Device 메모리 해제**

![](https://blog.kakaocdn.net/dna/AylJ3/btsJUbJB9vt/AAAAAAAAAAAAAAAAAAAAAEBLd4hjueq7MHYR7QYxMaGwivrYTiB4H4E56MV6AZ7q/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=5pYGQcIH8oABi2M5UMDcqHcB24Q%3D)
![](https://blog.kakaocdn.net/dna/dpAeje/btsJSQGDPWE/AAAAAAAAAAAAAAAAAAAAAKE9aBKUUf29E-_RBonc0020OMp0OMtbFT9nItNEEoFY/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KTyiRux2TVJjl3bCuBkO8Yxi40U%3D)

**c에서 동적할당 후 free를 하는 것과 같이 cuda도 직접 동적할당 해제를 해줘야한다.**

**3. Device 메모리 초기화**

![](https://blog.kakaocdn.net/dna/cujCgQ/btsJUcBKkX9/AAAAAAAAAAAAAAAAAAAAAOPJToLC6clx-ZDbcuA5RWqQzlC6nJ1Pt2ZIpn9mkt_J/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=IXiQg3iKKvOavWAX8iFneTZjPSw%3D)

* **void\* devPtr :** 초기화 할 주소
* **int value:** 초기화 할 값
* **size\_t count:** 초기화할 메모리 크기

![](https://blog.kakaocdn.net/dna/bm8hGY/btsJUmKXZX1/AAAAAAAAAAAAAAAAAAAAAC2gExCDOk9VCz4C285fuwYaiLUNDLG0_FFMf8bKlTxC/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=cd%2BsOc0BTHq7ZrXgaPNqzaF7YTs%3D)

4. 에러코드 확인

cudaGetErrorName

![](https://blog.kakaocdn.net/dna/bT8eSP/btsJSHiQk8q/AAAAAAAAAAAAAAAAAAAAAIKz0ytl4H1CCtEDN_5R83BmIXi_T6sImMHcmTdZS70i/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=HAP8C0UaYurwc2wDKHygyg7Axd8%3D)

5. 장치간 데이터 복사

cudaMemcpy()

![](https://blog.kakaocdn.net/dna/bMk1ed/btsJSK0NQDR/AAAAAAAAAAAAAAAAAAAAANgVHF_R4KMGqhPuIKU532U8PB0XSL_lrXgqTUkXSato/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1qFrCTj85AYotexoU2GTB2qUtFU%3D)

dst와 src는 직관적이다.

src에서 dst로 데이터를 옮기는 것이다. 근데 dst,src가 device인지 host인지 명시를 해줘야한다.

그것을 cudaMemcpyKind로 해주는 것이다.

![](https://blog.kakaocdn.net/dna/pvDRv/btsJTJmtMy5/AAAAAAAAAAAAAAAAAAAAALNp2rrg6VaNnUA_Y8iGd8BNPN3Rm6q1Vt9SmxC2RY8m/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ydqvzDC%2FY%2B5bqj34zR4mqvFt%2FiI%3D)

## +

#### **1. cudaMemcpy2D**

cudaMemcpy2D는 2차원 메모리 공간을 복사할 때 사용된다. (ex 이미지, 행렬)

* **dst**: 데이터를 복사할 목적지 주소.
* **dpitch**: 목적지에서 한 행(row)을 저장하는 데 사용되는 실제 메모리 너비(바이트 단위). 데이터는 실제로는 연속적이지 않고 메모리에서 padding이 있을 수 있기 때문에, pitch는 데이터를 복사할 때 이를 고려하게 해.
* **src**: 원본 데이터가 있는 주소.
* **spitch**: 원본 데이터에서 한 행을 저장하는 데 사용되는 메모리 너비.
* **width**: 복사할 데이터의 가로 길이 (바이트 단위).
* **height**: 복사할 데이터의 세로 길이.

#### **2. cudaMemcpy3D**

cudaMemcpy3D는 3차원 메모리 공간을 복사할 때 사용된다.

cudaMemcpy3D는 cudaMemcpy3DParms 구조체를 사용해 파라미터를 전달한다.

![](https://blog.kakaocdn.net/dna/bgsh5n/btsJUNIcb5F/AAAAAAAAAAAAAAAAAAAAABBzdn0TB_XyWeICAr3S0jW1C47Yv0gQ2qAU91Fh8T3t/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=vWCNS5c7L8YsqBdhRRrSYLrz14c%3D)
![](https://blog.kakaocdn.net/dna/b2aZWR/btsJUiaQFGp/AAAAAAAAAAAAAAAAAAAAAJpVt5D5K5kb4OtazXxzmDKZ2ZXMBM4nv9e5eokc4sUq/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=XIAkD4Ks7r8qEX61tQG8ktzDGNQ%3D)

* **srcArray**: 원본 데이터가 있는 3차원 배열
* **dstArray**: 데이터를 복사할 3차원 배열
* **extent**: 복사할 3차원 범위를 지정하는 구조체로, 가로, 세로, 높이 정보를 포함한다.
* **kind**: cudaMemcpyKind(위에 있다

## **실습**

**1.메모리 할당/해제**

![](https://blog.kakaocdn.net/dna/mNCo1/btsJT9dYo39/AAAAAAAAAAAAAAAAAAAAADH9zqDUk2a2-ILtx3gaX9gHpPYpXMc-45yO43N2Hta1/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=v7bTs0fWMo0LR1waq3LE3AgkKhU%3D)

![](https://blog.kakaocdn.net/dna/73MBx/btsJTqALB3t/AAAAAAAAAAAAAAAAAAAAAIjQ1ouQYDBmnFO02ffhOcZKgB-NsIKuQnJ8kpMCoNzH/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nWZsHqJ8%2B8CgbEac2kropdfgH9s%3D)

**2. 데이터 복사**

![](https://blog.kakaocdn.net/dna/8O9T2/btsJTFR1SxS/AAAAAAAAAAAAAAAAAAAAAHOkfb3ztAIgtNickVddvsVSgyRSc7FyP-SJmiujvzCb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1zuFKdDvxAjnUWEqunlG8igZmcE%3D)
![](https://blog.kakaocdn.net/dna/bFpqNX/btsJTSDy1rT/AAAAAAAAAAAAAAAAAAAAAKue_6UdZty55a4VKvI_SI1mficU6dkHLydhaPUgEPI7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=k6lfVydAHtb5kEKvzzwUZo48W3c%3D)