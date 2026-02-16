---
title: "[논문정리] Visual Simulation of Smoke (코드포함)"
date: 2025-03-26
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **실습:**

**<https://tithingbygame.tistory.com/175>**

[[실습저장소] 연기 시뮬레이션 ( 논문: Visual Simulation of Smoke )

논문 정리: 하는중실행 코드: https://github.com/GameTithe/stable\_fluid\_taichi GitHub - GameTithe/stable\_fluid\_taichiContribute to GameTithe/stable\_fluid\_taichi development by creating an account on GitHub.github.com

tithingbygame.tistory.com](https://tithingbygame.tistory.com/175)

### 

### **1. Introduce**

우리는 고해상도 격자에 비해 비교적 낮은 해상도의 격자에서도 복잡하게 말려 올라가는 연기의 애니메이션을 생성하였습니다.

### **1.1 Previous Work**

Stam은 unconditionally stable 시뮬레이션이 가능하도록 모델을 제안했다.

그 모델은 semi-Lagrangian advection 방식 + implicit solver를 사용했다.

하지마 해당 모델은 numerical dissipation( 수치적 손실 ) 이 심해서 전체적인 움직임은 유체처럼 보이지만, 연기에서 흔히 볼 수 있는 소규모 소용돌이는 빠르게 사라졌다.

### **1.2 Our Model**

**우리의 모델은 연기와 같은 기체를 시뮬레이션하기 위해서 설계되었다.**

 우리는 연기의 속도를 비압축성 오일러 방정식(incompressible Euler equations)으로 모델링하고,  **semi-Lagrangian 적분 방식**과 압력-포아송 방정식(pressure-Poisson equation)을 통해 해석한다. (Stam의 stable fluid와 동일하다 = 안정적)

우리의 주요한 기여는 semi-Lagrangian을 사용하면 numerical dissipation( 수치적 손실 ) 을 줄였다.

vorticity confinement(소용돌이 보존) 방법을 사용하였다.

기본 아이디어는 numerical dissiptaion 에너지를 forcing term을 통해 유체에 다시 주입하는 것이다. forcing term은 격자 수가 충분히 많아질 경우 사라지기 때문에 오일러 방정식과의 일관성을 유지한다.

forcing term의 계산은 약간의 연산만 추가되고 전체 시뮬레이션 속도는 기본 Stable Fluids 알고리즘과 거의 동일하다.

또한, forcing term의 크기만 일정 임계값 이하로 유지된다면 모델의 안정성도 유지가 된다. 이 범위 내에서, 우리의 시간 간격은 기존 명시적 방식보다 훨씬 크게 설정할 수 있다.

.

### **2. The Equations of Fluid Flow**

우선, 우리는 기체를 **비점성(inviscid)**, **비압축성(incompressible)**, **밀도가 일정한(constant density)** 유체로 모델링할 수 있다고 가정한다. 점성(viscosity)의 효과는 특히 coarse grid(거친 격자)에서는 numerical dissipation이 실제 점성 및 분자 확산보다 우세하기 때문에 기체에서는 무시할 수 있다.

또한 연기의 속도가 음속보다 훨씬 느릴 경우, 압축성(compressibility)의 영향도 무시할 수 있으며, **비압축성이라는 가정은 수치 해석을 훨씬 단순하게 만든다**.

따라서 연기의 속도 u=(u,v,w)를 모델링하는 방정식은

비압축성 오일러 방정식(incompressible Euler equations)

1. 질량 보존 방정식

![](https://blog.kakaocdn.net/dna/diDkfd/btsMVGfdC6t/AAAAAAAAAAAAAAAAAAAAAJa-flcq_oZ9Lvz_0VDTC9oAQBK7iDxzp7J0SfUr0NBG/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=uw4MMLNYggSf%2FLpterKJDszjslM%3D)

2. 운동량 보존 방정식

![](https://blog.kakaocdn.net/dna/dk15cO/btsMTIeIXHW/AAAAAAAAAAAAAAAAAAAAAJpJRNbdpyvdzNOZOaNE2kxYuUh7sXKPfXVxWu_KBoNR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fBqzgyaJEIQA4Wc3J0Vbibo5Gdk%3D)

(점성 부분이 없는 것을 볼 수 있다)

두 단계로 해결한다.

**첫 번째 단계**

압력항 없이, 중간 속도장 u\*를 계산한다.

![](https://blog.kakaocdn.net/dna/cEpD8Z/btsMT3CMxFt/AAAAAAAAAAAAAAAAAAAAAOFaAAoi5mUu2EBerHbg-eJV3dwgqN8QqkTeTjBnGIv5/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Niq9O1DKN0yEDT%2FQ2hx6aZOpkfM%3D)

**두 번째 단계**

포아송 방정식을 풀어서 압력항 p를 계산

![](https://blog.kakaocdn.net/dna/bKtL0z/btsMUuUmwyh/AAAAAAAAAAAAAAAAAAAAAGPLjqRfU-49XppuSHJiLWd65tTdn1245t66zSmz6gR3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wPJdZP1PBE8vQDGrn1LfBJi%2FpcM%3D)

우리는 **T(온도)** 와 ρ(밀도)의 변화를 계산할 방정식이 필요하다.

이 두 스칼라 물리량은 연기의 속도장에 따라 단순히 이동(advect)된다고 가정한다:

![](https://blog.kakaocdn.net/dna/lTcfK/btsMT9QrqNi/AAAAAAAAAAAAAAAAAAAAAPQhUP9D5HP11uFPFA2BvbAZhPMcu-wWCNNgdME_8f7p/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=q9nT3uGbSvLAgVW03juKeYhhq9o%3D)

무거운 연기는 중력 때문에 아래로 떨어지고 뜨거운 기체는 부력으로 인해 상승한다.

**z:** (0,0,1)은 위쪽 방향을 나타낸다.

**T**amb: 공기의 온도이다.

α와 ρ는 단위를 맞추기 위한 양의 상수이다.

이 식은 ρ=0이고 T=**T**amb일 때, 부력이 0이 되는 조건도 만족한다.

### **3. Vorticity Confinement(****소용돌이 보존****)**

일반적으로 연기와 공기 혼합물은 공간적으로 큰 변화를 가진 속도장을 포함하고 있으며, 회전성과 난류 구조가 나타난다.하지만 수치적 소산(numerical dissipation)은 이러한 특징을 가쇠시킨다.

우리가 제안하는 새로운 접근법의 목표는 이러한 특성을 조밀하지 않은(coarse) 격자에서도 나타나게 만든다.

우리의 방법은 유동장 안에서 특성이 생성되어야 할 **위치를 먼저 찾아낸 다음,** 해당 위치에 **물리 기반 방식으로 디테일을 추가**한다.

첫 단계는, **그 디테일이 어디서부터 오는지 식별하는 것**이다.  
비압축성 유동(incompressible flow)에서는, 소용돌이 벡터 ω(오메가) 소규모 구조를 나타낸다

![](https://blog.kakaocdn.net/dna/cs0I6X/btsMT6sIaer/AAAAAAAAAAAAAAAAAAAAAGMTeNG5ggPjNWnJ0deiV6joq9ZZ1GN0D5aUBM6dOBDF/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=4nmdW6e2MOPkcWuWVn0B%2BbSnkWo%3D)

각 소용돌이는 특정 방향으로 회전시키려는 성질을 가진다.  
하지만 numerical dissipation은 이 회전 효과를 감소시키기 때문에, 우리는 이를 다시 force term으로 추가하려는 것이다.

먼저, 소용돌이의 방향과 위치를 나타내는 벡터를 계산한다.

![](https://blog.kakaocdn.net/dna/bLNcik/btsMVD3R5Yp/AAAAAAAAAAAAAAAAAAAAAOelKpyrzF-pbJ9dBuMIcF7lKKNQzsjNDbjdDA3gU1bS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=zm8oO6%2F3WE16zmuTpX81r7dv80Y%3D)

force term은 아래와 같다.

![](https://blog.kakaocdn.net/dna/bwr4f6/btsMUZfxLNr/AAAAAAAAAAAAAAAAAAAAADdvyrLYABgPPjgz0XCtS8lEsMQjBbxiMDRQjPWHOGpo/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wb7VVRqejJ4NubwISDvyMLvbYSk%3D)

정리하면 이렇게 된다.

![](https://blog.kakaocdn.net/dna/uYAFj/btsMX48m4KF/AAAAAAAAAAAAAAAAAAAAABUsmoVBtYzEbABo_uSG_S2Efne7Fwuu3Q7d7mKKihgT/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=V4YsgWwcEvi1iIywP6utDIC6was%3D)

### **4. Implementation**

논문에서는 어떻게 어떻게 해라 자세히 나오지는 않는다.

구현해본 입장에서 정리를 하면

```
@ti.kernel
def vel_step(mouse_pos: ti.types.vector(2, ti.f32), add_force: ti.i32):
    
    if add_force: 
        AddSource_U(mouse_pos)
        SwapU()
    
    Diffuse_U() 
    #Project()
    SwapU()
    
    Advect_U()
    SwapU()
    
    compute_vorticity()
    apply_vorticity_confinement()  
    SwapU()
    
    Project()      
    SwapU()
```

이렇게 Diffuse, Advect하고

vorticity confinement를 추가해주면 잘 되더라....요..

깃 링크

<https://github.com/GameTithe/stable_fluid_taichi>