---
title: "[CG] 물 시뮬레이션 with SPH ( VPython을 곁들인.. )"
date: 2025-02-19
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

**유체의 움직임으로는 크게 3가지로 볼 수 있습니다.**

**분산(diffuse)**

다른 외력이 작용하지 않아도 유체의 밀도가 높은 곳에서 낮은 곳으로 유체가 퍼저나가는 것

**대류(advection)**

중력, 부력 등 외력의 작용으로 유체에 흐름이 생기는 것

**점성(viscosity)**

유체 분자가 서로 붙어있으려는 성질

SPH기법으로 물을 시뮬레이션 해볼겁니다. 차례대로 따라가면 어렵지 않을 겁니다...!

코드는 깃에 올려놨습니다 :)

<https://github.com/GameTithe/SPH-Vpython>

## **SPH(Smoothed Particle Hydrodynamics)**

물과 같은 유체를 묘사할 때 분자 개수만큼 입자로 표현하면 컴퓨터가 감당할 수 없을 정도로 연산량이 많아지기 때문에 그 범위를 설정해줘야 된다.

**As의 물리량에 대한 식:**

mj / pj : j 번째 입자의 부피

Aj: j번째 입자의 물리량

W: 커널 함수(두 입자의 거리, 반지름)

 

스칼라량 A는 위치 r에 대해서 모든 파티클의 가중합에 의해 보간됨

그림과... 같이.. 입자가 겹쳐지게 되면 겹쳐진 영역의 양만큼 물리량은 더해진다. 

