---
title: "[GameEngineArchitecture] Coordinate Spaces"
date: 2025-07-31
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### 

### **Coordinate Spaces (좌표 공간)**

우리는 지금까지 4×4 행렬을 이용해 점과 방향 벡터에 변환을 적용하는 방법을 살펴보았다.

이러한 개념은 강체(rigid object)로도 확장될 수 있는데, 강체에 변환을 적용한다는 의미는 강체 안에 있는 모든 점에 동일한 변환을 적용하는 것과 같다고 볼 수 있다.

예를 들어 컴퓨터 그래픽스에서 객체는 보통 삼각형들의 집합으로 표현되며, 각 삼각형은 세 개의 정점을 갖는다.

이런 경우, **객체에 변환을 적용한다는 것은 모든 정점에 변환 행렬을 각각 적용하는 것과 같다.**

![](https://blog.kakaocdn.net/dna/mXaCt/btsPEtkbfyI/AAAAAAAAAAAAAAAAAAAAAKGKomLFHabFIQ4vYkMO37IUFgklSTo6hXxC89rutH63/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=D4Uyj934gMCEaGkYT4JyL1K6gsg%3D)

위 그림에서는 동일한 점 P를 두 개의 좌표계로 표현한 예를 보여준다.

벡터 PA는 좌표계 A를 기준으로 한 점 P의 위치를 나타내고, 벡터 PB는 좌표계 B를 기준으로 같은 점 P의 위치를 나타낸다.

우리는 앞에서 **점**을 어떤 좌표계의 **원점에서 시작된 벡터**라고 정의했다.

즉, **점(위치 벡터)은 항상 특정 좌표축에 대해 상대적으로 표현된다는 뜻이다.**

### 

### **Model Space**

Maya나 3D Studio MAX와 같은 도구로 오브젝트를 생성하면, 삼각형의 정점들은 **데카르트 좌표계**(cartesian coordinate) 기준으로 정의된다.

이 좌표계를 우리는 **Model Space, O****bject Space**, **Local Space**라고 한다.

**모델 공간의 원점은** 일반적으로 객체의 **무게중심(center of mass)** 이나,**발 사이의 지면 위치** 등 객체 내부의 중심적인 지점에 위치하게 된다.

대부분의 게임 객체는 고유한 방향성을 갖고 있다.

예를 들어 비행기는 **앞면(코)**, **꼬리**, 그리고 **날개**가 있으며, 이는 각각 **전방(front)**, **상방(up)**, **좌/우측(left/right)** 방향에 해당한다. 모델 공간의 좌표축은 보통 이런 자연스러운 방향에 맞춰 정렬되며, 방향을 직관적으로 나타내기 위해 명확한 이름이 붙여진다.

![](https://blog.kakaocdn.net/dna/bGmup4/btsPDC20AUk/AAAAAAAAAAAAAAAAAAAAAPUg00gUtd8LDS8oO_fQTBIfuowKv1cEwDTIGBYpDP_q/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=dMWRx%2BJTS%2BcWVSeTFvKfUjbtdYY%3D)

오른손 좌표계를 사용할 경우에는 보통

+z 축을 **front**

+x 축을 **left**

+y 축을 **up**

으로 매핑한다.

즉 단위벡터 기준으로는 left = i, up = j, front = k가 된다.

**(방향은 임의로 변경이 가능하지만, 한 가지 컨벤션을 정했으면 모든 곳에 일관되게 적용해야한다.)**

### 

### **월드 공간 (World Space)**

**월드 공간**은 게임 세계 내 **모든 객체들의 위치, 방향, 크기**가 표현되는 **고정된 좌표 공간**이다.

이 좌표 공간은 각각의 객체들을 하나의 통합된 가상 세계로 연결해주는 역할을 한다.

**(점은 특정 좌표축에 대한 상대적인 거리라고 했는데, 기준 좌표축을 모두 동일하게 사용한다고 생각하면 쉬울 것이다.)**

**월드 공간의 원점 위치는 임의적이지만, 일반적으로는 플레이 가능한 게임 공간의 중심 근처에 위치시킨다**.

이는 (x, y, z) 좌표가 너무 커졌을 때 발생할 수 있는 **부동 소수점 정밀도 손실(floating-point precision loss)을 최소화하기 위해서다.** => 앞의 내용에서 float는 값이 커지면 정밀도가 떨어진다는 것을 배웠죠?? 여기서 응용이 되네요 굳굳

마찬가지로 x, y, z 축의 방향 역시 임의적이지만, 대부분의 게임 엔진은 **y-up** 또는 **z-up** 컨벤션 중 하나를 사용한다.

(z-up 컨벤션은  게임 세계를 **탑다운(Top-Down)** 방식으로 바라볼 때, **전통적인 2D xy-그래프처럼 보이도록 하기 위해서** 많이 사용된다.)

![](https://blog.kakaocdn.net/dna/rr8bs/btsPELkAf6W/AAAAAAAAAAAAAAAAAAAAAGp7WWT3nMz-KPTgdD3A_0MDE3fjH3tIM51T9Q_7o331/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=J67TRRpZvK6by7UqaPhn4IUrcSg%3D)

제트기의 왼쪽 날개 끝(left wingtip)이

**모델 공간**에서 (5, 0, 0)에 있다고 가정해보자.

**월드 공간에서는** **+x 방향**을 바라보고 있고, **모델 공간의 원점은 월드 공간의 (25, 50, 8)** 위치에 있다고 해보자.

이때 비행기의 앞 방향인 **F 벡터**는 모델 공간에서 +z축인데, 이것이 월드 공간에서 +x축 방향을 향한다면,

**이 비행기는 월드 공간의 y축을 기준으로 90도 회전한 것이다.**

만약 비행기가 월드 공간 원점에 있다면, (5, 0, 0) 모델 좌표는 월드 공간에서 (0, 0, 5)로 표현된다.

하지만 비행기 전체가 (25, 50, 8) 위치로 이동했으므로, 왼쪽 날개 끝은 (25, 50, 8 − 5) = (25, 50, 3)이 된다.

여러 대의 제트기를 추가할 경우**, 각각의 왼쪽 날개 끝은 모델 공간에서는 동일하게 (5, 0, 0)이지만, 월드 공간에서는 각 비행기의 방향 위치에 따라 상이할 것이다.**

### 

### **View Space (or Camera Space)**

**View Space, Camera Space**의 **원점은 카메라의 초점(focal point)에 위치한다. (카메라에 고정된 좌표계)**

축의 방향 설정은 자유롭게 가능하지만, 일반적으로 다음과 같은 컨벤션이 사용된다

**Left-handed( ex. DirectX )**

**+y**는 위쪽

**+z**는 카메라가 바라보는 방향 (화면 깊이 방향)

이 방식은 z 좌표가 **화면 안쪽으로의 깊이**를 의미하게 해준다.

**Right-handed ( ex. OpenGL)**:

**카메라가 -z 방향을 바라본다**

z 좌표는 **음수 방향의 깊이**를 의미한다

![](https://blog.kakaocdn.net/dna/r9tuR/btsPDHpCVsb/AAAAAAAAAAAAAAAAAAAAAD1Pi_CCiS_GzCuZDZOMFB4UQEyaeFhAGOBfgYW_VHZT/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=FPfmlikJZxrBtLxANXOTT1847tA%3D)

.

### 

### **Change of Basis**

게임 및 컴퓨터 그래픽스에서는 **객체의 위치, 방향, 스케일**을 **한 좌표계에서 다른 좌표계로 변환**하는 것이 매우 유용하다.

이러한 연산을 **change of basis**라고 부른다.

### 

### **Coordinate Space Hierarchies**

**좌표계은 상대적이다.**

즉, 3차원 공간에서 어떤 좌표계의 **위치, 방향, 스케일**을 수치로 표현하려면, 그것을 **다른 어떤 좌표계에 대해 상대적으로 명시**해야 한다. **그렇지 않으면 수치 자체가 의미를 갖지 못한다.**

이 말은 **모든 좌표 공간들이 계층 구조(hierarchy)** 를 이룬다는 뜻이다. 각 좌표 공간은 **어떤 다른 좌표 공간의 자식**이며, **그 부모 좌표 공간을 기준으로 정의된다.**  
 **월드 공간(world space) 은 예외로, 부모가 없는 루트 노드(root) 에 해당한다. 모든 다른 좌표 공간들은 궁극적으로 월드 공간을 기준으로 정의된다**

### 

### **Building a Change of Basis Matrix (기준 변환 행렬 만들기)**

어떤 **자식 좌표계 C**에서 **부모 좌표계 P**로 점과 방향 벡터를 변환하는 행렬을 Mcp라고 표기한다. (C to P라고 읽는다)

참고로 이 책에서는 row major 방식으로 설명한다.

![](https://blog.kakaocdn.net/dna/bhjZki/btsPCLTSNjc/AAAAAAAAAAAAAAAAAAAAAB3ZoMZ_uNyiSNHR01Mi0qIldB1DVgHRKT9skF6Ljhnv/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=zZuVGZmOmSsISO30uRYrPd3tt5g%3D)

iC, jC​, kC:  
자식 좌표계의 x/y/z 축을 **부모 좌표계 기준으로 표현한 단위 벡터**

tC: 자식 좌표계의 **원점이 부모 좌표계에서 어디에 있는지**를 나타내는 **위치 벡터**

#### 

#### **Rotation**

자식 좌표계가 **z축을 기준으로 θ만큼 회전**하고, **이동(translation)은 없음**인 상황을 보자.

우리는회전 행렬을 다음과 같이 정의했다.

![](https://blog.kakaocdn.net/dna/bt2z7K/btsPDOoN7rc/AAAAAAAAAAAAAAAAAAAAAAfqDBzagSAuARC3GQcFgbx5Rhh2mZ9OuzztFAV_jpSJ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=tVscbQVwvNQ2SHuDrDmFmgbRF2Y%3D)

iC: [cosθ,sinθ,0]

jC​: [–sinθ,cosθ,0]

kC: [0,0,1]

### 

### **Scaling the Child Axes**

자식 좌표계를 스케일링하려면, 단위 벡터들을 **적절히 스케일링**하면 된다.

예를 들어, 자식 공간을 **2배로 확장(scale)** 하려면, iC,jC,kC​ 벡터들의 **길이를 2배**로 만들면 된다..

### 

### **Extracting Unit Basis Vectors from a Matrix**

기준 변환 행렬을 **세 개의 직교 기저 벡터**와 **하나의 이동 벡터(translation)** 로 구성할 수 있다는 점은 역으로도 강력한 도구가 된다.

즉, 주어진 **affine 4×4 변환 행렬**에서,

자식 좌표계의 기저 벡터 iC,jC,kC​를 추출할 수 있다는 것이다.

**수학 라이브러리가 row vector 기반이라면 행(Row)에서, column vector 기반이라면 열(Column)에서 추출하면 된다.**

이 기술은 아주 유용하다.

우리는 어떤 차량의 **모델 공간 to 월드 공간 변환 행렬**을 갖고 있다 (게임에서 아주 흔한 상황).

이 행렬은 사실상 **기준 변환 행렬**이다.

게임에서 **+z축이 객체가 바라보는 방향**이라고 정해져 있다면,

차량의 전방 방향 벡터를 얻는 가장 간단한 방법은 **해당 행렬에서 세 번째 행(또는 열)을 추출하는 것**이다.

이 벡터는 이미 **정규화(normalized)** 되어 있으며, 바로 사용할 수 있다.

### 

### **Transforming Coordinate Systems versus Vectors**

앞서 설명했듯, 행렬 Mcp는 자식 공간의 점과 벡터를 **부모 공간으로 변환**한다.  
특히, 이 행렬의 4번째 행에는 자식 좌표계의 원점 위치​가 들어있다.

하지만 이 행렬은 **다른 시각**으로도 해석할 수 있다.  
즉, 이 행렬은 부모 공간의 좌표축을 **자식 공간의 축으로 변환하는 역할**을 한다고 볼 수도 있다.

**벡터 중심 시각:** 어떤 점을 **오른쪽으로 20단위 이동**시키는 것

==

**좌표계 중심 시각:** 좌표계를 **왼쪽으로 20단위 이동**시키는 것

![](https://blog.kakaocdn.net/dna/dtqQL5/btsPCppWh0F/AAAAAAAAAAAAAAAAAAAAANdLSaRqAv0N6dDncIbB44CSojHqhu2lOB2iP-HodNtS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=TR0gBCH3wbqmhuKrsIkGrQM0O9Q%3D)

벡터 중심 => 벡터에 행렬이 곱해진다

좌표계 중심 => 축에 행령이 곱해진다.

어떤 방법을 사용하던 지 자유지만, 한 가지 컨벤션을 유지하자

여기서는 벡터에 행렬 곱을 할 것이고, 벡터는 row vector를 사용할 것이다.

![](https://blog.kakaocdn.net/dna/eeejwz/btsPDDnmQep/AAAAAAAAAAAAAAAAAAAAAAFD_wPaiLm0bq74wqwubTwHDv0x4U4OBGFwZKwD6jj4/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=dd75nBkU1iHQilpRuLWvg8L14UM%3D)

### 

### **Transforming Normal Vectors**

**노멀 벡터(normal vector)** 는 일반적인 벡터와는 다르게 특별한 성질을 가진다:

대부분 **단위 벡터(unit length)** 이면서,

항상 **어떤 표면 또는 평면에 수직(perpendicular)** 해야 한다는 제약이 있다.

따라서 노멀 벡터를 변환할 때는,  
**길이와 수직성이 모두 보존되도록 특별한 처리가 필요하다.**

공간 A에서 공간 B로 벡터를 회전시키는 **3×3 회전 행렬**이 Mab​라고 할 때,  
다음과 같은 방식으로 변환된다:

![](https://blog.kakaocdn.net/dna/Mc2qp/btsPE627fS5/AAAAAAAAAAAAAAAAAAAAAI_LySJv1RZts78_DJJhewWo7okMsWq7Q4diaH-G12ls/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=L3Hm8VEk3WiWyYIiN3f1GsktMVU%3D)

**회전 행렬의 역행렬을 전치(transpose)** 한 것을 곱한다.

만약 행렬 Mab에 uniform scale만 있다면 노멀 벡터를 그대로 사용해도 무방하지만, 그게 아니라면 역행렬 + 전치행렬을 잊지말자