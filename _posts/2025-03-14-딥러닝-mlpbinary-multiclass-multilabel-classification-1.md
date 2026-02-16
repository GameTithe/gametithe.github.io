---
title: "[딥러닝] MLP(Binary, Multiclass, Multilabel Classification) - 1"
date: 2025-03-14
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **Classification**

**Binary Classification: 강아지가 있는 지 없는지 (0 or 1)**

Multicalss Classification: 여러개의 옵션 중 1개를 선택

Multilabel Classification: 여러개가 동시에 있을 수 있음

![](https://blog.kakaocdn.net/dna/dihbkV/btsMJdSpwsx/AAAAAAAAAAAAAAAAAAAAAC9SrIGiswuIsRvNNJPKK-V2IIC1w4NP6cJTeUlzv0Xr/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=TApkSMBjEmjyjkRrp4DyP9lA3ps%3D)![](https://blog.kakaocdn.net/dna/d8gHrr/btsMJrv56SD/AAAAAAAAAAAAAAAAAAAAANeMqUCRQxxBH3nObFvqT1jbN8fFCH5GH8fqTy4fUG0B/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=cP50zYDv8Ynx61K3DwOpLqsCyo8%3D)![](https://blog.kakaocdn.net/dna/bVQ3tT/btsMJbAiwJk/AAAAAAAAAAAAAAAAAAAAAKF7cYvCYcXN7LG-ivri-IUPg_K6LXopcT9uRWTMZ0Wb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Vu4gCeFYaPagZneEqhrIA8WLhec%3D)

### **Perceptron**

![](https://blog.kakaocdn.net/dna/debuAM/btsMIDcXy0I/AAAAAAAAAAAAAAAAAAAAABKdMAJS1z6ilnTga_H9UrOpUhZbSHqbDbXdmXmqsq9J/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=92MomdXHG43ARmT4q72lcCGJq%2Bg%3D)

f = activation function (step function: 0보다 크면 1로 or  0을 ouput으로)

**f ( Σ (pixel의 rgb \* 가중치) )**

Perceptron은 잘 쓰이지 않는다. 현대 인공지능에서 중요한 것은 미분이 가능해야되는데   
Perceptron은 미분이 불가능하기 때문이다.

### 

### **MLP란**

**Perceptron을 여러겹 쌓은 것이다. Multi Layer Perceptron...!**  
Perceptron 안쓴다면서요...  
Perceptron을 단일로 사용하지 않고

**Perceptron의 activation function을 미분 가능한 비선형 activation function으로 바꿔주고, 여러겹을 쌓아서 사용하고 있다.**

여기서 왜 비선형으로 하나요? 라고 의문이 생길 수 있다. (더보기)

더보기

만약 선형 변환이라고 생각해보자

3개의 레이어를 x1이 지났다고 가정하면 다음과 같이 표현할 수 있을 것이다. =>w 1\* w2\* w3 \* x1

근데 이게 선형이라면 w 1\* w2\* w3 \* x1   == w3 \* w2 \* w1 \* x1 이다.

layer의 순서가 중요하지 않게 되고, 사실 1개의 layer를 통과한 것으로 가정된다. 그렇기 때문에 비선형으로 변환이 되어야한다.

## **Binary Classification**

Binary Classification를 위한 모델인 Logistic Regression에 대해 알아보자.

### **Logistic Regression**

선형 모델의 출력을 비선형으로 변환하기위해서  sigmoid함수( σ )를 등장 시킴 (선형으로 했을 때 outlier에 민감해질 수 있기에 sigmoid 사용)

여기서 모델이 선형이라면

좌측은 시그모이드, 우측은 선형일 때 outlier의 민감성을 나타낸다.

![](https://blog.kakaocdn.net/dna/TNIBf/btsMMfvFFM0/AAAAAAAAAAAAAAAAAAAAAFTdgg83heeZRwrSZnYiXFW7CgagkNmHg7nU2caVIASc/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=2g8RL1YGm%2FgICn4ppqTQyp%2F%2B%2F2E%3D)![](https://blog.kakaocdn.net/dna/3gF45/btsMJIYFuth/AAAAAAAAAAAAAAAAAAAAAAjNhC8eg3ZDGZB7EEyxcHORLvE9rbd2PYmC5HatNDIl/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=e45Q9WKc467RZatfT%2FezGP9k7%2FI%3D)

**Threshold p** 를 기준으로  f() > p 일 때 1, 그 외에는 0

sigmoid 함수의 xw^T를 **logit**이라고한다.

**sigmoid가 0.5가 되는 선이 decision boundary**이다.

### **Loss Function**

**Binary Cross Entropy**

![](https://blog.kakaocdn.net/dna/cXdEZP/btsMHS2Z75r/AAAAAAAAAAAAAAAAAAAAAPLUBruBFwK281uZs4BHBsHJTF82A9Bw3GvOJpT0P_M5/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=7N7Gmj10sK%2BenxGnyaw0Gaq%2BiKw%3D)

```
  loss = y_true*np.log(y_pred) + (1-y_true)*np.log(1-y_pred)
  loss = -loss.mean()
```

이 부분만 따로 보자 (맨 앞에 -가 있다)

![](https://blog.kakaocdn.net/dna/1d7yM/btsMKa2dIiv/AAAAAAAAAAAAAAAAAAAAAKhNtLp_NxxEN0eunR5dR3bWFgUgKb4QvgYISq1Lm0ZW/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wUO%2BKTt2kDjlQ8a22%2FIXBHCXZvQ%3D)

![](https://blog.kakaocdn.net/dna/cqCGCk/btsMKqcG7Xg/AAAAAAAAAAAAAAAAAAAAAPCxrIw6NUEPVL75gtKJ83ajOAKIBzgdoaNyG9npJ7AS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=TEsKKBOrjgphAN%2FOQQFUDQkq%2Fiw%3D)

y(j) == 0일 때, -log(y^(j))이 된다.

loss가 최소가 되게 하려면, 값이  minimum이 되어야 하고, log(y^(j)가 최대가 되어야 한다. ( -가 있으니)

그러니 모델이 **y(j) = 0** 이면 **y^(j)** 도 0으로 **예측해야 Loss가 최소가 된다**.

y(j) == 1일 때,  -log(1 - y^(j))가 

loss가 최소가 되게 하려면, 값이  minimum이 되어야 하고, log( 1 - y^(j))가 최대가 되어야 한다. ( -가 있으니)

그러니 모델이 **y(j) = 1** 이면 **y^(j)** 도 1로  **예측해야 Loss가 최소가 된다.**

Sigmoid 함수 + BCE 를 사용하면 Convex(볼록한) 형태가 되는데, 그럼 global minimum이 존재하게 된다.

여기에 gradient descent 방법을 사용하면 global minimum에 수렴할 수 있다.

**BCE 손실 함수의 gradient (미분값)** 를 통해 **weight 업데이트하면 아래와 같이 된다.**

![](https://blog.kakaocdn.net/dna/bqcQiD/btsMJL9rimM/AAAAAAAAAAAAAAAAAAAAAALc6d3I2rVPFnafCAC3uf43awrq-PZZA-wIRSuJV2_N/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=A3%2Ftg8Lbtwjl0asrg4NOul%2Bdq5k%3D)

**그다음은 Multicalss Classification이다.**

**Multicalss Classification 중 대표적인 방법인 Softamx Regression(Multinomial Logistic Regression)에 대해 설명하겠다.**

**Multicalss Classification**

사전에 정의된 개, 식물, 고양이, 사과 등 집합들 중에서 하나를 분류(선택)하는 것 ( index값으로 변환된다).

**one-hot Encoding**

![](https://blog.kakaocdn.net/dna/OmKrn/btsMKS7731e/AAAAAAAAAAAAAAAAAAAAALTWDnw-HDuXpB0XdMB9XNIgKMo9mr-u6FmMHHc8IWRv/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=FgtS%2Bdd9rD857ZOMxA2O3LUTuDQ%3D)

인덱스에 해당하는 bit가 1이된다.

**activation function은 softmax를 사용한다.**

![](https://blog.kakaocdn.net/dna/JVHrs/btsMI3wKg8I/AAAAAAAAAAAAAAAAAAAAAAYDQfwPRbYNqmkcDSXBzveuPnPDDY9uJQlsiHcgm8v6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=mCV1DjesiBENyhnphsSKTb%2FIb0M%3D)

개, 식물, 고양이, 사과 분류 리스트에 있을 때, 각각의 확률을 모두 더하면 1이다.

각각의 확률 p를 예측하기 위해서  z= x \* w^T를 생성하고, softmax activation을 통해서 normalize를 한다.

최족 예측은 softmax까지 적용시킨 output에서 제일 값이 큰 index이다.

### **Cost Function**

**Categorical Cross Entropty:** BCE(bindary cross entropy)를 일단화 시킨 형태이다.

![](https://blog.kakaocdn.net/dna/K8AkL/btsMJctw2Jw/AAAAAAAAAAAAAAAAAAAAAABbL55T9yzyj8fONDcTK7pegRTzABCjEPPwhd-Wlhv_/img.jpg?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Z8MSI00KR%2FILmXXqEaT3b0aREqg%3D)

**output = (1, 0, 0, 0)**

만약 y0가 1이라면, 나마지는 0일 것이고,

위의 식에 대입해보면  -log(y0^)이니, 이것만 loss로 계산을 해주면 된다.

gradient descent

동일..

**linear한 dicision boundary를 동시에 학습하기 위해서 softmax regression을 사용하는 것이다.**

![](https://blog.kakaocdn.net/dna/skwaS/btsMI3wKGiX/AAAAAAAAAAAAAAAAAAAAAAKLuOvTLZabzmKUJbGhN0M0CLAZ2wvSw_bsx-nfSXJj/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=sYI%2B0KTk5Tr7W5539qlPh%2BOckEE%3D)

## **Multilabel**

여기서는 **Binary Relevance model**을 알아볼 것이다.

하나의 입력에 class label이 동시에 존재하는 것

위에서는 ouput이 (1, 0, 0 ,0) 과 같이 정답이 하나였는데, 이제는 (1, 1, 0, 0)도 가능하다는 것이다.

multilabel에서는 확률의 합이 1이 될 필요가 없다. 서로 서로가 독립적이기 때문에

그렇기 때문에 logistic regression을 k번하는 것과 같다.  (class가 k개 일 때)

![](https://blog.kakaocdn.net/dna/TGYVC/btsMJ1Skl9o/AAAAAAAAAAAAAAAAAAAAALFqoXayAUB-AoGgI9N7O8vKHZ1BUentz0KnrTi8CZTu/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=8eM6ED5FzXjdJ1Y7QAWIuj%2FtIyc%3D)

**전체적으로 Softmax Regression과 동일한데, activation function이 Softmax에서 Sigmoid로 바뀌고, Cost Function은 CCE에서 BCE로 바뀐다.**

![](https://blog.kakaocdn.net/dna/bJIYCO/btsMJmo5JSe/AAAAAAAAAAAAAAAAAAAAAAZgM9vECT9aTztbgoGqnUitCSTI9oQ4-VJohPm0bPc8/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=gaqbsQGbHbmpQ31e8KXJuUpd%2F1o%3D)