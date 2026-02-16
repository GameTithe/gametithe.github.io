---
title: "[실습저장소]육면체 회전(2) + Column major vs Row Major"
date: 2024-09-30
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

OpenGL에서는 column major maxtrix가 사용된다.

## **Column Major**

Column Major는 아래와 같이  
열(Column) 단위로 센다.

![](https://blog.kakaocdn.net/dna/lLZaL/btsJPKz0TGZ/AAAAAAAAAAAAAAAAAAAAADLo_1Yv-Hj6om70zoW3GHamYHYVvFeszo3PSvByUGpS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wOvMjCMfULeLOMTBIkZsw9sqCSA%3D)
![](https://blog.kakaocdn.net/dna/pW9LC/btsJRPTIjQA/AAAAAAAAAAAAAAAAAAAAAO_9A0ZoiCudXggx_i674ohe8ULoKBN9HJkdgTiTa_Ee/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=5mXw8xT4F1HQynVCSMc%2BuO0CZ%2Bk%3D)

m[1].z 는   
1번 행의 z번째

1번째 인덱스(행 단위로 끊긴다)의 3번째 인덱스라고 볼 수 있다

 => m[1][2]

![](https://blog.kakaocdn.net/dna/bjw6h2/btsJQmrByZy/AAAAAAAAAAAAAAAAAAAAABwdNtCDZz31pR_cGVTMd3F8ExwxFzc9CkRvya7nIxUr/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Mfa20JylUHUNTXn5WAe%2B0j94kzs%3D)

보통 C에서는 row major로 하는게 익숙하니

GPU로 넘겨줄 때 Transpose를 해줘서 넘겨주자

## 

## **Row Major**

column과 동일한데 row major는 행단위가 열단위라고 보면 된다.

![](https://blog.kakaocdn.net/dna/Y1yud/btsJSjf07at/AAAAAAAAAAAAAAAAAAAAAIMrcNrxU0VXs2KhC8k1EJaOpLTNN1JsIrf7t92d-y5V/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=bCgWngl1uWziPqFHCW2%2B%2F%2FIxDO0%3D)

## 

## **Basic Pipleine**

![](https://blog.kakaocdn.net/dna/tms4f/btsJScVMmG9/AAAAAAAAAAAAAAAAAAAAABXBCJFQ4zUREfyQ992HJjMvv2LqR2HDd6ut62St6ZF4/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=kCh88Rm%2F1P%2BGJBgdgpaD34boaiY%3D)

OpenGL의 기본 파이프라인이다.

VertexShader와 Fragment Shader로 육면체를 만들었으니 이번에는 Unifor을 사용해볼 것이다.

## **1. 크기 변환**

![](https://blog.kakaocdn.net/dna/cBqTwn/btsJRyxWJ49/AAAAAAAAAAAAAAAAAAAAANWAS212GknDvredCnf2ovWdzD8poiA5EVs2F91WWN_f/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=VMG9dB%2FHf2Embkf83gep%2BjJHt1o%3D)
![](https://blog.kakaocdn.net/dna/cDKfSN/btsJQyyHm39/AAAAAAAAAAAAAAAAAAAAAJcM-ekzMc7IggySkg2rQZNL9af9qeg3raB34vmDELTo/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=RI826%2FHOaiCnykWpHpvcTA%2BylvA%3D)

## **2. Uniform 사용**

![](https://blog.kakaocdn.net/dna/ccr0s1/btsJQgSHZEN/AAAAAAAAAAAAAAAAAAAAAABMo45Oze73PmR1D3COkOSRqY_xg4RBN1350qim_Wfh/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=aImxE8q0lAcxt9NOvQk3ffQP5JI%3D)
![](https://blog.kakaocdn.net/dna/bnQYBp/btsJP88rJ04/AAAAAAAAAAAAAAAAAAAAAErliTfcoH0SHHBSE1G__ll18H38wd8OAJ7-6X3Ww6Gt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=uLGvm%2FJh%2FWHMWtpdgWbaQSSPTi0%3D)
![](https://blog.kakaocdn.net/dna/bapVdu/btsJQb44wX4/AAAAAAAAAAAAAAAAAAAAANSJo6DXocxTJ_beuOi5m_5olCEnNm_3zTK0owqs3-Kl/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fEFy1ldTV3rlx137PsEfuMdV1Yk%3D)

## 

## **2-1 Uniform사용**

![](https://blog.kakaocdn.net/dna/dt5KGo/btsJQyFz0ni/AAAAAAAAAAAAAAAAAAAAAGOdETA-LBoK9BDektdUSlko5tmxMt8vm86ZIVCPW_HP/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Hy86AHXBTNg7xDIPGdTYyFFaHHw%3D)



2-3 Uniform 사용 (회전)

![](https://blog.kakaocdn.net/dna/z7eT9/btsJRZbaCIj/AAAAAAAAAAAAAAAAAAAAABU_OMtusadfk1nL5j8km_w5MKA8r9P8c94m82L7BN7z/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=q1Bf29Z557OS%2BBG270LKBJJz7Xk%3D)