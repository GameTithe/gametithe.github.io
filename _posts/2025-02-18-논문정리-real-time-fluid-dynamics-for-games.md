---
title: "[논문정리] Real-Time Fluid Dynamics for Games"
date: 2025-02-18
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

time step에 엄격한 물리적으로 정확한 식이 아니라, 터지거나 하지 않는 stable(안정적인) 알고리즘이다. 

### **The Physics of Fluids**

첫번째: Navier-Stokes Equation의 compact한 벡터 속도장이다. (비선형적)

두번째: 속도장을 지나가는 밀도 식이다. (선형적)

![](https://blog.kakaocdn.net/dna/bVm7Bc/btsMm2QtpOi/AAAAAAAAAAAAAAAAAAAAANEpi0j3maOPz8O-RiZDXijOhQixl4USxL0ykt32tPhE/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ksry%2FBTRly4JMFmoESgoYM5g5H8%3D)

유체의 상태는 **속도 벡터장(velocity vector field)** 으로 모델링된다. 즉, 공간의 각 지점에서 특정한 속도 벡터를 할당하는 함수이다.

**Navier-Stokes Equation**은 시간이 흐름에 따라 속도장이 어떻게 변화하는지를 정밀하게 설명하는 방정식이다.

속도장 자체는 단순한 수학적 개념이지만, 연기(smoke particles), 먼지(dust), 낙엽(leaves) 등의 물체를 이동시키면서 시각적으로 흥미로운 효과를 만들 수 있다.

연기의 경우 개별 입자를 모두 계산하는 것은 비용이 많이 드는 작업이므로, **밀도(density)** 를 이용한다. (두 번째 식)

### **A Fluid in a Box**

![](https://blog.kakaocdn.net/dna/npPWM/btsMkMaWNxq/AAAAAAAAAAAAAAAAAAAAAIyMf3OkIZf1aJsTv3Qlr_h7yDlgJQUIYPNuVZufblhY/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nUmea2Ke6GTfeTJbv%2BfWKGeV8C8%3D)

논문에서 계산한 속도, 밀도 그리드는 모두 셀 중심으로부터 계산된다. 그리고 그리드 주변으로 boundary condition을 쉽게 판단하기 위한 layer가 존재한다.   
  
시뮬레이션하기 위해서는 유한한 방식으로 유체를 표현해야 된다. 일반적인으로 **공간을 동일한 크기의 셀(cell)로 나누고, 각 셀의 중심에서 유체의 상태를 샘플링하는 것**이다.

속도(velocity)와 밀도(density)는 **각 격자 셀 내부에서 일정하다고 가정**한다.

```
size=(N+2)*(N+2)

static u[size], v[size], u_prev[size], v_p rev[size];
static dens[size], dens_prev[size];
```

효율성을 위해서 2차원 배열이 아닌 1차원 배열을 사용한다.

때문에 아래와 같은 매크로가 유용하게 사용된다.

```
#define IX(i,j) ((i)+(N+2)*(j))
```

격자의 각 변의 물리적 길이는 **1**로 가정한다. 따라서 격자 간격(grid spacing)은 **h = 1/N** 이다.

### **Moving Densities**

![](https://blog.kakaocdn.net/dna/bt0Y20/btsMk2q5J3Y/AAAAAAAAAAAAAAAAAAAAALM4pKf9YsSUBFvjPDL-JoQt2byO14nn7vB08Uk7-87R/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Hb3ecSVQRJjByyprPxf%2FJ32prAI%3D)

기본적인 밀도 Solver의 구조이다. time step마다 우측 3개의 terms을 해결해야 된다.

논문에서 먼저 설명할 내용은 **고정된 속도장에 따라 밀도가 이동하는 솔버**이다. (속도가 변하지 않는 것을 가정)

밀도 방정식에서 밀도의 변화는 세 가지 원인으로 인해 발생한다.

**대류(Advection)**: 밀도는 속도장을 따라 이동해야 한다.

**확산(Diffusion)**: 밀도가 일정한 비율로 퍼질 수 있다.

**소스(Source)**: 특정 위치에서 밀도가 추가될 수 있다.

밀도 solver는 **이 세 개의 항을 역순으로 해결**한다.

**밀도 소스 추가 (Source Term) →  확산 해결 (Diffusion Term) → 대류 해결 (Advection Term)** 순서로 진행된다.

### 

### **1. Source Term**

첫 번째 term은 구현하기 쉽다.

source의 값은 s[ ] 배열에 저장되며 game engine에서 제공한다. 프로토타입에서는 **사용자의 마우스 움직임**으로부터 s[ ] 배열이 채워진다.

```
void add_source ( int N, float * x, float * s, float dt )
{
    int i, size=(N+2)*(N+2);
    for ( i=0 ; i<size ; i++ ) 
    	x[i] += dt*s[i];
}
```

### **2. Diffuse Term**

![](https://blog.kakaocdn.net/dna/bQLIGo/btsMl7E4jA0/AAAAAAAAAAAAAAAAAAAAAAHz-VWY4mEC74-X7vjDxLeVhpQEhZ14q_kCasPNoOrB/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KzfnRG80AbZZNa1ubEMhuR10csc%3D)

확산(diffuse)은 **밀도가 주변 셀로 퍼지는 과정**을 의미한다. 확산 비율(diff) > 0이면 **밀도는** **격자 셀을 따라 퍼지게 된다.**

위의 그림이 확산(diffuse)에 따른 이웃 셀간의 밀도 변화를 나타낸 그림이다.

그림에서 보는 것처럼, 각 셀은 **위, 아래, 왼쪽, 오른쪽 네 개의 이웃 셀과 밀도를 교환**한다.

셀의 밀도는 **이웃에게 전달되면서 감소**하지만, 동시에 **이웃 셀로부터 밀도를 받아 증가**하기도 한다.

```
	x[IX(i,j)] = x0[IX(i,j)] + a * ( x0[IX(i-1,j)] + x0[IX(i+1,j)] + x0[IX(i,j-1)] + x0[IX(i,j+1)]
							-4*x0[IX(i,j)]);
```

구현하는 방법이 2가지가 있다.

#### **(1). Explicit (명시적)**

```
	x[IX(i,j)] = x0[IX(i,j)] + a * ( x0[IX(i-1,j)] + x0[IX(i+1,j)] + x0[IX(i,j-1)] + x0[IX(i,j+1)]
							-4*x0[IX(i,j)]);
```

x[IX(i,j)]를 바로 계산하는 방식인데, 이런 방식은 **새로운 밀도 값이 이전 값에 의해 바로 업데이트되는 구조**라서 불안정성이 크다.

다시 말해 grid 업데이트 과정에서 [0,1]이 업데이트가 됐다고 가정하면

[0,2]를 업데이트할 때 **사용되는 [0,1]이 이미 업데이트가 되어서 [0,2]는 불안정해진다.**

**그 뒤 grid는 불안정해진 grid를 사용하기에 더 불안정해질 것이다.**

비선형 시스템이기 때문에 새로운 밀도가 빠르게 변하고 **진동(oscillation)하거나 발산(diverge)하는 문제가 발생**할 수 있다. 아래 식을 보면 f(x)에 따라 비선형으로 변할 수 있다.

![](https://blog.kakaocdn.net/dna/bUOnZl/btsMmqYCb2I/AAAAAAAAAAAAAAAAAAAAAL_98ruiBwlVwX8oZIRm1pY-qDK3ET5KNX7o1T09rcLe/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=sdrnZrsoN2GK8q2V4E7gjsjttpk%3D)

#### **(2) Implicit (암시적)**

```
x0[IX(i,j)] = x[IX(i,j)] −a ⋅ (x[IX(i−1,j)] + x[IX(i+1,j)] + x[IX(i,j−1)] + x[IX(i,j+1)] 
                                                    −4⋅x[IX(i,j)])
```

x[IX(i,j)]를 바로 업데이트하지 않고, 기존의 x[] 값을 유지한 상태에서 x0[]에 값을 계속 저장하다가 한 번에 grid를 교체한다고 생각하면 된다.

우리가 구해야 하는 새로운 값(x)은 **이전 값(b)을 기반으로 연립 방정식을 풀면서 점진적으로 수렴**함.

위의 식을 풀어보면 아래처럼 구해야 될 x가 A(coefficient matrix)에 따른 선형변환이 된다.

**x** : 우리가 구해야 할 현재 상태 값 (속도 또는 밀도).

**b** : 이전 상태 값.

**A** : 인접한 격자(grid)의 영향을 고려한 계수 행렬(coefficient matrix).

![](https://blog.kakaocdn.net/dna/bdNwcE/btsMmH0aKaY/AAAAAAAAAAAAAAAAAAAAAGDLQ1S6N2aJJmGMezNMmuG4Sr1g7f2mVcG9BzD0BQtu/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=NSMqyaFFkVQkb5pwf4JVWQvL8UA%3D)

Implicit한 방법으로 선형 시스템을 행렬로 구성한 후, **표준 행렬 역행렬(matrix inversion) 루틴을 호출하여 풀 수도 있다.**

![](https://blog.kakaocdn.net/dna/begyWq/btsMkZacMD9/AAAAAAAAAAAAAAAAAAAAAIBOvSXUBK8X_SJWkjWr0uFlyIkDEKk2mbuvsyKUVBf-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=srpG%2F4TqJArFaiYyb%2FA4ekBcYmY%3D)
![](https://blog.kakaocdn.net/dna/q6UUO/btsMmriTkp7/AAAAAAAAAAAAAAAAAAAAAK3RZs19eeoedKQ9ZSvTOGteS2Vuy_SBmuFh9tkdTYT_/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Xgo2Is3SK46F%2FqCkM4nKS6v51zE%3D)

**하지만 matrix의 대부분이 sparse(원소가 대부분 0)이기에 비효율적이다.**

가장 간단하면서도 효과적으로 잘 동작하는 방법이 **가우스-자이델(Gauss-Seidel) 완화법(relaxation method)** 이다.

implicit 식을 풀어서 정리하면 이렇게 나온다.

```
x[IX(i,j)] = (x0[IX(i,j)] + a*(x[IX(i-1,j)] + x[IX(i+1,j)] +
                               x[IX(i,j-1)] + x[IX(i,j+1)])) / (1 + 4 * a);
```

```
void diffuse ( int N, int b, float * x, float * x0, float diff, float dt )
{
    int i, j, k;
    float a=dt*diff*N*N;
    for ( k=0 ; k<20 ; k++ ) 
    {
    	for ( i=1 ; i<=N ; i++ ) 
        {
        	for ( j=1 ; j<=N ; j++ ) 
        	{
        		x[IX(i,j)] = (x0[IX(i,j)] + 
				a*(x[IX(i-1,j)]+x[IX(i+1,j)]+ x[IX(i,j-1)]+x[IX(i,j+1)]))/(1+4*a);
        	}
        }
        set_bnd ( N, b, x );
    }
}
```

이 버전의 장점은 **불안정한 버전만큼 간단하지만 diff, dt 또는 N에 대한 모든 값을 처리할 수 있다는 점이다.** **값이 아무리 크더라도 시뮬레이션이 망가지지 않습니다.**

가우스 자이델:

**<https://study2give.tistory.com/entry/%EC%88%98%EC%B9%98%ED%95%B4%EC%84%9D-%EA%B0%80%EC%9A%B0%EC%8A%A4-%EC%9E%90%EC%9D%B4%EB%8D%B8Gauss-Seidel-%EB%B2%95>**

### 

### **3. Advection**

![](https://blog.kakaocdn.net/dna/Li4CI/btsMlh2Kx5S/AAAAAAAAAAAAAAAAAAAAAF3CwwmB5scp6N338uzfNABbgHyKutPck84UxDM0ZjMg/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ruuOwhV355daJU5bu1ezc8MpVEI%3D)

static한 속도 벡터 필드를 통과하면서 밀도가 움직이는 모습이다.

이번에는 방정식이 **velocity field에 따라 결정되기 때문에 가우스-자이델 방법으로 해결하기 어렵다.**

**새로운 접근법**을 사용해야되는데, 이 방법이 더 쉽게 해결해준다.

핵심 아이디어는 **밀도를 개별 입자(particles)로 모델링하는 것**이다.

만약 **각 격자 셀을 입자(particle)로 간주**하면, **입자를 velocity field에 따라 이동시키는 것만으로 밀도를 추적할 수 있다**.

예를 들어, **각 격자 셀의 중심(center)을 하나의 입자로 가정**하고, **이 입자가 속도장에 따라 어떻게 움직이는지 추적(track)하면 된다. (b)번 그림**

![](https://blog.kakaocdn.net/dna/blinMB/btsMlljKuXn/AAAAAAAAAAAAAAAAAAAAAEV1bII-Svml4iW2r43Gc2pgfTCcKa-WczT31cxCy4Re/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=uZ%2Fu6yScq2dE6YH3rF0PGERNZ0I%3D)

문제는, **이 입자를 다시 격자(grid) 값으로 변환하는 과정이 필요**하다는 것.

단순히 입자를 속도장에 따라 이동시키면, **다시 격자로 변환하는 과정이 쉽지 않다.**

이를 해결하기 위해서 **격자 위치에 도달하는 입자를 역추적(Backtrace) 할 것 이다**. (c)번 그림

grid의 가운데 정확히 도달하는 입자가 어디서 출발했는지 찾는 방법이다.

we look for the particles which end up exactly at the cell centers by tracing backwards in time from the cell centers (c).

backtrace한 부분은 grid의 중앙 부분이 아닐 수 있으니, 주변 이웃 4곳에서 선형 보간으로 값을 구한다.  
 

간단하게 구현하면 아래와 같다

backtrace하는 부분이라고 볼 수 있다.

```
x = i-dt0*u[IX(i,j)]; y = j-dt0*v[IX(i,j)];
```

비율에 맞게 선형 보간하는 부분이다.

```
 s1 = x-i0; s0 = 1-s1; t1 = y-j0; t0 = 1-t1;
        d[IX(i,j)] = s0 * ( t0*d0[IX(i0,j0)] 
        			+ t1*d 0[IX(i0,j1)])
        			+ s1*(t0*d0[IX(i1,j0)]
        			+ t1*d0[IX(i1,j1)]);
```

```
void advect ( int N, int b, float * d, float * d0, float * u, float * v, float dt )
{
int i, j, i0, j0, i1, j1;
float x, y, s0, t0, s1, t1, dt0;
dt0 = dt*N;
for ( i=1 ; i<=N ; i++ ) 
{
    for ( j=1 ; j<=N ; j++ ) 
    {
        x = i-dt0*u[IX(i,j)]; y = j-dt0*v[IX(i,j)];
        if (x<0.5) x=0.5; if (x>N+0.5) x=N+ 0.5; i0=(int)x; i1=i0+1;
        if (y<0.5) y=0.5; if (y>N+0.5) y=N+ 0.5; j0=(int)y; j1=j0+1;
        s1 = x-i0; s0 = 1-s1; t1 = y-j0; t0 = 1-t1;
        d[IX(i,j)] = s0 * ( t0*d0[IX(i0,j0)] 
        			+ t1*d 0[IX(i0,j1)])
        			+ s1*(t0*d0[IX(i1,j0)]
        			+ t1*d0[IX(i1,j1)]);
    }
}
    set_bnd ( N, b, d );
}
```

이렇게 밀도 time step에 사용할 모든 구성을 학습했다.

```
void dens_step ( int N, float * x, float * x0, float * u, float * v, float diff, float dt )
{
    add_source ( N, x, x0, dt );
    SWAP ( x0, x ); diffuse ( N, 0, x, x0, diff, dt );
    SWAP ( x0, x ); advect ( N, 0, x, x0, u, v, dt );
}
```

### 

### **Evolving Velocities**

이제 velocity solver에 대한 이야기이다!

속도 방정식은 세 가지 요소에 영향을 받는다.

1. 외부의 힘 (Force)

2. 점성 확산 (Viscous Diffusion)

3. 자기-이류 (Self-Advection)

![](https://blog.kakaocdn.net/dna/bbKdC3/btsMnE3qEul/AAAAAAAAAAAAAAAAAAAAAI5baRXDCgaxlCEbYFEn_Ps0y4zmkI6M-MbLLO8FmppT/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=8mhU9M6rI%2Bhnc2LxHOWuNIePlJ0%3D)

속도를 업데이트하는 코드입니다.

```
void vel_step ( int N, float * u, float * v, float * u0, float * v0, float visc, float dt )
{
    add_source ( N, u, u0, dt ); add_source ( N, v, v0, dt );
    SWAP ( u0, u ); diffuse ( N, 1, u, u0, visc, dt );
    SWAP ( v0, v ); diffuse ( N, 2, v, v0, visc, dt );
    project ( N, u, v, u0, v0 );
    SWAP ( u0, u ); SWAP ( v0, v );
    advect ( N, 1, u, u0, u0, v0, dt ); advect ( N, 2, v, v0, u0, v0, dt );
    project ( N, u, v, u0, v0 );
}
```

위에서 구한 밀도solver와 비슷한 모습이지만, 중요한 차이점은 project()함수가 추가 되었다는 것이다.

projection은 속도가 질량 보존이 되도록 강제하고, 소용돌이 같은 흐름을 생성한다.

![](https://blog.kakaocdn.net/dna/bheXz0/btsMnl4fVQg/AAAAAAAAAAAAAAAAAAAAALa9YVk_-FV8PN3x2OyeG-u7gwncr8s1HfEyvKmNc3yM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=oRwCs2xQIYuidL0fFL3bS%2B%2BHRK8%3D)

상단 그림: 속도장 = 비압축성 필드 + 그래디언트 필드

하단 그림: 압축성 필드 = 속도장 - 그래디언트 필드

왜 그런가..! ( 그렇구나 하고 넘어가도 무방 )

더보기

식을 이해하기 위해서는 Helmholtz-Hodge Decomposition을 알면 좋다.

최하단에 관련해서 정리해 놓겠다 여기서는 필요한 부분만 간단히 설명하겠습니다.

속도장은 Usol + Uirrot으로 구성되어있다는 것이다.

Usol: 발산이 없는 부분 (mass conserving)

Uirrot: 회전이 없는 부분 (gradient field)

![](https://blog.kakaocdn.net/dna/cjOZ9c/btsMmmP3tnc/AAAAAAAAAAAAAAAAAAAAALoz6NHEcoy6XlN_SdS7v1mF3pHVIfDlaTPYoYguFjWf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=G1x4LnOa70mRrGnVnP8sCBPWETM%3D)

이 식과 그림을 같이 보면 이해하기 좋을 것이다.

 좋은 소용돌이를 얻기 위해서 질량 보존(mass conserving) 속도장이 필요하기 때문에

속도장 - gradient fileld를 해서 구하면 된다

![](https://blog.kakaocdn.net/dna/cjOZ9c/btsMmmP3tnc/AAAAAAAAAAAAAAAAAAAAALoz6NHEcoy6XlN_SdS7v1mF3pHVIfDlaTPYoYguFjWf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=G1x4LnOa70mRrGnVnP8sCBPWETM%3D)

복잡한 수학적 세부 사항은 생략하겠지만, 이 필드를 계산하는 것은 푸아송 방정식(Poisson equation)이라고 불리는 선형 방정식을 푸는 것과 관련된다.

이 방정식은 희소 행렬(sparse matrix) 형태이며, 밀도 확산(density diffusion) 단계에서 사용했던 가우스-자이델 반복법(Gauss-Seidel Relaxation)을 재사용하여 풀 수 있다.

(논문에서는 설명하지 않아서 지금 설명하지 않지만 최하단에서 설명을 적어 놓겠다.)

(project()를 두번해주는 이유는 질량 보존 field일 때 더 잘 동작하기 때문이다.)

```
void project ( int N, float * u, float * v, float * p, float * div )
{
    int i, j, k;
    float h;
    h = 1.0/N;
    
	for ( i=1 ; i<=N ; i++ ) 
    {
        for ( j=1 ; j<=N ; j++ ) 
        {
            div[IX(i,j)] = -0.5*h*(u[IX(i+1,j)]-u[IX(i-1,j)]+
            v[IX(i,j+1)]-v[IX(i,j-1)]);
            p[IX(i,j)] = 0;
    	}
    }
    set_bnd ( N, 0, div ); set_bnd ( N, 0, p );
    for ( k=0 ; k<20 ; k++ ) 
    {
        for ( i=1 ; i<=N ; i++ ) 
        {
            for ( j=1 ; j<=N ; j++ ) 
            {
            p[IX(i,j)] = (div[IX(i,j)]+p[IX(i-1,j)]+p[IX(i+1,j)]+
             p[IX(i,j-1)]+p[IX(i,j+1)])/4;
            }
        }
            set_bnd ( N, 0, p );
    }

	for ( i=1 ; i<=N ; i++ ) 
    {
	    for ( j=1 ; j<=N ; j++ ) 
        {
    	u[IX(i,j)] -= 0.5*(p[IX(i+1,j)]-p[IX(i-1,j)])/h;
    	v[IX(i,j)] -= 0.5*(p[IX(i,j+1)]-p[IX(i,j-1)])/h;
        }
    }
    set_bnd ( N, 1, u ); set_bnd ( N, 2, v );
}
```

(project()를 두번해주는 이유는 질량 보존 field일 때 더 잘 동작하기 때문이다.)

(project()를 두번해주는 이유는 질량 보존 field일 때 더 잘 동작하기 때문이다.)

아래는 시뮬레이션 코드이다.

```
while ( simulating )
{
    get_from_UI ( dens_prev, u_prev, v_prev );
    vel_step ( N, u, v, u_prev, v_prev, visc, dt );
    dens_step ( N, dens, dens_prev, u, v, diff, dt );
    draw_dens ( N, dens );
}
```

끝!

최하단

### **Chorin Projection Method**

비압축성 유체 흐름 문제를 효과적으로 푸는 방법으로, Navier-Stokes 방법정식을 푸는데 효과적이다.

Helmholtz Decomposition(헬름홀츠 분해)의 기반한 알고리듬이다.   
Solenoidal Part(발산 없는 부분 ), Irrotational Part(회전 없는 부분) 으로 분해해야된다.

**(발산이 없다는 것은 움직이지 않는다는 의미가 아니라 압축되지 않는다, 팽창하지 않는다는 의미이다.)**

첫 번째**: 비압축성 조건을 만족하지 않는** intermediate velocity(중간속도)를 계산한다.

두 번째: 압력(pressure)을 이용하여 intermediate velocity(중간 속도)를 divergence-free velocity field(발산이 없는 속도장)으로 projection하여 다음 단계의 속도와 압력을 얻는다.

Helmholtz-Hodge Decomposition

속도장 u는 위에서 말한 Solenoidal 부분, Irrotational 부분으로 분해될 수 있다. 

![](https://blog.kakaocdn.net/dna/cjOZ9c/btsMmmP3tnc/AAAAAAAAAAAAAAAAAAAAALoz6NHEcoy6XlN_SdS7v1mF3pHVIfDlaTPYoYguFjWf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=G1x4LnOa70mRrGnVnP8sCBPWETM%3D)

**U**irrot 부분은 회전이 없는 속도장이기 때문에 미분을 취할 수 있기에, 어떤 스칼라 함수 ϕ의 그라디언트(gradient)로 표현할 수 있다.

이때 **그라디언트 연산자의 회전(Curl)은 항상 0이므로**

![](https://blog.kakaocdn.net/dna/bTZ4MT/btsMnBMefmc/AAAAAAAAAAAAAAAAAAAAAEAP67WEXdNiIiCXwXDZ-8q7I9EC_hLI40DTR3j8xeUf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=owtWC%2BklqqQQWdec7Ib2XBXQP7Y%3D)

왼쪽 식에 divergence를 취하면 Usol은 발산이 0이기 때문에, 오른쪽 식과 같이 된다.

![](https://blog.kakaocdn.net/dna/beMso6/btsMlkeCPun/AAAAAAAAAAAAAAAAAAAAACJIQW0iS1_mEB2-hnUMcfF2yJDEBiYt6T35cmrylvJK/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=kaWw74PjEv5H7JV6GXxBF1VVBrk%3D)![](https://blog.kakaocdn.net/dna/c56oBO/btsMly4NKgg/AAAAAAAAAAAAAAAAAAAAAJvT28cVs50tcfMyJo_lCkVwk3ytvrhEW5r1Th3KKASS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=MULsGN6EKZT5Iz8KfrtSYfKYWUM%3D)

오른쪽 방정식을 풀어 ϕ를 구하면, 비압축성(발산이 없는) 속도장 Usol을 구할 수 있다.

![](https://blog.kakaocdn.net/dna/da1NJP/btsMlo88HLE/AAAAAAAAAAAAAAAAAAAAANUgvkHui03eZU08OtIadAnCoyhZufFSzeQOejTHl6Q1/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Ce00W3urqnbEXGBUktrJcdcW5Co%3D)

이제 실제 식이 적용시켜보자

이 식이 비압축성 Navier-Stokes 식이다.

![](https://blog.kakaocdn.net/dna/uN1n2/btsMnkYlpe8/AAAAAAAAAAAAAAAAAAAAAKO46-oGeTFYMZTiIMFfdekNZF0pZ2wdD0EPph1GA-CS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3AkM78lIga5wGTu%2BveU%2B%2B0UqTzE%3D)

#### **첫 번째: 비압축성 조건을 만족하지 않는 intermediate velocity(중간속도)를 계산한다.**

첫번째 조건을 위해서 pressure를 제외하고 계산을 한다. (u\*는 intermediate velocity이다)

![](https://blog.kakaocdn.net/dna/cQkWjb/btsMmnao5CC/AAAAAAAAAAAAAAAAAAAAALd7FtVGIGW-ONceP2hm-eF6ysXdpk3itnRwvC4Ij1qU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=YgWogw3QLGEY2JyNlF99HyYUtt4%3D)

#### **두 번째: 압력(pressure)을 이용하여 intermediate velocity(중간 속도)를 divergence-free velocity field(발산이 없는 속도장)**

좌측 식을 정리하면, 우측식이 됩니다. 최종단계의 solution을 얻기 위해서 time step을 n+1로 수정했습니다.

![](https://blog.kakaocdn.net/dna/eoZTin/btsMnSAewUG/AAAAAAAAAAAAAAAAAAAAAHPdmKFukhqlEQMG2UZdXl_4gb4AtfYcuWP5tA8zkT4l/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nHTiGc%2FOYUwqj%2FRvUe3kcGSzbUs%3D)![](https://blog.kakaocdn.net/dna/bmMt6t/btsMml4KtZa/AAAAAAAAAAAAAAAAAAAAAH501YhGZJz5a7iHz0NouRy_2tdS0FPk-G3V109c2Dwt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=zmFlpOy%2Fu98Q3yMGPR6G6rY9TAQ%3D)

두 번째 식에서는 n+1단계에서의 p(압력)을 알아야한다. 이를 위해 **발산 조건( **∇⋅U^n+1 = 0** )**를 적용하여,  
다음과 같은**푸아송 방정식을 도출한다**.

(위의 좌측식에 양변에 divergence를 취하고 정리하면 아래의 식을 얻을 수 있다.)

![](https://blog.kakaocdn.net/dna/G9oPd/btsMlEcX3o5/AAAAAAAAAAAAAAAAAAAAAB1aU8mKhfxi6XheJtkwLLQ_P4pex6zsC6DjlkQj-yk_/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=J7IFhXMHU2U%2FD%2F%2BMb%2FfHPKYFhNI%3D)

정리하면

첫번째의 의미: 점성력(viscous forces)을 고려

두번째의 의미: 압력힘(pressure forces)을 고려

첫번째 단계에서 점성력을 반영해서 중간속도를 계산하고,

두번째 단계에서는 중간속도에 압력보정을 통해 발산이 0인 속도장으로 만든다.