![](https://blog.kakaocdn.net/dna/XTNeD/btsMojltKUc/AAAAAAAAAAAAAAAAAAAAAOBmUX0umAdNgkcZHEt1_k6T2rwpzZ24kuYiP2nKppmi/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=zVjgxk75rf6JuATtnd3pvgw4Tjo%3D)![](https://blog.kakaocdn.net/dna/cUX2ZZ/btsMomCw88L/AAAAAAAAAAAAAAAAAAAAAARmAJoaH9TID50ivmUOMIXZwW-zjXstG9-qGoTIxD1v/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=cnyH9B5WNbvkwv1C2WhqnXDgnHo%3D)

커널은 부피가 1이다.

![](https://blog.kakaocdn.net/dna/bJbYYc/btsMpKWskCl/AAAAAAAAAAAAAAAAAAAAAAyOLv58mt78VPeT5gpnyAOFn4aMJlL9daHdQa5fDeF_/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=PxBvoxwphV0OGOLNZ3l0PnqYm8Q%3D)

파티클의 질량과 밀도가 나타나는 이유는 각 j번째 파티클이 특정 부피 Vi = mi/ρi를 갖기 때문이다.

시뮬레이션 내내 질량 mi는 상수이고, 우리의 시뮬레이션의 경우 모든 파티클의 같은 질량을 갖겠지만,

**밀도 ρ****i****는 매 시간 단계마다 계산해줘야된다.**

위 식을 미분하면 커널 W에만 영향을 미친다. (r에 대한 미분이기 때문에)

**첫 번째식은** 물리량 A에 대한 공간 기울기 값이다. (그래디언트, Gradient)

**두 번째식은** 공간에서 두번 미분한 값이다.( 라플라시안, Laplacian)

![](https://blog.kakaocdn.net/dna/Hx76o/btsMn8EunEj/AAAAAAAAAAAAAAAAAAAAADnKDjDdywyRGu9uczXqeZSHfr_HTdyvFobnFOXYARjx/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=IJv14E9UJoJpt1eOCDLWUW3A5Os%3D)![](https://blog.kakaocdn.net/dna/sOFzq/btsMpoTFyDO/AAAAAAAAAAAAAAAAAAAAAKdqv04JyKJv2223u78wrRuR1us6UI0rXefc-1TNpEtn/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=UfEWIGxyTUcXC7mDWq7o9%2BLooWU%3D)

SPH의 안정성, 정확성, 속도는 어떤 커널을 사용하느냐에 다렸다고 한다.

일반적으로 미분 없이 물리량을 구할 때는 2차의 정확도를 지닌 아래의 커널을 사용한다.

poly6 커널은 커널 x = 0 일 때, 미분 값이 0이 되어 gradient 값을 구할 수 없다.

gradient를 적용할 때는 spiky 커널을 사용한다.

![](https://blog.kakaocdn.net/dna/bV7wB0/btsMoYgSuU6/AAAAAAAAAAAAAAAAAAAAAOLtqLmNV-XjQve7sEESVU_ZfMIuBfvH-ovP_qLMzLI8/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=89fkdmV5KM33TPqH7hguWT14R6M%3D)![](https://blog.kakaocdn.net/dna/bW5q4B/btsMoXPJsUb/AAAAAAAAAAAAAAAAAAAAAMDHUZxBg7JpKwVvkNix2m4xKeJ216osJgfDHn_C66H-/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=mGspk54SotiJ5bElu3yXyJY%2FcJo%3D)



![](https://blog.kakaocdn.net/dna/d5i8FK/btsMol4GOnW/AAAAAAAAAAAAAAAAAAAAAOsBmiWFbeHWPFBvKjKZL1dK9fjQjzcaCkPcqysrdza2/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=6Kj0TvyMXnXcamR6JIi3zVV1PPw%3D)![](https://blog.kakaocdn.net/dna/bnxcYY/btsMoYgSuVz/AAAAAAAAAAAAAAAAAAAAABFF9vLixtkrLBddP0gK7_BGNH3TER0DTJY3jaA18XB5/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=2hShgvY1lt2u%2Bb8kWEsPYwJ8i2Y%3D)

아래의 커널은 Laplacian 연산할 때 사용된다.

![](https://blog.kakaocdn.net/dna/benUNd/btsMnrrd5qQ/AAAAAAAAAAAAAAAAAAAAAElkKjrnGQLszwCLWyDEKP50r7ZzjS-qs_n87jPTZg5t/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=UObACIPnt%2FWiS67anUchWCLafqk%3D)![](https://blog.kakaocdn.net/dna/weTwC/btsMolp3RUp/AAAAAAAAAAAAAAAAAAAAAHhqxVl_OWWoE8SO2aRZu57uxznEs7v_m8cfPsb3h1S9/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=yMLYqjhwQOhi845GGnBtb3jLowE%3D)

### 

### **SPH를 위한 유체 지배 방정식**

t시간에 따라 움직이는 Navier-Stokes 방정식은 아래와 같다.

![](https://blog.kakaocdn.net/dna/DkSWn/btsMnQ49SAC/AAAAAAAAAAAAAAAAAAAAAHb11qOIsGyW-g-vfmgEaUOALxkOSp22i9DJOHafg8UH/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2Bo%2B1KuJtMCO%2Fr8uRodZsUunam%2B0%3D)
![](https://blog.kakaocdn.net/dna/uO3vz/btsMnqMClpK/AAAAAAAAAAAAAAAAAAAAANJ0FU8j7uehm4yn5CTprX9H8LXH_eJJhDR1U2z8y49m/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=S2c%2FWvyN5TbnpxFgzGKWIKHZz%2BI%3D)

### **SPH 물리량과 힘의 계산**

밀도는 각 입자가 가지고 있는 고유의 속성으로 SPH커널이 겹쳐진 부분을 계산하여 정한다.

우측 식을 통해서 밀도를 구해보자.

좌측 식이 도출된다. 결과적으로는 **밀도 = 질량 X 커널** 이다.

![](https://blog.kakaocdn.net/dna/bAYviV/btsMnswSFey/AAAAAAAAAAAAAAAAAAAAAKgbPe-vXDecuvFKzW_DsxPdbBm5vVfrDqyT5kpTSZhF/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=otaprdVNcHVJ04kp5gdOr%2FiGm9g%3D)![](https://blog.kakaocdn.net/dna/dbkpK3/btsMo75EzhJ/AAAAAAAAAAAAAAAAAAAAAHX7Po5hExH8iXxvmMbfWXQcAW1xacfh_-sQEE505YFJ/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xEbtJ5TtkUmrJM5cIPHeXZ2yqoA%3D)

### **압력에 의해 SPH입자에 작용하는 힘**

물리량에 대한 식을 다시한번 사용해서 압력을 구할 수 있다.

그림과 같이 좌측에서는 압력에 의한 변화가 없을 것이다.

가운데에서는 밀도가 낮으니 당기는 힘이 생길 것이고,

우측에서는 밀도가 높으니 밀어내는 힘이 생길 것이다.

![](https://blog.kakaocdn.net/dna/7O3R8/btsMoW4o76H/AAAAAAAAAAAAAAAAAAAAAJKvGJTCLKtUTEbVE1njYfyLxj5Os4rdRGNuAMCfOZh6/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=BIlru3Zh%2Bz4wYaYsjWrifj2EWfY%3D)

입자 하나에 주변 압력도 영향을 끼치기 때문에 본인의 압력만으로 압력 값을 계산할 수는 없다.

![](https://blog.kakaocdn.net/dna/bAYviV/btsMnswSFey/AAAAAAAAAAAAAAAAAAAAAKgbPe-vXDecuvFKzW_DsxPdbBm5vVfrDqyT5kpTSZhF/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=otaprdVNcHVJ04kp5gdOr%2FiGm9g%3D)![](https://blog.kakaocdn.net/dna/QlDWO/btsMn601qZs/AAAAAAAAAAAAAAAAAAAAAOyHtA5ftEVjjSYu3fuldnoPvrOMsFUOjtCrUr66WZyP/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1rLiT%2Bd%2F5fizeUCBSxZdTOwLKLU%3D)

이웃한 입자들의 압력 또한 고려하기 위해

본인의 압력이 아닌 이웃한 압력과의 평균을 구해서 사용한다.

![](https://blog.kakaocdn.net/dna/eqz38n/btsMpJpHn9X/AAAAAAAAAAAAAAAAAAAAAC05QUmPql6iM4SItkuk5mkVCkpiCprNPyj15GFflTCf/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=M1GUcF9E5IYgc1AtcZL1qdcpzTk%3D)

입자는 물리량(질량), 위치, 속력을 갖기 떄문에 특정 위치에서의 **압력을 우선적으로 계산**해야된다.

아래 식을 통해서 **밀도를 구하고,**

![](https://blog.kakaocdn.net/dna/cbAkFM/btsMpKa5dSg/AAAAAAAAAAAAAAAAAAAAAA5OE0JLBm0VuqVilHGh5fRr9SFtuNkvs4LyMtED72Vp/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=A0OaJ7RV8vbA6Bcnsl2wuBilNUY%3D)

```
 rSum += particles[j].mass * poly6Kernel(rdistance, m_kernel_h)
```

압력을 **이상기체방정식인 압력과 밀도 관계식**으로 구할 수 있다. p0은 유체의 기본 밀도로 정한다.

만약 유체가 기준 밀도 ρ0에 있을 경우 불필요하게 압력을 받지 않게 하기 위해서 -p0을 해준다.

여가서 k값이 커지면 유체가 조금만 모여도 압력이 커지기 때문에 시뮬레이션이 불안정해질 수 있다. 그렇다고 k를 너무 작게하면 시뮬레이션은 안정적이지만 유체가 압축되어진 것 처럼 보이게 된다.

![](https://blog.kakaocdn.net/dna/mMKJw/btsMolXUePk/AAAAAAAAAAAAAAAAAAAAANvLVMxHKdCZgynGw1D6-rzFIdH7sZ-R37uHvr02ZKJo/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=8F3GROqgTyvz2E4NRXzz98MVhzk%3D)

### **점성에 의해 SPH 입자에 작용하는 힘**

점성은 입자가 움직일 때 주변 입자의 속도의 차이 때문에 발생한다. 즉, 주변 입자와 속도가 같아지려는 현상으로 해석할 수 있다.

점성도 물리량 식을 사용해서 구할 수 있다

![](https://blog.kakaocdn.net/dna/vuNWp/btsMnPd4ONl/AAAAAAAAAAAAAAAAAAAAALj5xYAKfHDBkNippQOPpfFQNWltT_BD-OmN1z4xtbqw/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=rNsQyqn5qBTCAcQv7iD0V2nJoB0%3D)

하지만 압력과 비슷한 이유로 점성도 또한 주변 입자의 값을 사용해준다.

![](https://blog.kakaocdn.net/dna/cYQe0l/btsMpoTFyD5/AAAAAAAAAAAAAAAAAAAAAMOpyu0-9Y1MmivIyu92G9kiIKisRXxj9RDVZ9YnVjv-/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=vrlffRRJNJlJjlc8M1V8Kn1Bg%2B4%3D)

### **SPH 입자에 작용하는 그 밖의 힘**

SPH입자에 작용하는 그 밖의 힘으로는 중력과 충돌이 있는데, 여기에는 커널을 사용하지 않고 입자에 직접 적용시키면 된다!