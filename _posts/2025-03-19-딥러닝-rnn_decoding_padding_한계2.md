---
title: "[딥러닝] RNN_decoding_padding_한계(2)"
date: 2025-03-19
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

Auto Regressive: **이전까지의 출력을 기반으로 다음 출력을 순차적으로 예측하는 방식**입니다.

여기서 사용되는 Decoding 방법을 설명하겠다.

### **Greedy Decoding / BeamSearch Decoding**

**Greedy**

**가장 확률이 높은 단어를 즉시 선택**하는 방식이다.

간단하지만, 최적의 문장을 찾지 못할 가능성이 높다.

**BeamSearch**

전체 문장의 확률을 누적해서 현재 가장 확률이 높은 단어 선택 및 문장k개(beam width)를 유지한다.

당장의 확률만으로는 최적의 문장을 완성하지 못하므로 확률이 높은 문장 k개를 유지하는 방법이다.

최적의 답을 찾기에는 유용하지만, 연산량이 높다.

![](https://blog.kakaocdn.net/dna/blDSt2/btsMOfKFE96/AAAAAAAAAAAAAAAAAAAAAOSCDCW-nR1SmHa7TdO4_qD98u-UYblZxuPneIyNtDx7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=VNiL0r7fQ7vKC3tk4FPzCjpo%2BB0%3D)

### **Sampling Based(Non-deterministic)**

확률적으로 다음 단어를 선택하기에 실행할 때마다 출력이 바뀐다.

0.4 확률로 dog, 0.5 확률로 nice, 0.1확률로 car를 선택하는 것이다.

이러면 확률이 매우 낮은 단어도 선택될 수 있으니, Top-k, Top-p로 보완을 한다.

**Top-k**: 상위 k개의 단어만 선택

**Top-p**: 상위 후보의 확률 누적합이 p일 때 까지의  단어만 사용

![](https://blog.kakaocdn.net/dna/c5UP1j/btsMPos3VDD/AAAAAAAAAAAAAAAAAAAAALUZGzqxMQT-YE5INQUfrVQS1hhCJ9S2NwQsZKbQ-zVn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=VEGb%2Fx2%2BWGbsHITODu8EyYjOXIU%3D)

### 

batch 내의 sample들의 shape이 다를 수 있다.  하지만 GPU에게 일을 시키려면 shape을 맞춰줘야 한다.

그 작업이 padding이다.

(descrete 한 데이터(text와 같은)에는 연속적이지 않기 때문에 resize가 어렵기 때문에 padding을 해줘야 한다.)

**Padding**

가장 긴 길이를 기준으로, 짧은 곳에 pad token을 추가해서 ( 주로 0 ) token의 shape을 맞춰준다.

**문제점:**

가장 긴 곳을 기준으로 잡으면 학습 효율성이 떨어진다.

특별한 정보가 없는 token이 불필요하게 추가된다.

입력 길이를 고정하지 않으면 train test time inconsistency가 발생한다. (학습 때 padding을 추가했지만, 추론 때 padding이 없으면 잘못된 output을 출력하는 경우, masking 필요)

**Masking**

pad token은 gradient에 관여하지 않게 한다.

ex: RNN: pad일 때 hidden layer 업데이트 X, Conv일 때 kernel 값을 0으로

pad는 loss 계산에서 제외시킨다.

Masking을 구현하면

padding에 의한 train-test time inconsistency에 제약받지 않고, variable-shape input에 대한 처리가 가능하다.

(학습할 때 padding하는 )

RNN의 한계점:

1.time complexity: O(L)이어야 한다. 이전 time step의 영향을 받기 때문에 병렬화가 어렵다.

2. long-term memory문제: x1 ~ xt 까지의 정보를 고정된 크기 h에 저장해야되므로, 후반에는 정보를 버리게됨

3. Vanishing Gradient문제: LSTM, GRU, Layernomalization등으로 부분적으로 해결 가능 but 근복적 해결 X

위의 이유들로 CNN의 ResNet같이 layer를 늘려서 성능이 크게 증가하는 발전을 이루지 못함