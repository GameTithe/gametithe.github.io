---
title: "[CG] MLS-MPM (Elastic, Water)"
date: 2025-03-10
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

![](https://blog.kakaocdn.net/dna/O8nDC/btsNt7j4CJC/AAAAAAAAAAAAAAAAAAAAAJT3t0QW9lTwCoqMvr8j3TMsc9IH5JTr7IzcR7K6i3BB/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Oa44J2fMEXmUCfP7VuGj63VbG%2BI%3D)

<https://tithingbygame.tistory.com/163>

[[실습저장소] MLS-MPM ( 탄성체 Elastic, 물 시뮬레이션)

이론: https://tithingbygame.tistory.com/164 [CG] MLS-MPM (Elastic, Water)mpm guide - niall t.l. mpm guide - niall t.l.on one end of the spectrum, if the underlying spatial representation of your matter deforms along with its motion, you're using a Lagr

tithingbygame.tistory.com](https://tithingbygame.tistory.com/163)







**[mpm guide - niall t.l.](https://nialltl.neocities.org/articles/mpm_guide)**

[mpm guide - niall t.l.

on one end of the spectrum, if the underlying spatial representation of your matter deforms along with its motion, you're using a Lagrangian representation. examples of this would be SPH and PBF, where the spatial representation is the makeup of the partic

nialltl.neocities.org](https://nialltl.neocities.org/articles/mpm_guide)

**이 사이트를 참고해서 공부를 했고, 사이트에서 제공하는 github에 들어가면 C#코드가 있으니 참고하면 좋을 것이다.**

**나는 python, taichi를 사용해서 다시 구현했고 나의 깃허브에 올려놨으니 참고하실 분들은 참고하면 될 것 같다.**

<https://github.com/GameTithe/MLS-MPM>  
  
MPM은 물질 방정식( constitutive equation ) 으로 설명할 수 있는 거의 모든 것을 일반화 할 수 있다. 즉, 고체, 액체, 기체, 말랑말랑한 것들 등 다양한 재료를 시뮬레이션할 수 있습니다.

[GitHub - GameTithe/MLS-MPM

Contribute to GameTithe/MLS-MPM development by creating an account on GitHub.

github.com](https://github.com/GameTithe/MLS-MPM)

**참고:** 물질 방정식( constitutive equation )은 모델링하려는 물질을 특징짓는(characterise) 양들(quantities) 간의 관계를 설명한다. 응력(stress), 변형(strain), 압력(pressure), 밀도(density), 탄성(elasticity) 등이 있다.

아래 내용부터는 particle based method에 대한 기초 지식이 있다는 가정을 하고 진행하겠다.

**시뮬레이션의 기본 개념**

시뮬레이션을 하기 위해서는 discretize(이산화)를 해야 한다. 즉 수치적으로 다룰 수 있도록 만드는 과정이 필요한 것이다.

대표적인 이산화 방법으로는

Point Cloud(ex. particle), Discrete Grid(ex. voxel), Mesh(ex. wireframe) 가 있다.

또한 3가지의 관점(viewpoint)을 정해야된다.

#### **1. 라그랑지안(Lagrangian Representation)**

spatial representation에서 변화(deform)에 대한 문제일 때 사용되는 방법이다.

입자 기반 시뮬레이션에서 많이 사용된다. (ex. SPH, PBF, FEM)

#### 

#### **2. 오일러리안(Eulerian Representation)**

공간을 고정된 격자(grid)를 기준으로 공간을 나누어서 시뮬레이션하는 방법이다.

grid에 맞는 속도/밀도 등의 연속적인 물리량으로 정해진 위치에서 계산하는 방법이다.

(ex. MAX, Lattice-Boltzmann)]

#### 

#### **3. 하이브리드(Hybrid Methods)**

위의 두 방법을 적절히 섞어서 사용한다. (ex. MPM)

시뮬레이션 관점에서 봤을 때 특정 frame에서 더 간단하고, 효율적인 방법을 사용할 수 있다.

예를 들면

**Paticels 방법:** mass conservation, advection에 유리하다

**Grid 방:** pressure projection, incompressibility, finite differences에 유리하다.

### 

### **MLS-MPM에 대한 간략한 Background**

### 

**가장 먼저 등장한 방법으로 PIC(paricle-in-cell)가 있다.**



**PIC방법은 기본적으로 잘 동작하지만, 큰 단점으로 정보 소실로 인해 생기는 강한 점성입니다.**

이후에 FLIP이라는 새로운 방법이 개발 되었습니다.

PIC방법에서 Advection(이류)부분에 약간의 변화를 준 방법입니다.



하지만 FLIP방법 또한 단점이 존재합니다.

점성 문제는 많이 해결되었지만, 시뮬레이션이 불안정해졌고, 노이즈가 발생할 가능성(입자가 적은 부분)이 높아졌습니다.

이렇게 Hybrid Method에 대한 연구가 계속 진해되었습니다.

최근 연구에서는 MLS-MPM (Moving Least Squares MPM)이 개발되었습니다.

우리의 첫 번째 목표는 MPM의 "Hello World" 라고 할 수 있는 탄성체를 만들어볼 것이다.

### 

### **Part1**

**위에서 말했던대로 particle과 grid를 합쳐야 되니 paticle과  grid를 위한 class를 만들어 준다.**

```
@dataclass
class Particle:
    x: tuple[float, float]
    y: tuple[float, float]
    mass: float

@dataclass
class Cell:
    v: tuple[float, float] #velocity
    mass: float
```

MPM의 grid는 정보는 매 프레임마다 초기화된다.

즉 한 번의 time step이 끝나면 데이터를 없애고 다시 초기화 해 줄 것이다.

위의 class에는 기본적인 MPM을 구현하기 위한 최소한의 데이터이다.

더 정교하게 시뮬레이션하기 위해서는 몇 가지가 더 필요하다.

더보기

1. deformation gradient matrix

2. volume

3. affine momentum matrix

이건 나중에 신경쓰고 기본적인 틀을 만드는데 집중하자

### **Simultaion Loop**

**아래의 코드는 튜토리얼에서 제공해준 수도코드이다.**

```
Particle[] particles;
Cell[] grid;

void initialise() {
    // 1. 그리드 초기화:
    // grid 배열을 (grid_res × grid_res) 개의 셀로 채워서 초기화합니다.

    // 2. 입자 생성:
    // 입자들을 생성하고 시뮬레이션 도메인 내 임의 위치에 배치합니다.
    // 초기 상태의 입자들은 아직 변형되지 않았으므로 변형 그래디언트를 단위 행렬(identity matrix)로 초기화합니다.

    // 3. (선택 사항) 상태 변수 사전 계산:
    // 사용하는 모델에 따라 입자의 초기 부피(volume) 등과 같은 상태 변수를 미리 계산할 수 있습니다.
}

void each_simulation_step() {
    // 1. 임시 그리드 초기화 (scratch-pad grid 초기화)
    foreach (var cell in grid) {
        // 셀의 질량(mass)과 속도(velocity)를 0으로 초기화합니다.
    }

    // 2. Particle-to-Grid (P2G):
    // 목적: 입자에서 그리드로 데이터를 전달합니다.
    foreach (var p in particles) {
        // 2.1 입자 위치 주변 3x3개의 인접 셀에 대한 보간(interpolation) 가중치를 계산합니다.

        // 2.2 구성 방정식(constitutive equation)을 기반으로 응력(stress) 등과 같은 물리량을 계산합니다.

        // 2.3 입자의 운동량(momentum)을 주변 셀에 흩뿌려(scatter) 줍니다.
        foreach (var cell in particle_neighbourhood) {
            // 2.1에서 계산한 보간 가중치를 사용하여 입자의 운동량을 각 셀에 분산합니다.
        }
    }

    // 3. 그리드 속도 계산:
    foreach (var cell in grid) {
        // 3.1 P2G 단계에서 얻은 운동량을 이용해 각 셀의 속도를 계산합니다.

        // 3.2 경계 조건(boundary conditions)을 적용합니다.
    }

    // 4. Grid-to-Particle (G2P):
    // 목적: 그리드에서 계산된 데이터를 다시 입자에 전달하고, 입자의 위치와 속도를 업데이트합니다.
    foreach (var p in particles) {
        // 4.1 MLS-MPM의 속도 그래디언트 추정 방법을 이용해 입자의 변형 그래디언트(deformation gradient)를 업데이트합니다.
        // 참조: MLS-MPM 논문의 식 (17)

        // 4.2 앞선 단계(2.1)에서 했던 것처럼 다시 입자 주변 셀의 가중치를 계산합니다.
        // 주의: 이 단계까지는 입자의 위치가 아직 바뀌지 않았으므로 가중치 값은 이전과 동일합니다.

        // 4.3 입자의 새로운 속도를 계산합니다.
        foreach (var cell in particle_neighbourhood) {
            // 4.3.1 각 셀의 속도가 보간 가중치로 입자의 새 속도에 미치는 기여를 계산합니다.
        }

        // 4.4 계산된 속도를 이용하여 입자의 위치를 갱신(advect)합니다.
    }
}
```

이부분을 구현할 때는 demormation이 적용되지 않은 시뮬레이션이니

p2g, g2p를 중점으로 코드를 보고 구현하면 될 것이다.

![](https://blog.kakaocdn.net/dna/cJpGXQ/btsMDAtNhqo/AAAAAAAAAAAAAAAAAAAAAIirPYTEntBoHd16suqEK3OH_2t6cXBsY3wadSFCIeZh/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nnPKpKG8vBqgxoTKvIQ2LmQvGWA%3D)

### **Part2: Hyper-Elastic**



여기서는 deformation gradient와 affine momentum matrix를 사용해서 탄성체를 구현한다.

아래 코드를 보면서 어떻게 하라는건지 싶지만,, 실제 사이트에서도 딱히 추가 설명은 없다.

주석으로 식이 어디서 왔는지만 설명해줄 뿐...

일단 본인이 공부한 것을 최대한 정리는 해보겠다.

```
@ti.func
def P2G():
    
    for i in particles: 
        
        # deformation gradient
        F = particles[i].F
        
        # determinant of deformation gradient
        J = ti.math.determinant(F)
        
        # MPM Cours, page 46
        volume = particles[i].volume_0 * J
        
        # Neo-Hookean model (MPM course equation 48)
        # P(Piola kirchoff)를 구하고, F(deformation gradient)를 사용해서..
        F_T = ti.Matrix.transpose(F)
        F_inv_T = ti.math.inverse(F_T)
        F_minus_F_inv_T = F - F_inv_T

        P_term_0 = elastic_mu * F_minus_F_inv_T
        P_term_1 = elastic_lambda * ti.math.log(J) * F_inv_T
        P = P_term_0 + P_term_1
        
        # cauchy stress (MPM course equation 38)
        # P(piola kirchoff)를 이용해서 응력을 구한다
        stress = (1.0 / J) * P @ F_T
        
        eq_16_term_0 = -volume * 4 * stress * dt
        
        cell_idx = ivec3([int(particles[i].pos.x), int(particles[i].pos.y), int(particles[i].pos.z)])
        cell_diff = (particles[i].pos - cell_idx) - 0.5
        
        weights = [0.5 * pow(0.5 - cell_diff, 2), 0.75 - pow(cell_diff, 2), 0.5 * pow(0.5 + cell_diff, 2)]

        for gy in ti.static(range(-1, 2)):
            for gx in ti.static(range(-1, 2)):
                weight = weights[gx + 1][0] * weights[gy + 1][1]
                cell_x = ivec3([cell_idx.x + gx, cell_idx.y + gy, cell_idx.z])

                c_idx = cell_x.y * grid_res + cell_x.x  
                if 0 <= c_idx < cell_count: 
                    cell_dist = (cell_x - particles[i].pos) + 0.5
                     
                    
                    Q = particles[i].C @ cell_dist.xy

                    weighted_mass = weight * particles[i].mass
                    grid[c_idx].mass += weighted_mass

                    grid[c_idx].vel += weighted_mass * (particles[i].vel.xy + Q)                
                    momentum = (eq_16_term_0 * weight) @ cell_dist.xy
                    grid[c_idx].vel += momentum
```

### **1. Volume**

F(deformation gradient) 는 변형률을 계산할 때 사용하는 기본적인 양이다.

X: 변형 전 상태

x: 변형 후 상태

![](https://blog.kakaocdn.net/dna/1PfTf/btsMEC5fMvT/AAAAAAAAAAAAAAAAAAAAAHLy-BIXvqPTHQ03c8uPyUu8h3WTa0UnjbA58fcBYDsH/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=TIHwvN3mAFRLHnhPcQPJ0rkCtP0%3D)

J는 변형이 되었을 때 Volume Change Ratio (체적변화률)이다**.**

![](https://blog.kakaocdn.net/dna/JEPpE/btsMDRB4eEm/AAAAAAAAAAAAAAAAAAAAAJo4cm_nzlHDza-W45VaTOzAdMnz-w9wQTuqbMIKQvo3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Pvd%2FYPlXbWuDdum%2BjPOFPwdgAUY%3D)

Volume을 구하는 방법은 J \* Volume 이다.

![](https://blog.kakaocdn.net/dna/dh1lFu/btsMDwFeVCQ/AAAAAAAAAAAAAAAAAAAAABPDQPIfsa9twpCwwCFNXpJnPHT847CehzFUPp3LvZI_/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hg5v%2BXP%2BS%2Bi3X%2BP50aLcOoX6BAc%3D)

### **2. Stress**

### **Piola Kirchoff  Stress ( Neo-Hookean Model )**

P(Piola Kirchoff), Ψ(energy density function), F(deformation gradient)

아래 식을 여차저차 정리하면 (Neo Hookean 모델을 사용해서)

![](https://blog.kakaocdn.net/dna/CKz6n/btsMF1jGb8v/AAAAAAAAAAAAAAAAAAAAADCGZhgWs3fd_UbiIzf6Zl7quvyC1FCGBjYclo1syiH2/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=7dc8tFNj6LtgIeEdofJl2H%2BZNkk%3D)

다음과 같이 된다. 이건 코드로 구현 가능하다.

![](https://blog.kakaocdn.net/dna/QUUS7/btsMDHNlXeB/AAAAAAAAAAAAAAAAAAAAADWHUDDjVeTrQ0q7bZdlDUyXDjFBeFrzPwOTM67rIoCb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3f4GKyjqWQSOLj%2BMbxmLScyxDmY%3D)

```
 # Neo-Hookean model (MPM course equation 48)
        # F(deformation gradient)를 사용해서 P(Piola kirchoff)를 구하고,
        F_T = ti.Matrix.transpose(F)
        F_inv_T = ti.math.inverse(F_T)
        F_minus_F_inv_T = F - F_inv_T

        P_term_0 = elastic_mu * F_minus_F_inv_T
        P_term_1 = elastic_lambda * ti.math.log(J) * F_inv_T
        P = P_term_0 + P_term_1
```

### **Cauchy Stress**

**위에서 구한 식들을 조합하면 Cauchy Stress를 구할 수 있다.**

![](https://blog.kakaocdn.net/dna/bjbybY/btsMErweD0D/AAAAAAAAAAAAAAAAAAAAAJhpe9VjILyT4OXcQ7pj_suzFqAx8JNJsnezJLSc7GPC/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=0YlIBQSw0ohdWcPFR8SqXPFszi0%3D)

```
stress = (1.0 / J) * P @ F_T
```

### **정리**

Piola Kirchoff Stress는 아래의 공식으로 구할 수 있고,

![](https://blog.kakaocdn.net/dna/QUUS7/btsMDHNlXeB/AAAAAAAAAAAAAAAAAAAAADWHUDDjVeTrQ0q7bZdlDUyXDjFBeFrzPwOTM67rIoCb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3f4GKyjqWQSOLj%2BMbxmLScyxDmY%3D)

이를 사용해서 Cauchy Stress를 사용해서 시뮬레이션에 적용한다는 것

![](https://blog.kakaocdn.net/dna/bjbybY/btsMErweD0D/AAAAAAAAAAAAAAAAAAAAAJhpe9VjILyT4OXcQ7pj_suzFqAx8JNJsnezJLSc7GPC/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=0YlIBQSw0ohdWcPFR8SqXPFszi0%3D)

### **3. Momentum**

![](https://blog.kakaocdn.net/dna/2tbDN/btsMDGOB5H9/AAAAAAAAAAAAAAAAAAAAAJU9UrD1GpYR_yzaPYBuJa_LJjByTV0_8Vgi-NxNsk88/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=iyYg4gVBDD03EVtnmnWwj38FZyI%3D)

이부분을 코드로 바꾸면 아래와 같이 된다.

![](https://blog.kakaocdn.net/dna/b0heCY/btsMEJwA3Qj/AAAAAAAAAAAAAAAAAAAAAKm2_tYFnmjeUheA0N1Sn6C_sB2vtEzJ1WPRRSEIIj-_/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=PmJhBENZwFkFGEeojG541xWMABw%3D)

```
 eq_16_term_0 = -volume * 4 * stress * dt

# ...

momentum = (eq_16_term_0 * weight) @ cell_dist.xy
```

### 

### **4. APIC ( Affine Particle In Cell )**

입자의 운동 정보를 **속도 v 가 아니라 mv 형태로 저장**하는 이유는 **운동량을 보존하기 위해서야.**  
이 방식이 물리적으로 타당한 이유는, 시뮬레이션에서**질량이 다른 입자들이 동일한 격자로 모일 때, 평균적인 속도를 계산할 수 있도록 하기 위해서다.**

즉, **입자의 질량이 다르면 단순히 속도를 평균 내면 안 되고, 운동량을 고려해야 함.**

![](https://blog.kakaocdn.net/dna/dEWpvx/btsMEMOMemv/AAAAAAAAAAAAAAAAAAAAABb4MTjB-UnXPCUV30vND5zx7byrioGDZUFEkqNrxYII/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fQY0aMkiYQf%2FM%2FVcFWrC0Yt4flU%3D)

Q가 아래 식이라고 생각하면 코드와 일치한다.

![](https://blog.kakaocdn.net/dna/DJ7D5/btsMDG1980l/AAAAAAAAAAAAAAAAAAAAAANH8n8LfJd86JQU1v9M7LQNH45fMSVLWn_wQMVKN7CX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=s4Fnce5vxwrWCZPF9uV18Xrkfl4%3D)

```
                    grid[c_idx].vel += weighted_mass * (particles[i].vel.xy + Q)
```

그리고 C (velocity gradient)부분이 아래 식이라고 생각하면 맞는 코드이다.

![](https://blog.kakaocdn.net/dna/2yeBX/btsMEROV8d6/AAAAAAAAAAAAAAAAAAAAAEFECaTw8JjpaU-uHznMHFDzfxKyTPCwhvhA_If627ah/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=gqQn0DGbTiUU%2BqrN5Ql4FyPLG2s%3D)

```
Q = particles[i].C @ cell_dist.xy
```

그리고 나중에 C는 이렇게 정의된다.

```
        particles[i].C = B * 4
```

D가 아래 처럼 나와있지만 우리는 Quadratic 보간 방법을 사용중이고, Quadratic의 역함수는 4이기에 B\*4가 등장한 것

![](https://blog.kakaocdn.net/dna/bIiiHL/btsMDhO7fup/AAAAAAAAAAAAAAAAAAAAAAPBi8qevrUt3x2ksni_QMUnvY4s8FE-rqKnK-lORTwD/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2F7dQwhwmsKhqT6MJ2ZPf3h2%2FHG0%3D)

후.. 여기기까지가 G2P 내용이고, 이제 P2G를 파보자

```
@ti.func
def G2P():
    for i in particles: 
        
        particles[i].vel.fill(0.0)
        
        cell_idx = ivec3([int(particles[i].pos.x), int(particles[i].pos.y), int(particles[i].pos.z)])
        cell_diff = (particles[i].pos - cell_idx) - 0.5
        
        weights = [0.5 * pow(0.5 - cell_diff, 2), 0.75 - pow(cell_diff, 2), 0.5 * pow(0.5 + cell_diff, 2)]
        B = ti.Matrix.zero(dt=ti.f32, n=2, m=2)

        for gy in ti.static(range(-1, 2)):
            for gx in ti.static(range(-1, 2)):
                weight = weights[gx + 1][0] * weights[gy + 1][1]
                cell_x = ivec3([cell_idx.x + gx, cell_idx.y + gy, cell_idx.z])
                
                c_idx = cell_x.y * grid_res + cell_x.x

                if 0 <= c_idx < cell_count:
                    cell_dist = (cell_x - particles[i].pos) + 0.5
                    weighted_velocity = grid[c_idx].vel * weight

                    term = weighted_velocity.outer_product(cell_dist.xy)
                    
                    B += term
                    
                    particles[i].vel += vec3(weighted_velocity.x, weighted_velocity.y, 0.0)
        
        particles[i].C = B * 4
        particles[i].pos += particles[i].vel * dt
        particles[i].pos = clip_vec3(particles[i].pos, 1, grid_res - 2)
```

.

### 

### **1. APIC**

APIC가 Affine Particle In Cell이지만 Cell to Particle 공식도 제공해준다 :)

grid to particle 공식은 아래와 같다.

![](https://blog.kakaocdn.net/dna/bvv7yX/btsMDA2x7bq/AAAAAAAAAAAAAAAAAAAAAOC6-8TF1wOlsGPJV2xAJJl5FmA-cwijBgHWOMJCKUWe/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=sqY2%2BJAlyJV%2BlMGz2y41jSZXOPE%3D)

```
                    cell_dist = (cell_x - particles[i].pos) + 0.5
                    weighted_velocity = grid[c_idx].vel * weight

                    term = weighted_velocity.outer_product(cell_dist.xy)
                    
                    B += term
```

이 부분은 위에 설명이 있다.

```
        particles[i].C = B * 4
```

## **Part3 Fluid with MPM**

위에서 Neo-Hookend모델에서 mu와 lamda를 잘 조절하면 살짝 어색하지만 fake fluid를 흉내낼 수는 있다.

우리가 선택한 모델은 고체 모델로 탄성체를 표현한 것이기 때문에 유체를 시뮬레이션하기 위해서는 살짝 변경을 할게 생깁니다.

첫번째로 할 일은 우리가 사용하던  Cauchy model을 뉴턴 유체 모델로 바꾸는 일이다.

아래는 뉴턴 유체식이다.

![](https://blog.kakaocdn.net/dna/9FIFD/btsME51mfat/AAAAAAAAAAAAAAAAAAAAAOb7x8YYlc9yttbsc1YJLjOXyqZwjcX9m8mKdcj123jQ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Hc37bSc9Nd4gF2k91ZtAqOWy1Z8%3D)

첫 번째 항:

![](https://blog.kakaocdn.net/dna/dFdS05/btsMFMz0nQB/AAAAAAAAAAAAAAAAAAAAAEpdJq45FcgigtYnZl1nW7MLSzIVpPf3f_Sm4c2OjQkn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=2CV%2FJS4zf2jFxSnzht02UdXUm1k%3D)

```
        stress = mat2([-pressure, 0], [0, -pressure])
```

두 번째 항:

![](https://blog.kakaocdn.net/dna/CVybw/btsMEYVzaA6/AAAAAAAAAAAAAAAAAAAAABdgjCWtPiAxr5AZP640P1oS7i9cmAhmPvq5f5feVen-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=IMUBjjxkro5fidYkb3rr5ju2Cmc%3D)

여기서 조금의 트릭이 들어가는데

변형률 텐서(strain tensor)는 뉴턴 유체에서 항상 symmetric matrix이다.

그래서 아래의 코드가 성립한다고 볼 수 있다. ( 2\* 하는 느낌s )

그리고 변형률 텐서를 symmetric matrix로 바꿔주는 것도 포함되어있다.

```
        trace = strain[0, 1] + strain[1,0]
        strain[0,1] = strain[1,0] = trace
```

이렇게 구한 점성응력을 stree에 더해준다 ( 압력기반 응력이 이미 할당되어있으니 += 을 사용하자 )

```
        viscosity_term = dynamic_viscosity * strain
        stress += viscosity_term
```

마지막으로 아래 코드 부분은 part3의 momentum 부분과 일치하기에 그 부분을 참고하쇼

```
    eq_16_term_0 = -volume * 4 * stress * dt
        
        for gy in ti.static(range(-1, 2)):
            for gx in ti.static(range(-1, 2)): 
                    weight = weights[gx + 1][0] * weights[gy + 1][1]
                    cell_x = ivec3([cell_idx.x + gx, cell_idx.y + gy, cell_idx.z])
                    c_idx = cell_x.y * grid_res + cell_x.x
                    
                    if 0 <= c_idx < cell_count:   
                        cell_dist = (cell_x - particles[i].pos) + 0.5
                        momentum = (eq_16_term_0 * weight ) @ cell_dist.xy
                        grid[c_idx].vel += momentum
```

이렇게 고생을 하면 처음 봤던 영상처럼 시뮬레이션을 할 수 있다.

APIC정리

더보기

입자-격자(PIC)에서 각운동량 손실로 인해 발생하는 회전 아티팩트를 보정하기 위해 piecewise rigid formulation 을 도입했지만, 이는 여전히 전단(shearing)과 같은 비강체 운동을 감쇠시킨다.

우리는 piecewise rigid formulation 을 사용하는 대신 각 입자에서 국부적으로(locally) 어파인(affine) 속도를 이상함으로써 속도표현을 강화하여 shearing mode를 다룰수 있도록 했다. 이것을 하기 위해서는 행렬 C, grid x에서의 particle 속도가 필요하다.

식은 아래와 같다.![](https://blog.kakaocdn.net/dna/c92jPq/btsMD5OuDsY/AAAAAAAAAAAAAAAAAAAAAIxQUbBQ7527X5etuFqP8Iq49-IUu-twegxR44EYZg84/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=cqibR1a%2FPBh%2FoHkzSACVEdYRj3U%3D)

이 방법은 각운동량을 명시적으로 보존하기 보다는,a ffine 속도장을 보존하려고 한다. 그러나 affine 속도장의 보존에서 유도된 간단한 해법이 각운동량도 보존한다는 것을 보충 문서에서 보여준다.