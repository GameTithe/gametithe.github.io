---
title: "[논문정리] Taichi: A Language for High-Performance Computation on Spatially Sparse Data Structures"
date: 2025-03-12
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

## **1. Introduction**

희소성을 효과적으로 활용하기 위해서 광범위하게 연구중이다. 하지만 이러한 데이터구조에 대해 고성능 코드를 작성하는 것은 불규칙성(irregulatity) 때문에 까다로운 일이다.

첫 번째, 순회구조를 순진하게 탐색하면 필수 계산보다 1~2배 더 많은 클록 주기가 필요할 수 있다.

두 번째, 효율적인 병렬화를 위해서 load balancing을 보장해야된다.

세 번째, inactive(비활성화) 요소에 접근할 때는 메모리 할당과 희소성 유지를 신경써야된다.

( 희소성 유지란 행렬에 sparse한 부분이 많을 수 있으니, 필요한 데이터만 사용하자는 의미라고 합니다.

ex) if (grid[x][y][z] == nullptr) 일 때 grid[x][y][z]  에만 접근)

이런한 데이터 구조를 가진 라이브러리들은 high-performace를 보장하는 것이 쉽지 않다.

왜냐하면 인터페이스가 여러번 호출되면 계층구조를 중복 순회하면서 불필요한 비용이 발생되기 때문이다. 또한 data racing, pointer aliasing등의 문제 때문에 general-purpose 컴파일러는 라이브러리 함수간 호출 최적화를 실패하는 경우가 많다.

그러나 우리는 코드도 high level로 지원하고, 속도도 매우 빠른 taichi를 구현하였다

우리의 모델은 **물리 시뮬레이션과 렌더링에서 사용되는 다양한 데이터 구조**를 표현할 수 있다. ( multi-level sparse grids, particles, dense and sparse matrices 등등) 하지만 k-d 트리 처럼 깊이가 가변적인 구조는 직접적으로 모델링하지 않는다.

#### **우리가 기여한 것**

**1. 계산과 데이터 구조를 분리했다.**  
어떤 데이터 구조를 사용하던 뒤에서 어떻게 연산되는 지 사용자는 신경을 쓰지 않아도 된다.

**2. 미니 언어를  통해 필요한 데이터 구조를 만들 수 있다.**

**3. 컴파일러가 알아서 성능을 높여준다.**

**4. 최신 그래픽스 알고리즘으로 테스트 해봤는데 성능이 좋다**

## **2. 목표 및 설계**

대부분의 3D task에는 희소성 패턴, 공간 일관성이 나타난다. 우리는 빈 공간에 쓸데없는 계산 자원을 낭비하지 않으면서 공간적 희소성(spatial sparsity) 을 효과적으로 모델링하여, 공간적 일관성을 최대한 활용하는 고성능 프로그래밍 언어를 개발하는 것을 목표로 한다.

**우리의 목표는 아래 4가지이다.**

**1. 표현력**

Taichi는 **희소 데이터 구조 내에서 임의의 요소에 자유롭게 읽기/쓰기**가 가능하며, **분기(branch)** 와 **반복(loop)** 과 같은 구문도 지원한다.

**2. 성능**

**메모리에 친화적이고 병렬화에 적합한 데이터 구조**는 **작업(task)** 과 **하드웨어(hardware)** 에 따라 다르기 때문에,  
**하나의 데이터 구조만 제공하는 기존 라이브러리로는 모든 성능 문제를 해결할 수 없었다.**

**3. 생상성**

****컴파일러가 자동으로 최적화된 코드를 생성한다.**  
**Taichi는 복잡한 데이터 구조를 사용한 대규모 물리 시뮬레이션을 단 몇백 줄의 코드****로 작성할 수 있는 최초의 시스템이다**.**

**4. 이식성**

다양한 하드웨어 환경에 대해 자동으로 최적화된 코드를 생성해야 한다.

## 

## **2.1 설계 결정 (Design Decisions)**

**1. 데이터 구조와 계산 분리**

사용자는 high-level 코드로 계산을 작성해야 한다.

동시에 계산 코드를 바꾸지 않고도 다양한 희소 데이터 구조를 실험할 수 있어야 한다.

=> 데이터 표현 방법은 일관되게 하고, 내부 알고리즘만 바꿀 수 있어야 한다

