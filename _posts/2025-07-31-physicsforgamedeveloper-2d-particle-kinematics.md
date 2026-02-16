---
title: "[PhysicsForGameDeveloper] 2D Particle Kinematics"
date: 2025-07-31
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

## 

## **2D 입자 운동학 (2D Particle Kinematics)**

1차원 운동, 즉 운동이 직선 상으로 제한되는 경우에는 앞서 배운 공식을 그대로 적용하여  
**순간 속도, 가속도, 위치 변화량** 등을 쉽게 구할 수 있다.

하지만, **운동이 평면 상에서 임의의 방향으로 가능한 2차원 상황**에서는  
속도, 가속도, 변위를 벡터(vector)로 고려해야 한다.

표준 직교 좌표계(Cartesian coordinate system)를 사용할 때는 변위, 속도, 가속도의 **x성분과 y성분**을 모두 고려해야 하며,  
각 성분들을 따로 계산한 뒤 합쳐서 전체 벡터를 구성할 수 있다.

이를 돕기 위해, 단위벡터 i, j 를 각각 x축, y축 방향으로 정하고, 아래와 같이 표기하자.

![](https://blog.kakaocdn.net/dna/DcD7i/btsPDC91JWG/AAAAAAAAAAAAAAAAAAAAAL4mRw9kzmRxRnSH537UM0vYHNRHbRa2ZYGMxmPmmRIr/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ikVRq3TYqSB4y9517%2Fpd6rDFZ9U%3D)

## 

## **2D에서의 위치, 속도, 가속도**

만약 x가 x방향 변위, y가 y방향 변위라면,  
변위 벡터는 다음과 같다.

![](https://blog.kakaocdn.net/dna/A74cB/btsPCJaWi6W/AAAAAAAAAAAAAAAAAAAAAPzmyrrIQFLeZEdBjMks4XWjZJVOtMhG5HnKMqMgzzOQ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fPMr8w7wk3rrnqLIVj21HWriGDY%3D)

그러면 시간 미분을 통해 아래와 같이 표기할 수 있을 것이다.

![](https://blog.kakaocdn.net/dna/zQGHZ/btsPENJIDvf/AAAAAAAAAAAAAAAAAAAAADzl3XPg8Bwp0H4zIBXXcLYha7lnem2ZuMrEeGNwim8k/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=7iksjB5WFlmQ0%2FhIHhSdr%2BHnjOE%3D)

## 

## **사격 게임에서의 낙하 거리 계산**

사격 게임을 만든다고 가정하고,  
총에서 발사된 총알이 목표물에 도달할 때까지  
수직 방향으로 얼마나 낙하(drop)하는지를 계산해야 한다고 해보자.

중력만 작용하고, 바람, 공기 저항이 없다고 가정하자.

=> 이 의미는 따라서 **등가속도 문제**로 단순화가 가능하다

![](https://blog.kakaocdn.net/dna/dPKTa3/btsPDC91T3L/AAAAAAAAAAAAAAAAAAAAADTJc9bGtvIJcm9Vx44jhmcwMsgtGsBPqbwxrw22UNzW/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2B7fjVO30sDIpjp1eB%2FGlrBY8GzY%3D)

좌표계의 원점은 총구 위치로 하고

x축: 목표물

y축: 위로

### 

### **X좌표 성분 해석**

1총랑의 x방향 운동은 일정한 속도 Vm으로 진행되며, 가속도는 없다.

![](https://blog.kakaocdn.net/dna/o4mm3/btsPEChnChH/AAAAAAAAAAAAAAAAAAAAANNMcg8GAXZBfJQ5cRIcrBYf-IwVzeB_gqYZ1KQUOjbe/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=MfOVmJ8t61a1eY6zTZNX1YaVhwo%3D)

### 

### **y좌표 성분 해석**

총알이 발사될 때 y방향 속도는 0이다.

가속도는 중력으로 인해 -g

![](https://blog.kakaocdn.net/dna/lWNxc/btsPC4F1asn/AAAAAAAAAAAAAAAAAAAAAKktiPDwQTasuiebKp_AKbh0t3IbFP9XmIOLf9AFTY8e/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ZE%2BLala%2F3jr5q94sOhY9sg5FPoI%3D)

### **최종 벡터 표현**

s = s0 + v \* t + a \* 1/2 \* a \* t^2

(s0은 0이다)

![](https://blog.kakaocdn.net/dna/rJM4T/btsPCT5F6Gj/AAAAAAAAAAAAAAAAAAAAAMd5U3DAn_7P3oXTXTHsGdb2p9r0GIwR1V63HAwBPvkq/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=6mlNpfSG34ARgqUUcrfURK%2FBQTw%3D)

v = v0 + a \* t

![](https://blog.kakaocdn.net/dna/cL2g0H/btsPCmUBVH3/AAAAAAAAAAAAAAAAAAAAADPfYPye71oTpnSH5at1GaRmWnIYaMK_eD-J_YIDYBMN/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=gBAVCS%2F1VJ%2FTpN%2FBRgoycOy6jk4%3D)

a = -g

![](https://blog.kakaocdn.net/dna/s9ULg/btsPD0QiNIK/AAAAAAAAAAAAAAAAAAAAAJfnkYVUs37vmG1jFWsBchS1riAsEgmi4QWcUlNrs5gy/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=BAQyF8%2BCvmuMoyyE9CRlgsT42as%3D)

벡터의 크기는 아래처럼 구하면 된다.

![](https://blog.kakaocdn.net/dna/STz9N/btsPE5pU8o3/AAAAAAAAAAAAAAAAAAAAALhUzUbrOM-1AB9EGtSgNbAZb6E5bvK6LWCRwH90rnHi/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1AnmLlwadJs0KSVg%2FO6SQoafPAE%3D)

![](https://blog.kakaocdn.net/dna/ztY44/btsPDsT4khS/AAAAAAAAAAAAAAAAAAAAAAqdUX8tABl5cRw4xsLdLB01LJX99tss-bemRh2aju_j/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=53Yv1KsRKWLZEsji81Wadx%2FpHPw%3D)

위의 식을 사용한 것이데, 위의 식이 이해가 안되면 이전 포스팅을 보고 오는 것을 추천한다.<https://tithingbygame.tistory.com/245>

[[PhysicsForGameDeveloper] 등가속운동

이번 장에서는 운동학(kinematics)의 핵심 개념들을 설명합니다.구체적으로는 선형 및 각 변위(linear and angular displacement), 속도(velocity), 가속도(acceleration)에 대해 다룹니다. Introduction운동학은 물체에

tithingbygame.tistory.com](https://tithingbygame.tistory.com/245)

## 

## **목표 지점에서의 수직 낙하 거리 계산**

총알이 목표 지점에 도달했을 때의 y방향 낙하 거리(수직으로 떨어진다)를 구하려면  
먼저 도달 시간 t\_hit​을 구하고, 그 시간을 y식에 대입한다

x\_hit = v\_hit \* t\_hit을 사용하면 아래의 식을 얻는다. (n: 총구 ~ 타겟 까지 거리)

![](https://blog.kakaocdn.net/dna/xkXHp/btsPEwnZier/AAAAAAAAAAAAAAAAAAAAAE1aesRzQJTaAuXH2K7gR6aFnUvIFuud71Le0KB5pnNE/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Cny13PmJ%2BzBBuoBCZGSE2Tnf8Lw%3D)

d는 총알이 타겟에 도착했을 때 떨어진 거리이다.

y방향의 속도는 없고, 중력 가속도만 존재하니

d = -1/2 \* g \* t\_hit^2 으로 구할 수 있다.

![](https://blog.kakaocdn.net/dna/v61S9/btsPESRN6Kj/AAAAAAAAAAAAAAAAAAAAALuqLw1hD14_YXWOVF1mgwzsfoGFi4POJKxkRCbSGRXk/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=JEPgMsOCZjzNsQnDHdnFZ9N%2BOXg%3D)

n이 500m이고, 총알의 속도가 800m/s라면,

t\_hit 은 500 / 800 이므로, 0.625초이고,

t\_hit 을 d 식에 대입하면 -1.9m를 얻을 수 있다.