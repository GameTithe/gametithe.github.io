---
title: "[CG] 옷 시뮬레이션(import Taichi...!)"
date: 2025-02-28
toc: true
categories:
  - "Tistory"
tags:
  - "taichi"
---

### **Taichi에서의 필드**

더보기

Taichi에서 필드는 전역 데이터 컨테이너로, Python 스코프와 Taichi 스코프 모두에서 접근할 수 있다.

마치 NumPy의 ndarray나 PyTorch의 tensor처럼, Taichi의 필드는 요소들의 다차원 배열로 정의된다.

또한, 필드 내의 요소는 **스칼라(Scalar), 벡터(Vector), 행렬(Matrix), 구조체(Struct)** 중 하나가 될 수 있다.

## **스칼라 필드(Scalar Fields)**

스칼라 필드는 **스칼라 값을 저장하는 필드이다.**

* **0D(0차원) 스칼라 필드**: 하나의 단일 스칼라 값

  ```
  f_0d = ti.field(ti.f32, shape=())
  ```

  ![](https://blog.kakaocdn.net/dna/BB2uE/btsMx6mr0lG/AAAAAAAAAAAAAAAAAAAAAI0S9OOHmkZSWLDfemgr2PGHih6bCe9NWC-0b9jdLf-M/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wuFyZyQAgU2hXQWtvhZAdXM8k%2Bo%3D)
* **1D(1차원) 스칼라 필드**: 스칼라 값들의 1D 배열

```
f_1d = ti.field(ti.i32, shape=9)  # A 1D field of length 9
```

더보기

![](https://blog.kakaocdn.net/dna/cO9rGk/btsMyEiNx5C/AAAAAAAAAAAAAAAAAAAAADRqT0PH0NqnarcHBImMC6Iku5EzDQ7_NyuB065g-fp8/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=YMWq2%2B408Qa%2FoZWKKpHKriOeAPU%3D)

* **2D(2차원) 스칼라 필드**: 스칼라 값들의 2D 배열

```
f_2d = ti.field(int, shape=(3, 6))  # A 2D field in the shape (3, 6)
```

더보기

![](https://blog.kakaocdn.net/dna/bhIZ3j/btsMyBsU6x5/AAAAAAAAAAAAAAAAAAAAAB4wkbMAp8-Oo71PYlmTpi1Zrdniaaw-Cmd6aSAZwC-K/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=iH%2F9csdBlW%2BLeBEsOyvaRf0UlGc%3D)

* 더보기

  **nD(n차원) 스칼라 필드**: 다차원 배열로 확장 가능

![](https://blog.kakaocdn.net/dna/XzPx7/btsMAG7uR8r/AAAAAAAAAAAAAAAAAAAAAIUFR8pEqqmz960eb_doEEc7ZLVQfdul3DKDSW_uJF_v/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=HIvqI7633pql5Zgeo3ZkF%2B4rJgM%3D)![](https://blog.kakaocdn.net/dna/Vc7zW/btsMyj0ivZ1/AAAAAAAAAAAAAAAAAAAAAKhPXOS2AC9Nw2FLhJdh94kGdbs5Nq2CAg0ZqtXXz8yx/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=sR%2FApUNh6evnCxK4%2FucMoMZWP%2B4%3D)

![](https://blog.kakaocdn.net/dna/RqhNp/btsMx9i81R3/AAAAAAAAAAAAAAAAAAAAADwmDYBYSRfdKo3FegHOpBybUTGbBHRNY6gB-MFofMwU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=mCV2dw4QQOxhLt715IJVQS66R10%3D)

.

**천을 n × n 그리드 형태의 질량점(mass point)** 으로 나타내며, 인접한 점들은 스프링으로 연결한다.  
빨간색 점은 질량점(mass point), 흰색 선들은 스프링을 나타낸다.

이 질량-스프링 시스템은 두 개의 배열로 표현할 수 있다.

* **질량점의 위치**를 저장하는 n × n 배열
* **질량점의 속도**를 저장하는 n × n 배열

또한, 위치와 움직임은 다음 네 가지 요인에 의해 영향을 받습니다.

* 중력 (Gravity)
* 스프링의 내부 힘 (Internal forces of the springs)
* 감쇠 (Damping)
* 중앙에 있는 공과의 충돌 (Collision with the ball in the middle)

**구현을 해보자**

기본 세팅이다.

x는 position

v는 velocity이다.

taichi는 kernel decorator를 사용하면, top-level for loop를 자동으로 병렬처리를 해준다.

@ti.kernel을 사용해서 초기화 함수를 병렬로 처리해준다.

```
import taichi as ti 

ti.init(arch=ti.gpu)

n = 128

# x is an n x n field + 3D floating vector 
x = ti.Vector.field(3, dtype = float, shape = (n, n))
v = ti.Vector.field(3, dtype = float, shape = (n, n))

quad_size = 1.0 / n

# automatically parallelize all top-level for loops 
@ti.kernel
def initialize_mass_points() : 
    random_offset = ti.Vector([ti.random() - 0.5, ti.random() - 0.5]) * 0.1 
    
    for i,j in x:
        x[i,j] = [
            i * quad_size - 0.5 + random_offset[0], 0.6,
            j * quad_size - 0.5 + random_offset[1]
        ]
        
        # inital velocity of each mass point is set to 0
        v[i,j] = [0,0,0]
```

### **공 선언**

```
# ball
ball_radius = 0.3
ball_center = ti.Vector.field(3, dtype = float, shape = (1, ))
ball_center[0] = [0,0,0]
```

아래와 같이 center를 field로 선언했다고 보면 된다.

```
float3 center[1]
```

위에서 말했던 force들인데, 차례대로 구현을 해보자.

* 중력 (Gravity)
* 스프링의 내부 힘 (Internal forces of the springs)
* 감쇠 (Damping)
* 중앙에 있는 공과의 충돌 (Collision with the ball in the middle)

### 중력

```
gravity = ti.Vector([0, -9.8, 0])

@ti.kernel
def substep():  
    for i in ti.grouped(x):
        v[i] += gravity * dt
```

```
for i in ti.grouped(x):
```

x의 모든 요소를 자동으로 순회해주는 방법이다. ( 2D, 3D에 구애받지 않는다.)

다중 for문을 사용하지 않도록 도와주는 아주 좋은 함수이다.

### **스프링의 내부 힘 (Internal forces of the springs)**

우리는 다음과 같은 가정을 할 것이다.

**1. 12개의 인접한 이웃 points에만 영향을 받고, 그 외의 points는 영향을 주지 못한다.**

![](https://blog.kakaocdn.net/dna/OsPTS/btsMzr4eaXW/AAAAAAAAAAAAAAAAAAAAAAA7lheBwVx7cvlc82_TARdMQoxzT2utuWCekfbW-ACI/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=qVrl%2FiQ65y8JGPQ6Xip6HuSZ%2BPw%3D)

**2. 이웃한 points는 internal force를 spring을 통해서 가한다.**

여기서 internal force란 스프링의 탄성변화(elastic deformation)와 두 point 간의 damping을 포함하는 개념이다.

![](https://blog.kakaocdn.net/dna/NU1FC/btsMAq4KpBi/AAAAAAAAAAAAAAAAAAAAAE6Tv0_3OCHAtSYwLbHzMQ816_5guSifx0PAgnzs4tG5/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9O4be3qWwdiQ45VCx%2BR64F8Lry8%3D)
![](https://blog.kakaocdn.net/dna/cuFmEo/btsMzfbViBh/AAAAAAAAAAAAAAAAAAAAAOQ1NJhENcsuaDNshmVSi3xyxTjFgDlppxMgoqiLfhLA/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hbUTP81Dps%2BNRA3IHoIp170eyGQ%3D)

위의 공식들을 이용해서 코딩을 해주면 된다. 생각보다 간단하다

```
quad_size = 1.0 / n
 
spring_Y = 3e4  
dashpot_damping = 1e4
 
spring_offsets = []
for i in range(-1, 2):
    for j in range(-1, 2):
        if (i, j) != (0, 0):
            spring_offsets.append(ti.Vector([i, j]))

@ti.kernel
def substep():
   for i in ti.grouped(x):
        force = ti.Vector([0.0, 0.0, 0.0])
        
        for spring_offset in ti.static(spring_offsets):
            j = i + spring_offset
            
            if 0 <= j[0] < n and 0 <= j[1] < n :
                x_ij = x[i] - x[j]
                v_ij = v[i] - v[j]
                
                dir = x_ij.normalized()
                
                current_dist = x_ij.norm()
                original_dist = quad_size * float(i - j).norm()
                
                #Hooke's Law
                force += -spring_Y * dir * (current_dist / original_dist - 1 )
                
                # daming force
                # quad_size -> original_dist? 
                force += -dashpot_damping * (v_ij.dot(dir)) * dir * quad_size

        v[i]  += force * dt
```

### **Damping**

현실 세계에서 스프링 진동은 시간이 지나면서 서서히 줄어든다. 이를 위해서 time step마다 속도를 줄여줄 것이다.

```
# Damping coefficient of springs
drag_damping = 1

@ti.kernel
def substep():

    # Traverse the elements in field v
    for i in ti.grouped(x):
        v[i] *= ti.exp(-drag_damping * dt)
```

### **Collision with the ball**

만약에 옷이 공 안으로 들어가면 안되니, 위치가 공 안이라면 속도를 공의 normal 방향으로 바꿔줄 것이다.

```
# Damping coefficient of springs
drag_damping = 1

@ti.kernel
def substep():

    # Traverse the elements in field v
    for i in ti.grouped(x):

        offset_to_center = x[i] - ball_center[0]
        if offset_to_center.norm() <= ball_radius:
            # Velocity projection
            normal = offset_to_center.normalized()
            v[i] -= min(v[i].dot(normal), 0) * normal
        # After working out the accumulative v[i],
        # work out the positions of each mass point
        x[i] += dt * v[i]
```

이렇게까지 하면 Simulation을 위한 코드는 끝~ 

전체코드는 여기에 올렸습니다

<https://github.com/GameTithe>