데이터 표현 방법은 cartesian indexing으로 추상화하였다

**2. 빌딩 블록으로써 표준 그리드**

**우리 시스템의 기본적인 데이터 구조는 regular grid 형식이다. regular grid는 1차원으로 flat하게 변경하는 것이 쉽기 때문에 선형 메모리 저장 체계를 사용하는 최신 아키텍처와 궁합이 잘 맞다.**

**3. 하이라키 구성을 통한 데이터 구조 설명**

mini language를 통해서 데이터 구조 하이라키를 설정할 수 있다.

**4. 고정된 데이터 구조 하이라키**

컴파일러의 최적화를 쉽게하고 메모리 할당을 쉽게하기 위해서 하이라키는 컴파일 단에서 정한다.

**5. 희소 반복자의 Single-Program-Multiple-Data**

희소 반복자는 active element에 대해서만 병렬 for 루프를 돈다.

**6. 자동으로 최적화 코드 생성**

컴파일러는 자동으로 다음과 같은 최적화를 한다.

1. 지역성 최적화

2. 일단성 있는 접근으로 access 중복 줄이기

3. 자동 병렬, 메모리 할당

사용자는 백엔드에서 작동될 하키텍처만 고르면 된다.

## 

## **3. Taichi 프로그래밍 언어**

물리 시뮬레이션과 이미지 처리에서 자주 사용되는 2D라플라스 연산자로 예를 들어보겠다.

![](https://blog.kakaocdn.net/dna/E9UAX/btsMG9WhPlX/AAAAAAAAAAAAAAAAAAAAAHeogbNnjxh3CBcDyDGw6FPiE_2x_V-XlfImTjK4HEQ3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GVSwW7F%2F3dZPi8nTLrxk9aTBSXs%3D)

### **3.1 계산 정의**

데이터 구조와 계산을 분리하기 위해, 우리는 데이터 구조를 다차원 인덱스에서 실제 값으로의 매핑(mapping) 으로 추상화했습니다.  
**예를 들어, 2D 스칼라 필드 u 에 대한 접근은 내부 데이터 구조가 무엇이든 항상 u[i, j] 와 같은 인덱싱 방식으로 접근합니다.**

고수준 인터페이스와 비슷하지만,****우리의 컴파일러는 이러한 접근을 분석하여 중복을 최소화한 코드를 자동 생성한다.****

계산 kernel은 주로 active element를 순회하면서 계산하도록 정의된다. sparsity를 효율적으로 사용하는 방법이다.

앞에서 말했던 라플라스 연산자로 예를 들어보자

```
Kernel(laplace).def([&]() {
    For(u, [&](Expr i, Expr j) {
        auto c = 1.0f / (dx * dx);
        u[i, j] = c * (4 * v[i, j] - v[i+1, j] - v[i-1, j] - v[i, j+1] - v[i, j-1]);
    });
});
```

위와 같은 상황이라면 u[i,j]가 active element가 되는 것이다.

컴파일러가 **자동으로 희소성을 관리한다.**

**비활성 요소를 읽으면 기본값 (예: 0)** 반환하고,

**비활성 요소에 쓰면 자동으로 메모리 할당 및 활성화**

**Taichi가 CUDA나 ispc 같은 SPMD 언어와 다른 점:**

**1. 병렬 희소 For 루프**

**2. multi-dimensional sparse array 접근자 (Multi-dimensional sparse array accessors)**

ex) grid[i][j][k]

**3.** **컴파일러를 위한 스케줄링 최적화 힌트 제공**

### 

### **3.2 내부구조를 계층적으로 정의하기**

계산코드 작성을 마치면, 사용자는 내부 데이터 구조 계층을 정해야된다. 데이터 구조를 정의하는 것은 두 가지 수준의 선택을 포함한다.

**매크로 수준 (Macro Level):**

* 데이터 구조 요소들이 어떻게 중첩(nest) 되는지,
* 희소성(sparsity) 을 어떻게 표현할지 결정.

**마이크로 수준 (Micro Level):**

* 데이터가 어떻게 묶여(grouped) 저장될지 결정.

**Structural nodes and their decorators**

우리 언어는 structural node(계층구조를 구성하는)와 decorators를 제공한다.

