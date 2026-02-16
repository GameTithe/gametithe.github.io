---
title: "[딥러닝]CNN_Regularization(3)"
date: 2025-03-17
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **Regularization**

모델의 complexity를 줄이지 않고, generalization erro를 줄이는 방법이다.

![](https://blog.kakaocdn.net/dna/0WpO3/btsMM3oks7J/AAAAAAAAAAAAAAAAAAAAAHCxOSMa6sVWLxPmr1l2DWiWT8sQ8-LfcwMcur77vaiE/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=yEK7qrcbyTCohd3XXx0V%2Bkw6B3g%3D)

모델의 layer수가 늘어나면 Complexity가 증가하고, Variance가 증가한다.

그럼 그래프에 따라서 over fitting이 일어난다.

**이를 regularization을 통해 complexity는 유지하면서**

**variance를 줄이고, bias를 늘려(bias-variance tradeoff) over fitting 문제를 해결하자**

### **Dropout**

**학습 중에 임의의 노드의 출력값을 랜덤하게 0으로 만드는 기법**.  ( AlexNet에서 도입됐다. )

확률 p로 설정을 해놓으면 p확률로 0을 갖게된다.

![](https://blog.kakaocdn.net/dna/cP6LQp/btsMM3Po590/AAAAAAAAAAAAAAAAAAAAAMRSJvPzOsysCMv9coZ_qRjlcrvlfR9DJjj49wrsup_7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=e15ohONnHhi3MiLMLVBYWohzs7Y%3D)

과도한 학습을 막아서 overfitting을 효과적으로 방지해준다. 다양성을 가져온다는...

학습시에만 적용이 되고, 추론/평가 시에는 적용하지 않는다.

 => 당연하지, parameter를 반밖에 못쓰게 되는거니까..

**학습 때**는 일부 노드가 랜덤하게 **0**이 되므로, **전체 출력값의 평균과 분산이 줄어든 상태**에서 학습된다.

**하지만 추론/평가 시**에는 **모든 노드가 살아 있으니** **학습 때보다 출력값이 커질 수 있다.**

즉, **보정(rescale)이 필요하다. (학습할 때 적용시켜주면 된다)**

1) test time scaling(standard dropout): y = y \*(1 - p) 

2. training time scaling(inverted dropout):y = y \* ( 1/  (1 - p) )

=> p가 0.5일 때 다시 1로 만들어서 internal convariate shift 문제를 고려한 것을 깨뜨리지 않는다. 

training time scaling이 많이 사용된다.

### **DropPath (Stochastic Depth)**

Dropout을 unit이 아닌 layer에 적용시키는 것이다.

(layer를 확률적으로 비활성화 하는 방법)

**Drop Path 또한 학습 시에만 활성화하고, rescaling을 해줘야된다.**

**=> training time scaling(inverted dropout)을 사용한다.**

layer를 비활성화 시키면 해당 batch에서 학습을 할 수가 없다. (gradient가 0이 되기 떄문에)

이를 예방하기 위해서는 **Residual Connection을 추가해줘야된다**. ( 이전 output을 사용하는 방법 )

이를 통해 layer들을 다양하게 학습시킬 수 있다.

### **Data Augmentation**

데이터에 적절한 변화를 줘서 추가적

인 데이터를 자동 생성하는 방법이다.

over fitting을 해결하기 위해서 학습 데이터 셋의 크기를 늘리면 되지만, 그에 따른 비용이 발생한다.

이를 우회해서 해결하고자

아래처럼 데이터를 회전, 색변형, 데이터에 노이즈 추가 등을 통해서 추가적인 데이터 셋을 만들어서 학습시킨다.  
(회전을 해도 고양이, 색이 변해도 고양이니까..)

![](https://blog.kakaocdn.net/dna/bOBS0b/btsMNecgQJN/AAAAAAAAAAAAAAAAAAAAAOxan7soHZMkuXRbDQCPc1LySmFnxg3tC1-rKSnpWCGA/img.jpg?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=39dReG7L4wNSpsCpjp2%2BONNRA7Y%3D)![](https://blog.kakaocdn.net/dna/DYebS/btsMNJ3VNg0/AAAAAAAAAAAAAAAAAAAAAArtG1sI9g6o8vxtMazmW_7Z5xnCVxR37-h003hVROfF/img.jpg?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=n7Eb7tL9N3B1JICPDbsclq62blU%3D)

### **Mixup(Data Augmentataion)**

두 개의 데이터 포인트와 그에 대한 레이블을 **선형적으로 섞어서 새로운 데이터 포인트를 생성**하는 방식이다.  
즉, 단순히 원본 데이터를 조금 변형시키는 게 아니라 **완전히 새로운 데이터를 만들어내는 방식**이야.

![](https://blog.kakaocdn.net/dna/cPMsph/btsMLYIlI45/AAAAAAAAAAAAAAAAAAAAAIH5pvX-S-amvyT3DpUTK3_CFLERehelSTkmtJXtgD1u/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=yc6BmuLa9RZc66NakOW23IufLas%3D)
![](https://blog.kakaocdn.net/dna/no7J1/btsMLZAyD8T/AAAAAAAAAAAAAAAAAAAAAEnkmTV5KreZUheWcZ4Z1t_nOiC90ohzTUUSWFtV8r14/img.jpg?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=G9aHXLyPjlAv2E%2F0cNyD1DnnjUY%3D)

**입력 데이터**뿐만 아니라 **레이블**도 섞는 것이 특징이다.

예를 들어, 개(1)와 고양이(0) 이미지를 0.7 : 0.3 비율로 섞으면,

새로운 데이터는 **개와 고양이의 합성 이미지**가 되고, 레이블은 0.7 (개) + 0.3 (고양이)로 표현된다.

=>모델이 출력해야 하는 정답(label)이 one-hot vector가 아니라 **비율로 섞인 라벨**이 되는 것이다.

### **Label Smoothing**

Label Smoothing은 **모델이 지나치게 확신(과잉확신, Overconfidence)** 하면서 학습하는 것을 방지하기 위해 **label(정답)을 부드럽게 만드는 (smoothing) 기법**이다.

**분류 문제**에서 사용되는 **One-hot vector** 형태로 예로 들어보겠다.  
예를 들어, 4개의 클래스가 있고, 정답이 인덱스 1이라면 레이블은 아래와 같이 생길 것이다.

Original label=[0,1,0,0]

하지만 **Label Smoothing**을 적용하면 **1 대신 0.9**, **0 대신 0.0333 (혹은 다른 작은 값)** 처럼 **부드럽게 변형된 라벨**로 학습하는 것이다.

Smoothed label=[0.0333,0.9,0.0333,0.0333]

(위 숫자는 예시일 뿐이고, 보통은 smoothing 값 ε(입실론)으로 조절

 softmax function이 적용된 상태라면

0을 학습 하기 위해서  -∞로, 1을 학습하게 위해서 +∞로 logit이 학습될 것이기 이를 방지하는 것이다.)

![](https://blog.kakaocdn.net/dna/sg7mo/btsMMpyK2Zm/AAAAAAAAAAAAAAAAAAAAANQCKQqO6E-TpAvojYfyczxWXYw_Weo2IXQu77HlPwk-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=g2cx0LWwKUPjIp0wpkiJ%2B%2F3GtNI%3D)

![](https://blog.kakaocdn.net/dna/zTXuf/btsMLvGx3nl/AAAAAAAAAAAAAAAAAAAAANell8LU0xDALzpj4H05d8hvfW_8RM9gUYnKS6PZwfN3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3KgZS4ce8MJ1pqzFfTb5m6Nkitg%3D)

yk​: 원본 라벨(one-hot vector)

K: 클래스 개수

ε: smoothing factor (예: 0.1)

**위에서 여러가지 Regularization 방법을 배웠는데**

**어떤 모델을 어느 강도로 사용하냐에 따라 성능이 좋아질 수도, 악화될 수도 있다.**

**Validation Loss가 적고, Metric을 향상시키는 Regularization을 잘 찾아서 사용하자**