---
title: "[DX11] Row-major인가 Column-major인가"
date: 2024-10-11
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### Row-Major vs Column-Major 그리고 DirectX에서 벡터와 행렬의 곱셈

#### 1. **메모리 저장 방식**

* **Column-Major**:
  + 행렬이 메모리에 **열 단위**로 저장됩니다.
  + 예시: 첫 번째 열의 요소들이 연속적으로 저장되고, 그 다음에 두 번째 열의 요소들이 저장됩니다.

* **Row-Major**:
  + 행렬이 메모리에 **행 단위**로 저장된다.
  + 첫 번째 행의 요소들이 연속적으로 저장되고, 그 다음에 두 번째 행의 요소들이 저장된다.

#### 2. **벡터와 행렬의 곱셈:**

* **Column-Major**:
  + [x,y,z,w]∗[변환행렬]
* **DirectX(Row-Major)**:
  + 예시: [변환행렬][x, y, z, w]^T (여기서 T는 transpose\를 의미)

#### 3. **HLSL**

* HLSL에서는 Column-Major방식을 사용하기 때문에 데이터를 보내기 전에 Transpose를 해줘야한다.

#### 4. **DirectX에서의 변환 과정:**

1. **CPU에서**:
   * 행렬은 일반적으로 **row-major** 형식으로 정의된다
2. **GPU로 전송 전**:
   * 행렬을  Transpose하여 **column-major** 형식으로 변환한 뒤 전송한다.
3. **GPU(HLSL)에서**:
   * 전송된 행렬을 **column-major** 형식으로 해석하고, **열 벡터**와 곱셈을 수행합니다.

####