구조 노드 (Structural nodes)

|  |  |
| --- | --- |
| **dense** | 고정 길이의 연속된 배열 (고정된 크기). |
| **hash** | **해시 테이블**로 활성 좌표를 메모리 주소로 매핑. **희소성 높은 경우 적합**. |
| ****dynamic**** | 가변 길이 배열(최대 길이 미리 정의). std::vector 역할 |

hash:

전체 128 x 128 x 128 grid이고, 활성 셀은 200개일 때(0.1% 만 사용)

density로 하면 메모리 낭비가 심하다. hash도 활성셀 정보만 저장하자.

노드 데코레이터 (Node decorators)

|  |  |
| --- | --- |
| **morton** | 메모리 상에서 **Z-order curve (Morton 코드)** 로 데이터 재정렬, **공간 지역성 향상**. (dense 전용) |
| ****bitmasked**** | 각 자식에 대해 **1비트 마스크**로 희소성 유지. (dense 전용) |
| ****pointer**** | 전체 구조 대신 **포인터 저장**으로 메모리 절약 및 희소성 유지. (dense, dynamic 전용) |

**데이터 구조 선택의 트레이드오프**

**hash:**

* 속도가 느리기 때문에 (50 cpu cycles),  매우 희소한 데이터에 적합하다(활성비율 0.1% 정도)

**비트마스크 + dense**:

* 빠른 활성화/접근.
* **희소도가 높을 때는 비효율** (마스크도 메모리 차지).

### **Defining Hierarchy**

사용자는 데이터 구조 구성 요소를 임의로 조합하여 원하는 계층을 형성하고, 다양한 트레이드오프(trade-off)를 탐색할 수 있다.

컴파일러는 sparse data에 대해서 어떻게 커널을 계산할 지 합성(synthesize)할 수 있다.

