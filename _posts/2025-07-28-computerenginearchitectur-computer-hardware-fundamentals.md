---
title: "[ComputerEngineArchitectur] Computer Hardware Fundamentals"
date: 2025-07-28
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

진정으로 능숙한 프로그래머가 되기 위해서는 **목표 하드웨어의 아키텍처에 대한 이해**가 중요하다.

이러한 이해는 **코드 최적화**에 도움을 줄 뿐만 아니라, 컴퓨팅 하드웨어에서 점점 더 증가하는 병렬성(parallelism)을 효과적으로 활용하는 것에도 도움을 줄 것이다.

이후의 설명에서는 실제 특정 CPU에 대한 설명보다는, **단순하고 범용적인 CPU 설계**를 통해 이론적인 내용을 다룰 것이다.

### **Anatomy of a Computer(컴퓨터의 구조)**

* CPU(중앙 처리 장치)
* 메모리 뱅크 (RAM 등)
* 이것들은 bus라는 회로를 통해 서로 연결되어 있으면, 모두 마더보드(motherboard)에 탑재되어있다.

이런한 구조를 폰 노이만 구조라고 부른다.

![](https://blog.kakaocdn.net/dna/qUZ3l/btsPB1uvVE2/AAAAAAAAAAAAAAAAAAAAANwVFwU680nByjx-TPzxCHvwlrhcQqolnmRBTORDDLJ6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=6jMjy9ziHJMm9gguLCOrJziPJj4%3D)

### **CPU(중앙 처리 장치)**

CPU는 컴퓨터의 두뇌에 해당하는 부분으로, 아래와 같은 구성요소를 포함한다.

**1. ALU (arithmetic/logic unit 산술 논리 유닛)**  
정수 연산, 비트 이동 등 수행

**2. FPU (a floating-point unit, 부동소수점 유닛)**

IEEE 754 부동소수점 표준 기반의 연산 처리

**3. VPU (vector processing unit, 벡터 처리 유닛)**

여러 데이터 항목을 병렬로 연산할 수 있는 SIMD 구조

**3. MMU or MC (memory controller, 메모리 컨트롤러)**  
CPU내부 및 외부 메모리와 통신

**4. CU (control unit, 제어 유닛)**

기계어 명령 해석 및 각 부품으로 데이터 라우팅

이 모든 부품은 clock이라는 정기적인 직사각형 파형 신호로 구동된다.

클럭 주파수는 CPU가 명령어를 실행하거나, 산술 연산을 수행하는 속도를 결정짓는 핵심 요인이다.

![](https://blog.kakaocdn.net/dna/dFSiyB/btsPBjWGHBh/AAAAAAAAAAAAAAAAAAAAAAZ-CjMZ2W_2tGrUHtSdVMNEkpEh1aYGW4QfKOvGPUJf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ueoz06s9VIv4C0J9GlND3etEQaE%3D)

  

### **ALU (산술 논리 유닛)**

ALU는 **unary 또는 binary로 산술연산**을 수행한다. (**부호 반전, 덧셈, 뺄셈, 곱셈, 나눗셈** 등)

또한 AND, OR, XOR, 비트 반전, 비트 시프트와 같은 **논리 연산**도 수행한다.

(일부 CPU 설계에서는 ALU가 물리적으로 산술 유닛(AU)과 논리 유닛(LU)으로 나뉘어져 있다.)

ALU는 일반적으로 **정수**연산만 수행한다. **부동소수점** **계산은 매우 다른 회로가 필요하며, 보통 물리적으로 분리된 부동소수점 유닛(FPU or VPU)에 의해 수행된다.**

### **VPU (벡터 처리 유닛)**

VPU는 ALU와 FPU의 조합처럼 작동한다.

**즉, 일반적으로 정수 및 부동소수점 산술 연산을 모두 수행할 수 있다.**  
VPU를 차별화시키는 점은 **벡터(vector)** 형태의 입력 데이터에 적용할 수 있다는 점이다.

**오늘날의 CPU에는 전통적인 의미의 FPU는 사실상 존재하지 않는다. 대신, 모든 부동소수점 연산(심지어 스칼라 float 연산조차도)은 VPU에 의해 수행된다.**

(독립적인 FPU가 존재했을 때는 Float 형변환이 굉장히 비쌌지만, 현재는 VPU가 정수, 실수 연산을 같이 처리해주기 때문에 비용이 많이 감소했다. => 여전히 형변환을 줄이는게 성능면에서 좋긴하다. )

### **Registers**

**성능을 극대화하기 위해, ALU나 FPU는 보통 특수한 고속 메모리 셀인 레지스터(register) 내에 있는 데이터만을 대상으로 연산을 수행할 수 있다.**

**레지스터는 보통 컴퓨터의 주 메모리(main memory)와는 물리적으로 분리되어 있으며, 칩 내(on-chip)에 위치하고 관련 구성요소 근처에 배치된다.**

레지스터는 고속이지만 비용이 많이 드는 SRAM을 사용하여 구현된다.

CPU 내에 있는 레지스터들의 묶음을 레지스터 파일(register file)이라 부른다.

레지스터는 **주 메모리의 일부가 아니기 때문에, 일반적으로 주소(address)는 없지만 이름(name)은 있다.**  
(이름은 R0, R1, R2처럼 단순하게 사용했다.)

사용용도

**1. GPR(General-Purpose Register)**

일반 산술용도

**2. SPR(Special-Purpose Register)**

명령어포인터 (IP)

스택 포인터 (SP)  
기준 포인터 (BP)  
상태 레지스터 (Status Register) 

### **Instruction Pointer**

명령어 포인터(IP)는 현재 실행 중인 머신어 명령어의 **주소**를 담고 있다.

### **Stack Pointer**

프로그램의 호출 스택(call stack)은 함수 간의 호출을 처리할 뿐만 아니라, 지역 변수의 메모리 할당을 담당하는 주요 구조다.

**스택 포인터(SP)는 프로그램의 호출 스택 상에서 가장 위(top)에 있는 데이터의 주소를 저장한다.**

스택은 메모리 주소 기준으로 **위쪽 또는 아래쪽으로 성장**할 수 있는데,

스택이 **아래쪽으로 성장**한다고 가정하면

**푸시(push)하는 상황:**

SP 값을 해당 데이터 크기만큼 **감소시킨 뒤**, 새 SP가 가리키는 주소에 데이터를 저장한다.

**팝(pop)하는 상황:**

SP가 가리키는 주소의 값을 읽고, SP를 해당 데이터 크기만큼 **증가**시키면 된다.

### **Base Pointer**

베이스 포인터(BP)는 현재 실행 중인 함수의 스택 프레임(stack frame)의 기준(base) 주소를 저장한다.

함수의 많은 지역 변수(local variables)는 이 스택 프레임 내에 위치한다.

.

스택에 할당된 지역 변수들은 BP로부터의 offset을 기준으로 메모리에 위치한다.

(Stack pointer는 call stack의 마지막 부분이고, base pointer는 현재 함수의 시작부분)

### **Status Register**

이 레지스터는 다음과 같은 이름으로도 불린다:

**조건 코드 레지스터 (condition code register),** **플래그 레지스터 (flags register)**

이 레지스터는 최근에 수행된 **ALU 연산 결과에 대한 상태를 반영하는 비트들이다.**

뺄셈 결과가 **0**이면 Z(zero) 비트가 설정되고,

덧셈 중 오버플로우가 발생하여 상위 비트로 자리 올림(carry)이 일어나면 C (carry) 비트가 **설정된다.**.

### **레지스터 형식 (Register Formats)**

FPU(부동소수점 연산 유닛)와 VPU(벡터 연산 유닛)는 보통 ALU의 범용 정수 레지스터(GPRs)를 사용하지 않고,  
**자신만의 전용 레지스터 세트**를 사용한다.

그 이유는 다음과 같다:

**속도**  
 연산 유닛에 가까이 있는 레지스터일수록 접근 시간이 짧아져 성능이 향상됨.

**폭(크기) 차이**  
예를 들어 ALU의 GPR은 32비트지만,  
FPU는 64비트 **double precision** 혹은 80비트 **extended precision**을 처리하므로  
더 넓은 레지스터가 필요함.

**벡터 처리용 폭**  
VPU는 벡터 데이터(다중 값)를 다루므로, 레지스터 폭이 훨씬 커야 함.

### **제어 장치 (Control Unit)**

CPU가 컴퓨터의 "두뇌"라면, 제어 장치(Control Unit, CU)는 **CPU의 두뇌**라고 할 수 있다.  
CU의 역할은 **CPU 내부의 데이터 흐름을 관리하고, CPU의 다른 모든 구성 요소들의 동작을 조율**하는 것이다.

CU는 프로그램을 실행할 때, 머신어 명령어들의 스트림을 읽고,  
각 명령어를 opcode(연산 코드)와 operand(피연산자)로 **디코딩**하며,  
명령어의 opcode에 따라 **ALU, FPU, VPU, 레지스터, 메모리 컨트롤러** 등에 **작업 요청을 보내거나 데이터를 전달**한다.

**CU는 분기 예측(branch prediction) 및 비순차 실행(out-of-order execution)을 위한 복잡한 회로도 포함하고 있다.**

### 

### **Clock**

모든 디지털 전자 회로는 본질적으로 state machin이다.  
회로가 상태를 바꾸기 위해서는 어떤 **디지털 신호**가 이를 **유도**해야 한다.

이러한 신호는 회로 내의 전압을 **0V에서 3.3V로**, 또는 그 반대로 바꾸는 방식으로 제공될 수 있다.

CPU 내부의 상태 변화는 일반적으로 system clock이라고 불리는 **주기적인 정사각형 파형**에 의해 구동된다.

이 파형의 **상승 또는 하강 에지(edge)** 하나가 한 번의 clock cycle을 의미하며,  
CPU는 각 사이클마다 최소 하나의 primitive operation을 수행할 수 있다.

따라서 **CPU에게 시간은 양자화된(quantized)** 것처럼 보인다.

CPU가 연산을 수행할 수 있는 속도는 **시스템 클럭의 주파수**에 따라 결정된다.  
클럭 속도는 수십 년간 크게 증가해 왔으며, **Intel Core i7** 같은 CPU는 보통 **2~4GHz**(십억 사이클/초)의 속도로 작동한다.

(하지만 CPU 명령어 1개가 1클럭 사이클 내에 끝나는 것은 아니다. 성능측정을 위해서는 표준화된 벤치마크를 돌리는게 좋다  )

### **Memory**

컴퓨터의 메모리는 마치 우체국의 사서함(mailboxes)과 같다.  
각 사서함(또는 셀)은 보통 1바이트(8비트)의 데이터를 저장하며, 고유한 주소(address)로 식별된다.

이 주소는 단순한 번호 체계이며, 0부터 N-1까지 부여된다.  
여기서 N은 바이트 단위로 **주소 지정 가능한 메모리 전체 크기**다. (컴퓨터 초기에는 byte가 아닌 word도 접근했다.)

### 메모리의 두 가지 기본 유형

**읽기 전용 메모리 (ROM, Read-Only Memory)**

1. 전원이 꺼져도 데이터를 유지함

2. 일부 ROM은 **한 번만 프로그래밍 가능(일회성)**

3. 일부는 **여러 번 재기록 가능한 EEPROM (전자식 소거 가능 프로그래머블 ROM)**

**읽기/쓰기 메모리 (RAM, Random Access Memory)**

1. 이름은 역사적 이유로 RAM이라고 불리지만, 오늘날 일반적으로 **읽기/쓰기 모두 가능한 메모리**를 의미함

2. 전원이 공급되는 동안만 데이터를 유지함

### 

### RAM의 하위 분류

|  |  |
| --- | --- |
| **정적 RAM (SRAM)** | - 전원만 공급되면 데이터를 유지함 - 별도 갱신(refresh) 불필요 |
| **동적 RAM (DRAM)** | - 전원이 켜져 있어도 **주기적으로 갱신(refresh)** 필요 - 내부적으로 **MOS 커패시터**를 사용하여 데이터를 저장 - 커패시터는 시간이 지남에 따라 전하가 새어 나감 - 또한 DRAM 셀은 읽을 때 **데이터가 파괴**되므로 읽은 후 **다시 써야 함** |

### RAM의 추가 분류 기준:

**멀티 포트(Multi-Ported)**  
**CPU 내 여러 구성 요소가 동시에 RAM에 접근**할 수 있는지 여부

**동기식 vs 비동기식**  
RAM이 시스템 클럭에 동기화(SDRAM)되어 동작하는지, 또는 **비동기적으로** 동작하는지 여부

**더블 데이터 레이트(DDR)**  
RAM이 클럭의 **상승 에지와 하강 에지** 모두에서 **읽기/쓰기**를 수행할 수 있는지 여부  
(클럭 주기당 **2배의 데이터 처리 가능**)

### Bus

**CPU와 메모리 사이의 데이터 전송은 bus라 불리는 연결을 통해 이루어진다.**  
버스란 본질적으로 **병렬로 정렬된 디지털 선(wire들의 묶음**으고, 이 선 하나 하나는 1비트의 데이터를 표현할 수 있다.

n개의 단일 비트 선이 병렬로 묶이면, **0부터 2ⁿ-1 범위의 정수**를 전달할 수 있다.

일반적인 컴퓨터는 두 개의 주요 버스를 가진다:

**1. 주소 버스 (Address Bus)**

**2. 데이터 버스 (Data Bus)**

### 

### 데이터 전송 흐름

**CPU가 메모리에서 데이터를 읽을 때:**

1. 주소 버스를 통해 메모리 컨트롤러에 **읽고 싶은 주소**를 보냄
2. 메모리 컨트롤러가 그 주소의 데이터 비트를 **데이터 버스에 실어 보냄**
3. CPU가 그 데이터를 받아 **레지스터에 저장**

**CPU가 메모리에 데이터를 쓸 때:**

1. 주소 버스를 통해 **저장할 위치의 주소**를 전달
2. 데이터 버스에 **저장할 데이터 값**을 실어 보냄
3. 메모리 컨트롤러가 해당 주소에 데이터를 기록

주소 버스와 데이터 버스는 보통 **물리적으로 별도의 선**으로 구현되지만,

일부 시스템에서는 **하나의 선을 시간 분할 방식으로** 주소/데이터 전송에 재사용하기도 한다 (이것을 멀티플렉싱(multiplexing)이라 한다.

## Bus Widths

**주소 버스의 폭**(bit 수)은 CPU가 **최대 얼마만큼의 메모리 주소 공간을 접근할 수 있는지를 결정**한다.

**데이터 버스의 폭**은 CPU 레지스터와 메모리 사이에서 **한 번에 전송할 수 있는 데이터 크기**를 의미한다.

보통은 **CPU의 GPR(범용 레지스터)의 폭과 동일**하지만, 항상 그런 건 아니다.

### 

## **Words**

word라는 용어는 "여러 바이트로 구성된 하나의 데이터 단위" 를 의미하지만, **그 정확한 크기는 상황에 따라 다르다.**

CPU는 보통 워드 크기만큼 데이터를 주고받으며, 이 "워드"의 크기는 아키텍처마다 다르다.

보통  32비트 PCU에서는 1워드가 4바이트(32비트), 64비트 CPU에서는 1 워드가 8바이트(64비트)가 된다. 

### **Machine & Assembly language**

CPU의 관점에서 볼 때, “프로그램”이란 단순히 **순차적으로 나열된 명령어들의 흐름이고,** 제어 유닛(Control Unit, CU)과 궁극적으로는 메모리 컨트롤러, ALU, FPU, VPU 등 **CPU 내부의 다른 구성 요소들**에 **특정 연산을 수행하라고 지사하는 것이다.**

대부분의 경우 명령어는 **순차적으로 실행**되지만,  
일부 명령어는 프로그램 흐름을 변경(jump)시켜 명령어 스트림 내 **다른 위치로 이동**할 수 있다.

### **명령어 집합 구조 (ISA: Instruction Set Architecture)**

CPU의 설계는 제조사마다 매우 다양하다.  
어떤 CPU가 지원하는 **모든 명령어의 집합**, 그리고 그와 관련된 **주소 지정 방식(addressing modes)**, **메모리 내 명령어 포맷** 등을 통틀어 명령어 집합 구조(ISA)라고 부른다.

우리는 특정 CPU의 ISA를 상세히 다루지는 않겠지만, 거의 모든 ISA에서 **공통적으로 나타나는 명령어 유형**은 다음과 같다:

Move: 레지스터간 or 레지스터-메모리 간 데이터 이동

Arithmetic(산술연산): 덧셈, 뺄셈, 곱셈, 나눗셈, 부정, 역수, 제곱수 등

Bitwise(비트연산) : AND, OR, XOR

Shift, Rotate: 비트를 좌우로 밀거나 회전시키거나

등등...

정리하면 CPU는 프로그램을 명령어들의 나열로 이해하고, 이를 ISA에 맞게 수행한다.

## **Machine Language(기계어)**

컴퓨터는 오직 **숫자만** 처리할 수 있다.  
따라서 프로그램 내 명령어 스트림의 **각 명령어는 숫자 형태로 인코딩되어야 한다.**  
이렇게 인코딩된 프로그램을 Machine Language(기계어)로 작성되었다고 말한다.

물론, 머신어는 단일한 언어가 아니다.

![](https://blog.kakaocdn.net/dna/bx737K/btsPChYmolH/AAAAAAAAAAAAAAAAAAAAAKKCbTiLksM28EtzXl4NAUe3Y3Uevc4uLNB9LJwh1bRJ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=WVVD0eB1yYqUkIOHEJRJxnPp%2FNc%3D)

사실상, **CPU/ISA마다 서로 다른 머신어를 가지고 있기 때문에, 머신어는 수많은 언어들의 집합**이다.)

### 

### 기계어 명령어의 기본 구성

모든 기계어 명령어는 보통 다음 3가지 기본 요소로 구성된다:

**Opcode (연산 코드)**

CPU에게 어떤 연산을 수행할지를 지시함 (예: add, subtract, move, jump 등)

**Operands (피연산자)**  
명령어가 사용할 **값** 지정 (레지스터, 상수, 주소 등)

**옵션 필드 (옵션, addressing mode 등)**  
주소 지정 방식이나 기타 플래그를 포함함

### 

### **피연산자(Operands)의 다양한 형태**

일부 명령은 **레지스터 이름**(숫자 ID로 인코딩됨)을 피연산자로 사용 (R2 레지스터에 값 5를 로드해라)

어떤 명령은 **리터럴 값**을 피연산자로 사용  (주소 0x0102ED5C로 점프해라 등)

명령어의 피연산자를 CPU가 해석하는 방식은 Addressing Mode이라고 부른다.

### 

### **Instruction Word**

Opcode와 Operands 보통 **일련의 비트 시퀀스**에 함께 포장되며, 이를 **인스트럭션 워드**라고 한다.

어떤 CPU에서는 **첫 번째 바이트에 opcode, 주소 지정 모드, 옵션 플래그**를 담고,

뒤따르는 바이트들에 **피연산자 정보**를 담는다.

### **Instruction Width**

어떤 ISA는 **모든 명령어가 고정된 비트 수**를 가짐 (**RISC 구조**의 특징, reduced instruction set computers)

어떤 ISA는 **명령어마다 다른 길이**를 가짐 (**CISC 구조**의 특징, complex instruction set computers, 기본)

**LIW (Very Long Instruction Word)** 구조에서는, (수 백 바이트일 수 있음)  
하나의 매우 긴 명령어 워드에 여러 연산을 담아 **병렬 실행**을 가능하게 하기도 한다.

## 

## **어셈블리 언어 (Assembly Language)**

기계어로 직접 프로그램을 작성하는 것은 **매우 번거롭고 오류 가능성이 높다**.  
이를 해결하기 위해, **텍스트 기반의 기계어,** **어셈블리 언어**가 개발되었다.

### 

### **어셈블리 언어의 특징**

각 명령어에는 기억하기 쉬운 영문 약어(mnemonic)가 지정됨  
(예: ADD, MOV, JMP, CMP 등)

피연산자는 다음과 같이 쉽게 표현할 수 있음:

**레지스터 이름** (EAX, R1, 등)

**메모리 주소** (16진수 혹은 기호로 정의한 심볼 이름)

명령어 위치에는 사람이 읽을 수 있는 label을 붙일 수 있음(분기 명령어가 **실제 주소가 아닌 레이블로 점프** 가능)

C언어

```
if (a > b)
    return a + b;
else
    return 0;
```

어셈블리

```
; if (a > b)
cmp eax, ebx       ; eax과 ebx 비교
jle ReturnZero     ; eax ≤ ebx면 ReturnZero로 점프

; return a + b;
add eax, ebx       ; eax = eax + ebx
ret

ReturnZero:
xor eax, eax       ; eax = 0
ret
```

## **주소 지정 방식 (Addressing Modes)**

겉보기엔 단순해 보이는 "move" 명령어도 **여러 가지 변형**이 존재한다.

값을 **한 레지스터에서 다른 레지스터로** 옮기는 것일까?

아니면 **리터럴 값 5를 레지스터에 직접 로드**하는 걸까?

아니면 **메모리에서 값을 읽어 레지스터에 저장**하는 것?

또는 **레지스터의 값을 메모리에 쓰는** 것?

이러한 각각의 방식은 모두 주소 지정 방식(Addressing Mode의 일종이다.

![](https://blog.kakaocdn.net/dna/MbL1q/btsPAyAugfF/AAAAAAAAAAAAAAAAAAAAAJ8LWOdoZihDvb4rqqD2gzgdbxX2a4zQcYzt-MAdQ-eQ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=QwNPoQUe1YdHagcNJqd081O8YW8%3D)
![](https://blog.kakaocdn.net/dna/ubGKX/btsPB0WULtT/AAAAAAAAAAAAAAAAAAAAAALAm5BR5Ue5rJRTB8Y5r1293c1-5Xc06qVqwn3xxCMQ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2B8HWuuj%2Fbt90Jmma9ZTm452SZZQ%3D)