![](https://blog.kakaocdn.net/dna/dxeGuW/btsMHpETweu/AAAAAAAAAAAAAAAAAAAAAKZ2agOgL8XiwNcE0YxJ3gp5vOhr0bbAhHoqcNw_pMR8/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=i%2BvB5YDqhBy8gsBtEGWgYTaaOkc%3D)

프로그래머가 hash table, dense array와 같은 구성 요수를 중첩(nesting)하여 데이터 구조를 정의할 수 있다.

커널은 **내부 데이터 조직 방식과 상관없이** leaf element에 대한 **반복**으로 정의됩니다.

**leaf blocks은** leaf element의 묶음이며, **저장 및 계산 작업의 가장 작은 단위이다.**

**예를 들어, 아래의 코드와 같이 2개의 고정된 사이즈 2D dense array  u, v가 있다.**

**위코드는 구조체 배열 방식이다. (SOA: Structure of Array )**

![](https://blog.kakaocdn.net/dna/bmaNz7/btsMEP6suOC/AAAAAAAAAAAAAAAAAAAAAHBn7XRS7IcPmvRikfcGtgS_9j0iVNrG0ChMvfZc8YrM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xbItt7MdQjMqH1QtnkNmpP%2Bnjao%3D)

**SOA형식을 AOS**(AOS: Array of Structures)** 로 바꾸기 위해서는 아래와 같이 하면된다.**

**로 바꾸려면 아래와 같이하면 된다.**

![](https://blog.kakaocdn.net/dna/V3Cez/btsMGNsr3gf/AAAAAAAAAAAAAAAAAAAAADYyV6TIUszD9-H-Uhuapzo87zxPj6SralWfL_EkuA6m/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nzlEj6LVR67u6nCZVqu8POhbzyY%3D)

사용법인데 아래 정도의 차이같다.

```
place(u), place(v) VS place(u,v)
```

AOS 방식에서는 **u**ij ,**vij**의 데이터가 서로 인접한 위치에 존재한다.

SOA 방식에서는 **u**ij**, u**i,j+1**이** 인접하고 vij와는 멀리 떨어져있다.

이 차이는 유의미한 속도차이를 발생시키니 주의하자.

우리는 structual nodes들을 top-down 순서로 중첩시켜서 계층 트리를 만들 수 있다.

최상위는 hash, 두 번째는 pointer 세 번째는 fixed array 로 만든 것이다.

![](https://blog.kakaocdn.net/dna/k6zsg/btsMG8wXaFW/AAAAAAAAAAAAAAAAAAAAADqlaBULelzzTAYhncW6Fut3lbW5KTk6NGOaFlQY_3tW/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=cmtcHupPsdTk5CPJA0bcXC0o%2BuM%3D)

또한 multi global variables 를 둘 수 있을 뿐만 아니라, 자식으로 multi structual nodes를 가질 수 있다.

아래 코드를 보면 global 변수를 여러 개 선언한 것을 볼 수 있고,

dense array와 dynamic array를 섞어서 사용할 수 있다.

![](https://blog.kakaocdn.net/dna/bhFBXF/btsMHdSwH81/AAAAAAAAAAAAAAAAAAAAAJj4KW-dX97eL4EaZ-3R1b5L0_tyooAiu_h3_QKAub_U/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3VBjCfcllieUQprnf5%2FE6F5jIj8%3D)
![](https://blog.kakaocdn.net/dna/Kfoxk/btsMF4WjL91/AAAAAAAAAAAAAAAAAAAAAMDkKCGGeYhFH-S2J2h-SNOsrNtO7chb9f5NJqzWTgFo/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=H8QmgjSWvSdkY6h5Egvr7Bp7ttc%3D)

C++ 코드로 보면 다음과 같다고 볼 수 있다.

![](https://blog.kakaocdn.net/dna/bUom5v/btsMIbGqbHf/AAAAAAAAAAAAAAAAAAAAANGyowuP2ScCC88ByaXhtQcfnQXp7oUz7TzPJKZTvCCP/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=v42G6inzH%2F5couRubAwAGRMX%2Ffo%3D)

structure node의 type은 간결하지만 다양한 데이터 구조를 표현할 수 있습니다.

### 

### **4. Domain-Specific Optimizations**

우리는 세가지 방법을 최적화해서 오버헤드를 줄입니다.

**1. 캐시 외부 접근**

**2. 데이터 구조 계층 탐색**

**3. 인스턴스 활성화**

atomic연산이나 spinLock은 본질적으로 느릴 뿐 아니라 직렬화되어있다.

캐쉬 로컬리티, 중복(redundant  접근의 제거(reduction), 자동 병렬화 및 벡터화를 통해 고성능을 낼 겁니다.

### **4.1 Scratchpad Optimization through Boundary Inference.**

**Scratchpad는 데이터 재사용**이 가능한 경우 **메모리 대역폭 감소**와 **지연(latency) 감소**를 위해 쓰는 **빠른 로컬 데이터 영역이다.** 하지만 **직접 scratchpad를 다루는 것은 복잡하고 오류 가능성**이 높다.

**우리는 커널(kernel)** 내에서 **Cache(v)** 명령어를 사용하면 **자동 scratchpad 할당을** 지원한다.

예를 들어 **3x3 이웃 값**이 필요한 **Laplace 커널**에서, 필요한 데이터만큼 자동으로 scratchpad 메모리가 할당된다.

자동으로 경계를 추론하는 것이 가능하지만, 굉장히 까다롭기에 모든 경우에 가능한 것은 아니다.

그래서 AssumeInRange로 범위를 제공해줘야된다.

semi-Lagrangian advection kernel 이다.

![](https://blog.kakaocdn.net/dna/QDN68/btsMHQp7ehZ/AAAAAAAAAAAAAAAAAAAAAG8Q7dU4ZLK6LnnzXVsHhrN-SV07g9l6GA7aucZ6FwM0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=bP3atf7RMWNwPnmWtWO6RO%2BXt6k%3D)
![](https://blog.kakaocdn.net/dna/s2CU2/btsMHU0ds1x/AAAAAAAAAAAAAAAAAAAAAHIpj1cXKqY3cF676wQe1MTIh-9O47l-Jlw7SPF2Kh5q/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=gNwmGAPfI8Wt22aFbfNCJ0KfJdo%3D)

또한 GPU는 L2캐쉬를 사용하는게 디폴트이기에  **NVIDIA GPU**에서 \_\_ldg() 명령어를 통해 **글로벌 변수 V를 L1 캐시에 강제로 로드할 수 있다.**

---

### 4. **AssumeInRange로 수동 범위 제공**

* 컴파일러가 경계를 추론하기 어려운 경우, 사용자가 직접 범위를 제시 가능.
* 예시:

  c++

  복사편집

  backtrace\_i = AssumeInRange(i, {-2, 3}); // i-2 <= backtrace\_i < i+3 backtrace\_j = AssumeInRange(j, {-2, 3}); // j-2 <= backtrace\_j < j+3
* **반드시 이 범위 안에 값이 존재한다고 가정**하도록 컴파일러에게 알려줌.
* 사용 예: **semi-Lagrangian advection** 같은 커널에서 경계 미리 지정.

---

### 5. **GPU에서의 적용**

* **현재는 GPU에서만 scratchpad 최적화 적용**.
* 이유:
  + **GPU 공유 메모리**를 이용한 scratchpad는 **성능 향상에 매우 효과적**.
  + **CPU는 이미 L1 캐시가 비슷한 역할**을 하므로 성능 차이가 크지 않을 수 있음.

---

### 6. **추가 기능: CacheL1**

* GPU 전용 **CacheL1(v)** 제공.
* **NVIDIA GPU**에서 \_\_ldg() 명령어를 통해 **글로벌 변수 V를 L1 캐시에 강제로 로드**.
* 참고:
  + NVIDIA GPU는 기본적으로 **L2 캐시** 사용.
  + L1 캐시는 하드웨어가 자동 관리 → **컴파일 타임 경계 추론 필요 없음**.

---

## ✅ 📌 한 줄 요약:

> **Taichi는 Cache(v)와 경계 추론(혹은 AssumeInRange)을 통해 자동으로 scratchpad 최적화를 수행하며, 특히 GPU에서 성능을 극대화한다.**

### **4.2 Removing Redundant Accesses**

**라플라스 연산자(Laplace operator)** 를 다시 생각해보자.  
이번에는 그림 2와 같은 **3단계 계층 구조(three-level data structure)** 를 접근한다고 가정합니다.

![](https://blog.kakaocdn.net/dna/Nheb3/btsMFIlZjpr/AAAAAAAAAAAAAAAAAAAAABiQwUD8QsUGCCWJwJ6wSyTqA-66_H1LZG6O8T7oiCUG/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=MtrZhr2S9RLQn9mVj5YW%2B8yFNEk%3D)

그림2

![](https://blog.kakaocdn.net/dna/eTdbrf/btsMFEDRA9s/AAAAAAAAAAAAAAAAAAAAAK7M4385a5WijIX_XtJMhnpagAEbotOQK9tq-OOSAatq/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nsE3ngou4UvmjHdtD50QvvOAQIo%3D)

라플라스 연산자

**j가 4-wide loop vectorized**라면, **j는 4의 배수**임이 보장되고, 따라서 x[i, j+1]은 x[i, j]와 **같은 상위 노드 or block(ancestor)** 를 공유합니다.

따라서 **데이터 구조를 i, j와 i, j+1에 대해 각각 탐색할 필요 없이 한 번만 탐색하고, 거기서 j , j + 1에 접근하면 된다.**

![](https://blog.kakaocdn.net/dna/sWzR3/btsMH9vo2qL/AAAAAAAAAAAAAAAAAAAAAAracW6ytuEQ4THXuAKq7CH0cl1cmUXZHNgOkFA9buLO/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=kq6fp3A7naYpbBmtFpzMUA625hI%3D)

yellow 가 red에 대한 compile time know offset으로 단순화 된다.

![](https://blog.kakaocdn.net/dna/HU1xq/btsMIdErlvI/AAAAAAAAAAAAAAAAAAAAAPQS2XfK905h57qtS5yrUldCFjdQ9AjLWAlaDIpaDf7y/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=OOPcHrlHYpcxCv2MIi9Epf856Q4%3D)

### **4.3 Automatic Parallelization and Task Management**

**희소 데이터 구조(sparse data structures)를** **작업을 프로세서 코어에 고르게 분산**하는 것은 매우 어렵다.

불규칙한 트리를 순진하게 순서대로 짜르면 아래의 그림 처럼 수가 다른 leaf block이 생길 수있다.

![](https://blog.kakaocdn.net/dna/UTE3I/btsMHYgzlxM/AAAAAAAAAAAAAAAAAAAAAC_gGuZE8zHjQiM0SuYjTdQsVn3_eKl7l1VV2uBx7XBE/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=BnFi8nZg1l9gD8TLYY3thI06L5c%3D)

우리의 전략은 leaf block에 대한 task list를 만드는 것이다. task list는 1D일 것이고, 불규칙한 트리를 우회하게 도와줄 것이다. (task per block)

**CPU**

light-weight traversal를 통해 직렬로 task of list를 만든다.

이 list는 thread pool에 queue로 저장된다.

이후에 OpenMP를 사용해서 병렬로 처리한다.

**GPU**

root에서 leaf까지 structural node 별로 task of list를 유지한다.

**list는 root 부터 시작되고, active parent node의 큐로부터 active parent node의 큐 생성.**

큐의 위치는 global atomic counter로 관리된다.

![](https://blog.kakaocdn.net/dna/b7OmmW/btsMHqR12LT/AAAAAAAAAAAAAAAAAAAAAOV8HU0FrrZS-ufQJBFGNKpEmRgTN7nayqjDzV3FhjMD/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=F5afZrlOzKOJVhdxw6w9JrtlWM0%3D)

실선(solid lines): **계산을 위한 중간 표현(IR) 파이프라인**.

점선(dotted lines): **데이터 구조 정보(data structure information)**

**GPU 커널과 CPU 간의 동기화(synchronization)** 는 **비용이 매우 크기 때문에 최소화**해야 한다.

**사용자가 명시적으로 동기화 함수**(예: cudaDeviceSynchronize())를 호출하거나,

**GPU 메모리 상의 데이터에 읽기/쓰기 작업**을 요청할 때만 **CPU-GPU 동기화**가 발생한다.

이러한 설계 덕분에 **비동기(asynchronized)** GPU 실행이 **사용자에게 투명하게 동작**합니다. (실제로 print해보면 병렬로 처리되는 것을 볼 수 있다. for문이 우리가 예상한 순서대로 실행되지 않음)

5. Compiler and Runtime Implentation

컴파일러 및 런타임의 주요 구성 요소는 두 단계다.

**1. 간소화(simplifier)**

명령어 줄이기, 중복 접근 체거, 낮은 수준의 접근으로 변환, 메모리 할당과 가비지 컬렉터에 대한 관리 컴스터마이

**2. CPU 루프 벡터화**

우리의 IR(immediate representation)은 데이터 구조 접근 시 **인덱스의 범위 정보**나 **데이터 구조 요소의 크기**와 같은 정보를 명시적으로 포함한다. 이와 같이 구체적인 **데이터 구조 접근 정보를 가지고 있어 컴파일러가 데이터 구조 조합과 연관된 최적화를 자동으로 수행할 수 있게 한다.**

### 

### **5.1 Simplification**

데이터 구조 접근(data structure access)을 위한 최적화 외에도, 우리의 간소화 단계는 일반적으로 널리 사용되는 다목적 최적화 기법을 적용한다. (common subexpression 제거, local variable store forwarding, dead instruction elimination , lowering “if”-statements into conditional moves 등을 사용)

**local variable store forwarding:**

```
int tmp = a + b
int x = tmp

=> int x = a + b
```

**dead instruction elimination:**

```
int y = a ^ 10 // dead instruction
int x = 1

return x
```

**lowering “if”-statements into conditional moves.**

기계어 명령어에서 branch문을 안쓰도록 유도.

if문을 안쓰면 코드가 straightline code가 되는데, 이는 최적화에 많은 도움이 된다.

우리는 simplificaion을 두 개의 단계로 나누어 수하는데,

첫 번째 단계는 대부분의 복잡한 연산을 미리 정리하여, 두 번째 simplification 단계가 더욱 쉽게 진행될 수 있도록 한다.

데이터 구조 접근 simplification의 핵심은 micro access이다.

(OffsetAndExtractBit, SNodeLookup, GetCh, and IntegerOffset.)

이것들은 access lowering 단계를 통해서 생성된다.

access lowering: root-to-access(ex. x[i])는 계층구조 안에서 다양한 단계로 나뉘어 지는데,

많은 access들이 root 에서 leaf까지의 경로가 비슷하기 때문에 비슷한 micro access 연산자는 병합이 가능하다.

1. 각각의 dimenstion의 offset들을 계산하고 , 시작과 끝은 bitbask를 표시한다. => OffsetAndExtractBit

예시:

만약에 kernel이 j에 대해서 4-wide loop이고, 현재 block의 자식이 4보다 큰 사이즈라면

OffsetAndExtractBit를 통해서 offset을 얻을 때 j, j + 1, j + 2, j + 3에 대해서 4번 호출하는 것이 아니라,

1번만 호출해서 계산할 수 있다는 것이다.

만약 아래와 같은 상황이면 offset에 1번만 접근해서 j, j+1, j+2, j+3 의 값을 얻을 수 있다는 말

```
for j in range(100):
	access(j)
    access(j+1)
    access(j+2)
    access(j+3)
```

그 다음에는

다차원 indices일 때 1차원으로 변경하고, 원하는 iteam의 pointer를 offset을 통해서 가져와 사용한다. 이 때 해당 node가 active 상태인지 아닌지 잘 확인해야된다. **(SNodeLookUp).**

**SNodeLookUp을 사용할 때**

읽기 연산 시, node가 not active라면, 모든 필드가 기본값(ambient value, 예: 0)을 가지는 **ambient node**를 반환한다.

쓰기 연산의 경우, node가 not active라면, **새로운 노드를 먼저 할당한 후**, 할당된 노드를 반환한다.

마지막으로, 데이터 구조의 아이템에서 실제로 필요한 필드를 **GetCh** 연산을 통해 가져온다.

만약 컴파일 시간에 이미 알고 있는 non-zero offset이 있는 **동일한 type의 micro access instruction**가 두 개 존재한다면, 두 번째 명령어를 **IntegerOffset**이라는 연산으로 대체할 수 있다.

이는 두 access간의 byte 단위 관계를 명시적으로 나타내며, 불필요한 데이터 구조 순회를 피할 수 있게 한다.

### **5.2 Memory Management**

우리 시스템은 **필요할 때 할당하는(on-demand allocation)** 메커니즘에 크게 의존하며, **동적 토폴로지를 가지는 데이터 구조**를 지원한다. 그렇기 때문에  **효율적인 메모리 관리**는 특히 **대규모 병렬 GPU** 환경에서 성능의 핵심 요소이다.

dynamic topology: 어느 부분에 데이터가 존재하고 존재하지 않는지 관리하는...

이 문제를 해결하기 위해 우리의 **추상화(abstraction)에 특화된** 매우 **단순한 데이터 구조의 메모리 관리 시스템**을 디자인했다.

우리의 메모리 관리자는 노드의 구조에 맞는 별도의 메모리 할당자(memory allocator)를 둔다.  
**1. 여러 개의 할당자**를 가지는 이점은, 각 할당자가 **고정된 크기(fixed size)의 메모리 조각만을 할당**하면 되기 때문에, 간단하고 **속도가 빠르다**.

**2.**  메모리를 최소한으로 사용하기 위해서 가상 메모리를 넉넉하게 잡아서 사용하고, 그 중 실제로 사용한 부분만 실제 메모리에 올린다.

### **5.3 Loop Vectorization on CPU**

우리는 최신 CPU에서 벡터 명령어 집합(vector instruction sets)을 활용하기 위해 loop를 벡터화했습니다.

(분기문에 의한 side effect를 피하기 위해 masking을 사용한다.)

가능한 경우 **데이터 구조에 대한 접근**이 반드시 vectorized loads and writes로 수행되도록 보장한다.

**CPU에서의 벡터화된 메모리 접근**

좋은 메모리 성능을 얻기 위해, **스칼라(scalar) 읽기 대신 벡터화된 메모리 작업(vectorized memory operations)을 수행**하는 것이 필요하다.

아래와 같이 동작한다.

![](https://blog.kakaocdn.net/dna/bevpmJ/btsMHsbTGTH/AAAAAAAAAAAAAAAAAAAAAIMDO2xDgT0JnuzItSTFvImSpL7juHIqBFz7mc6lktuH/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=UhW9pz9cbkBnZf2z3SD0Y1OooGU%3D)

### **5.4 Interaction with the Host Language**

C++과 호환이 가능하다.