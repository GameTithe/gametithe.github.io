---
title: "[GameEngineArchitecture] Data, Code and Memory Layout(1)"
date: 2025-07-25
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

숫자는 게임 엔진 개발의 중심에 있습니다.

모든 소프트웨어 엔지니어는 숫자가 컴퓨터에 의해 어떻게 표현되고 저장되는지를 이해해야 합니다.

이 절에서는 책의 나머지 내용을 위해 필요한 기초 개념을 설명하겠습니다.

### **Numberic Bases**

사람들은 일반적으로 **10진법으로 생각을 합니다.**

오른쪽에서 왼쪽으로 갈수록 자릿수는 10의 거듭제곱을 나타낸다. 숫자 7803은 다음과 같다.

![](https://blog.kakaocdn.net/dna/UZFph/btsPxCgQKgX/AAAAAAAAAAAAAAAAAAAAABash_mbOF2Ww93u4bc2hapV_LIzPVBJwemLI7eECfqx/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9KWS4P1fmvNT8o%2BIklbi5xJ%2FbXY%3D)![](https://blog.kakaocdn.net/dna/HgIsv/btsPwW7XWyl/AAAAAAAAAAAAAAAAAAAAAKeNbSYa5zaID6yV_-XRGrGOdfU0GG7MCFYhGodh4mo3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fRJvJYDqQ0FIzE7MsMhe8LKAh7E%3D)

컴퓨터 과학에서는 정수 및 실수와 같은 값을 컴퓨터의 메모리에 저장해야 합니다.

그리고 우리가 알다시피, 컴퓨터는 숫자를 이진법으로 저장합니다. (0과 1의 두 숫자만을 사용한다는 의미)

오른쪽에서 왼쪽으로 갈수록 각 자리는 2의 거듭제곱을 나타낸다. 이진수를 나타내기 위해 접두사 0b를 사용합니다.

![](https://blog.kakaocdn.net/dna/KfHhc/btsPwCILEIY/AAAAAAAAAAAAAAAAAAAAAHkfF1GfSwmIwac3ThSMdz_67MrDGRUIQ6k8oLLVWS2n/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=8r%2Ba%2BQ01YhrJzpk7XJmQrD6DDd0%3D)

컴퓨터 분야에서 자주 사용되는 기법은 16진법(hexa-decimal), 16진수입니다.

이 표기법은 0부터 9까지의 10개 숫자와 A부터 F까지의 6개 문자(A는 10, F는 15에 해당)가 사용된다. C와 C++ 프로그래밍 언어에서는 접두사 0x를 사용해 16진수를 나타냅니다.

이 표기법이 많이 사용되는 이유는,

컴퓨터는 데이터를 일반적으로 8비트 단위(바이트)로 저장하는데, 16진수는 **2개의 16진수 자릿수가 정확히 1바이트를 표현하**기 때문입니다. **(1개의 16진수 자릿수가 정확히 4비트를 차지하니까)**

![](https://blog.kakaocdn.net/dna/c1hjPV/btsPxKTnxXd/AAAAAAAAAAAAAAAAAAAAAEDgKXxjUb8MIwLAXxwvWRfYggEyWCUZsQNQ8hweh_DV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9S5ODv31T2wS4OqccjISfxAEoIE%3D)![](https://blog.kakaocdn.net/dna/1Dqhw/btsPw0CmO7c/AAAAAAAAAAAAAAAAAAAAANxTnvUAlVxUmzA4qiqNx0xefYCM2OMCrM98v52oYLd7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=DyxLkdcB1Oi%2FvNTHQv35%2FCAzZiM%3D)![](https://blog.kakaocdn.net/dna/bq8f3h/btsPxLxY1ED/AAAAAAAAAAAAAAAAAAAAAB1vMZcrm3Z4FKuF221iiyPn2l2D2JJgAKmIUp5L5cye/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FOKI6UMnQ5SrnB%2FDgnhiffmprF4%3D)

### **Signed and Unsigned Integers (부호 있는/없는 정수)**

컴퓨터 과학에서는 부호 있는 정수(signed integer)와 부호 없는 정수(unsigned integer)를 모두 사용합니다.

**32비트 부호 없는 정수**는 값을 이진법으로 단순히 인코딩하여 표현한다.

 0x00000000 (0)에서 0xFFFFFFFF (4,294,967,295)

**32비트** **부호 있는 정수**를 표현하려면, 양수와 음수를 구분할 방법이 필요합니다.  
가장 간단한 방법 중 하나는 **부호 + 절댓값 방식입니다**.

이 방식에서는 가장 상위 비트(MSB)를 부호 비트로 사용하여서, 0이면 양수 / 1이면 음수로 표시할 수 있습니다.

이 방법은 각 절댓값에 대해 양수/음수 모두 존재하므로 0을 두 번 표현하게 됩니다.

하지만 대부분의 마이크로프로세서는 **더 효율적인 방식인 2의 보수(two’s complement) 표기법을 사용하여 음수를 인코딩합니다.**

이 방식은 0을 오직 하나의 형태로만 표현하며, 양/음수 연산이 훨씬 더 간편합니다.

### 

### **Fixed-Point Notation**

**정수는 분수나 무리수를 표현하려면 소수점의 개념을 표현하는 다른 형식이 필요합니다.**

처음 사용한 방법 중 하나는 고정소수점 표기법입니다.

**이 표기법에서는 전체 비트 중 얼마나 많은 비트를 정수부에 할당할지 임의로 정하고, 나머지 비트는 소수부를 표현하는 데 사용됩니다.**

최상위 비트(MSB, 오른쪽)에서 최하위 비트(LSB, 왼쪽)으로 이동하면서,

정수 부분 비트는 2의 점점 작은 거듭제곱 값들(…, 16, 8, 4, 2, 1)로 표현하고,

소수 부분 비트는 2의 역수 값들(1/2,  1/4,  1/8, 1/16, …)로 표현합니다.

예를 들어, 부호 비트 1개 + 정수부 16비트 + 소수부 15비트로 32비트 고정소수점 숫자로 173.25를 저장한다고 해봅시다.

부호 비트: 0b0 => +

정수부: 0b0000000010101101 (16비트) =>173

소수부: 0b010000000000000 (15비트) => 0.25

이것들을 하나의 32비트 정수로 결합하면 결과는 0x8056A000이 됩니다.

![](https://blog.kakaocdn.net/dna/cJ6EF7/btsPxiJAIdR/AAAAAAAAAAAAAAAAAAAAAKjTSYPRO-uFTmEZU2jUhaNxUPqCIRmQQM6yAQWdEAa-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=sQv1ALhGw%2FaWcjZa71QzeJEVQNg%3D)

**단점은 이 방식이 표현 가능한 정수 범위와 소수 정밀도를 동시에 제한한다는 것이다.**

**이 문제를 해결하기 위해 부동소수점(floating-point) 표현이 사용된다.**

### **Floating-Point Notation (부동소수 표현법)**

**부동소수점 표기법에서는 소수점의 위치가 고정되지 않고 지수(exponent)를 통해 조정됩니다.**

숫자는 아래의 세 부분으로 나뉩니다.

**1.부호비트 (Sign bit)**: 양수 또는 음수 여부

**2.지수 (Exponent)**: 소수점이 어디에 위치하는지를 지정해준다.

**3. 가수 (Mantissa)**: 소수점 전후의 실제 숫자들 ( 1/2^n으로 계산될 예정)

이 구조를 메모리에 어떻게 배치할지는 다양하지만, **가장 널리 쓰이는 표준은 IEEE-754입니다.**

**( 모회사 인턴 시험에서 이걸 봤던 기억이... 가장 널리 쓰이는 표준은 IEEE-숫자이다. True/Flase  고르는... )**

IEEE-754에 따르면 32비트 부동소수점 수는 다음과 같이 구성됩니다.

**부호 => 1비트**

**지수 => 8비트 (소수 위치를 정한다.)**

**가수 => 23비트  (숫자를 표현한다. )**

![](https://blog.kakaocdn.net/dna/brYXLq/btsPwxnhuF4/AAAAAAAAAAAAAAAAAAAAAHDLiYqEsc2axB3k77Rg_jFw0Zk6H4IY6SLFhiEvOq1C/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=DjutGqYp7mvtz3Eirpk5PLC1Cqs%3D)

부동소수점 수의 최종 값 v는 아래 수식으로 계산됩니다.

![](https://blog.kakaocdn.net/dna/u5sKN/btsPvjp3Oqq/AAAAAAAAAAAAAAAAAAAAAAVhzWFWGyBo3gyZa9YRckpochvsor7sd61a1ENt_rUw/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=EC7WJkim4iggSpcvI9r4ZHPtlzw%3D)

s: 부호비트 (0이면 +1, 1이면 -1)

e: 지수 (8비트, -127로 오프셋)

m: 가수 (23비트, 실제 값은 1 + m로 표현됨)

예제 값을 계산해봅시다.

s = +1,

e = 124 => 124 - 127 => -3

m = 1 / 2^2 => 1 / 4 => 0.25

![](https://blog.kakaocdn.net/dna/nBdAV/btsPwzyCz6p/AAAAAAAAAAAAAAAAAAAAAKoGJRMdUKXAtywNFWaZTY-3dEZdEX-88bFIucfgnphm/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wm%2BmiCN2fJBj6EPY0VpM5cE%2Fjh0%3D)

즉, 이 비트 패턴은 실제 값 0.15625를 표현합니다.

 Visaul studio에서 실험을 해봤습니다.

아래의 코드도 실제로 보면 값에 오차가 있고, 연산에 문제를 야기할 수 있습니다.

```
int main()
{
	if (1 + 0.1f == 1.1f) cout << "yeah";
	else cout << "What??";

}
```

![](https://blog.kakaocdn.net/dna/bnj1UN/btsPxlGtYXH/AAAAAAAAAAAAAAAAAAAAAN-MHPb2imjWGig_1d58Xeq4RyBEj7CyUFcQ5_V3zYSt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=VnSBL%2FkhybPVJZ19%2FBz0HcWja%2BM%3D)
![](https://blog.kakaocdn.net/dna/rquFq/btsPwFlfM6E/AAAAAAAAAAAAAAAAAAAAAE1m_cgCl-L9VAUta7XZutrfrxfZEjwc1TOoRzvHkfSS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xoi5UdMa4qI7X0i6uorYTwdGaNU%3D)

다행이 컴파일러에서 어떻게 잘 조정해주나봅니다. 허허 같다고 인식은 해주네욤. 허허허

![](https://blog.kakaocdn.net/dna/vp73t/btsPv5rAOB7/AAAAAAAAAAAAAAAAAAAAABH1G37C1FgF1vi3vazKEpfRswyN3vIPXSWoEvsv5IXM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Prh4QyFyMxZpBsQ6lagCmaCYgws%3D)

### **정밀도와 표현 범위 간의 트레이드오****프**

**정밀도는**

**수의 크기가 작을수록 커지고 (지수 부분의 비트 수를 적게하고, 가수 부분에 투자를 많이 할 수 있어서)**

**반대로 크기가 커질수록(지수 부분에 많은 비트를 투자, 가수 부분에 적게)정밀도는 낮아진다.**

=> 큰 숫자를 표현하려면 더 많은 비트를 지수부에 쓰게 되고, 가수부 에 쓸 비트가 줄어들기 때문입니다.

### **FLT\_MAX**

가장 큰 부동소수점 값으로는 약 3.403 \* 10^38이다.

가수는 23비트이므로 최대값은 16진수로 0x00FFFFFF이다.

**지수 255는 NaN, 무한대 를 가지므로 (NaN과 무한대 표기법이 같다는 의미는 아님, 가수 부분이 다름)**

**일반 수로서 최대 지수는 254입니다.( 바이어스 127을 빼면 127이 된다. )**

즉 2의 127비트가 왼쪽으로 시프트 된 값이다.

127 - 24 = 104 개의 0 비트가 패딩되고 있는 것으로 볼 수 있다.

이 패딩된 0들은 실제 32비트 값에 존재하지 않지만, 지수 덕분에 계산상으로 붙게 되는 것이다 .

결과적으로 FLT\_MAX는 아래와 같이 표현이 된다.

![](https://blog.kakaocdn.net/dna/JU4oD/btsPwcYfJX3/AAAAAAAAAAAAAAAAAAAAAM2YmS2g9f7uRNtxzAO7HP8z8Jn9LJa0QQbiExApLwj2/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nDk1%2BSN3PuHNj4a%2FifXKtDFaJl0%3D)

0이 패딩하고 있기 때문에 FLT\_MAX에 작은 값을 뺀다고 해도 실제로 값이 변하지는 않는다.

그래서 궁금해진것... 작은게 얼마난 작은건데?

```
float a = FLT_MAX;

if (a == a - 1) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 10) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 100) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 1000) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 10000) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 100000) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 1000000) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 10000000) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 100000000) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 1000000000) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 10000000000) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 100000000000) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 1000000000000) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 10000000000000) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 100000000000000) cout << "Still" << "\n";
else cout << "changed";
if (a == a - 1000000000000000) cout << "Still" << "\n";
else cout << "changed";
if (a == a - pow(10, 30) ) cout << "Still" << "\n";
else cout << "changed";
```

![](https://blog.kakaocdn.net/dna/xx1a3/btsPwJumh5n/AAAAAAAAAAAAAAAAAAAAADSGreJTijkngmDercIP2i1XPQIqJyAXwk7x_5t0sfuF/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=SylPV2OgyNIkTgjUw92SQOCB1fk%3D)

100조 넘는 수를 빼도 안변하는데 이걸 작다고 할 수 있나...? 허허허

1보다 작은 매우 작은 수에서는 반대 현상이 일어난다. ( 음수가 아닌 )

결론적으로, 부동소수점 수는 항상 일정한 수의 정밀도를 가지고, 지수를 통해 표현하고자 하는 수의 범위를 이동시킨다.

### **Subnormal Values**

여기서 중요한 점은, 부동소수점에서 표현 가능한 FLT\_MIN(0 이 아닌)과 0 사이에 간격이 존재한다는 점이다.  
이 간격은 실수(real number)가 양자화(quantized) 되어 있다는 것을 의미합니다.

![](https://blog.kakaocdn.net/dna/KUovp/btsPw3G5bpx/AAAAAAAAAAAAAAAAAAAAAB9RbQkF9j_kqOoemCO1j0n3gA4xNwV6lbly8qDGeMK3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=dr%2BmaU5u6XdQp3j7E%2F7dqfArBKo%3D)

16진수 표현: 0x00800000

지수: 0x01 = 1 - 127 = -126  => 서브 노말을 위해서 1이 가장 작은 값

가수: 전부 0 (암묵적 선행 1은 존재)

그런데 이보다 작은 값은 0이 되어버린다.

0과 ±FLT\_MIN 사이의 간격을 채우기 위해 서브노멀(subnormal) 값이 등장한다.

서브노멀 값은 지수 필드가 0일 때 등장하며, 다음과 같은 해석을 적용한다

![](https://blog.kakaocdn.net/dna/cQOD5Z/btsPxeWvwTh/AAAAAAAAAAAAAAAAAAAAAKL21ORaxazf23ppZlM-KvZNJD-d8iAcEWcqXHS561-U/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=YAF2CunC2CfdL7imA04u5g3aZZg%3D)

**지수는 0에서 1로 바꾸고** ( 지수부가 0에서 1이 된건, 크기 측면에서 사실상 무의미한 변화)

**가수 부분의 암묵적 선행 1은 0으로 대체된다.** 1+m이 m으로 변하는 것 ( 이게 더 큰 변화라고 생각, FLT\_MIN보다 훨씬 작은 값으로 변화된 것이다.)

이로 인해 -FLT\_MIN ~ +FLT\_MIN 사이의 공백이 선형 간격의 서브노멀 수로 채워진다.  
**이 구간에서 0에 가장 가까운 수는 FLT\_TRUE\_MIN으로 정의된다.**

**서브노멀 값이 가지는 이점**

0 근처에서의 정밀도 확보

예를 들어, a == b 와 a - b == 0.0f가 동일한 의미를 갖도록 해줌  
(서브노멀이 없었다면, a != b 임에도 a - b == 0.0f로 나올 수 있음)

## **Machine Epsilon(머신 입실론)**

특정 부동소수점 형식에서, machine epsilon은 다음 조건을 만족하는 **가장 작은 값입니다.**

![](https://blog.kakaocdn.net/dna/bCxl5y/btsPxWN1QOk/AAAAAAAAAAAAAAAAAAAAALJzQwRmW_XJVSatFpepBGfd1m83Uj-P7poyTaSeE3M7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=6rV8KqJzeuKaFVNWSoMWHgQ0%2Bs4%3D)

IEEE-754 32비트 기준, 입실론 = 2^-23 ( 약 1.192  \* 10^-7 )

이는 1.0f 값의 가장 작은 변화 단위

입실론 보다 더 작은 값을 1.0에 더해도 가수에 반영되지 않고 잘려나갑니다.

즉, 23비트 가수의 정밀도 한계를 설명하는 값입니다.

## **ULP (Units in the Last Place)**

ULP는 **가수의 마지막 비트 하나 차이로 발생하는 값 차이**를 의미합니다.

ULP는 지수에 따라 2x로 증가하고,  
부동소수점 수의 정밀도는 지수에 따라 달라집니다.

ULP는 다음과 같은 상황에서 유용합니다.

1. 연산 오차 허용치 계산

2. 다음 표현 가능한 값이나 이전 표현 가능한 값을 찾을 때

**사용되는 예시로**

**a ≥ b를 a + 1 ULP > b로 바꾸어 연산을 단순화할 때**

Naughty Dog 엔진에서는 모든 비교를 < , > 로 통일 시켜 로직을 최적화 했다.

**(>= 을  x + 1 ULP >  으로 변환하는 것이다. )**

### **Impact of Floating-Point Precision on Software (부동소수점 정밀도가 소프트웨어에 미치는 영향)**

유효 숫자 정밀도(limited precision)와 **머신 엡실론(machine epsilon)** 개념은 실제 게임 소프트웨어에서 중요한 영향을 미칩니다.

예를 들어, 게임의 절대 시간(초 단위)을 추적하기 위해 부동소수점 변수를 사용한다고 해봅시다.  
그럼 게임을 얼마나 오랫동안 실행할 수 있을까요?

시계 변수의 **값이 너무 커져서**, 그 위에 1/30초(프레임 단위 시간)를 더해도 **값이 변하지 않게 되는 시점**이 언제일까요?

정답은 **12.14일**, 즉 2^20 초(약 1,048,576초)다.

이는 대부분의 게임 실행 시간보다 훨씬 길기 때문에,

게임에서 초 단위로 시간을 측정할 때 32비트 float를 사용하는 것은 대부분 문제없었습니다.

=> 여기서 복습 왜 시계변수의 값이 충분히 커졌을  때 1/30초를 더하는게 의미가 없어지는 순간이 올까?

=> float는 지수, 가수분으로 나뉜다. bit수는 한정적인데 높은 값을 표현하기 위해서 지수가 커진다면, 가수로 표현할 수 있는 상대적인 정밀도는 떨어지게 된다.

=> 1/30을 표현할 지수가 부족해지는 것

하지만, 부동소수점 포맷의 한계를 이해하고,

잠재적 오류가 발생할 수 있는 시점에 대비할 수 있어야겠죠?

### **Primitive Data Types**

C와 C++은 다양한 **기본 데이터 타입**을 제공합니다.  
이 타입들의 크기와 부호 여부는 C/C++ 표준이 가이드라인을 제공하긴 하지만,  
**실제로는 각 컴파일러가 하드웨어 성능을 최대로 끌어내기 위해 세부 정의를 달리할 수 있다.**

**char**  
일반적으로 **8비트**이고, ASCII 또는 UTF-8 문자를 저장할 수 있는 크기.  
어떤 컴파일러는 char를 signed로, 어떤 컴파일러는 unsigned로 처리한다.

**int, short, long**

int는 **타겟 플랫폼에서 가장 효율적인 크기의 정수**로 지정됨 ( 최소 2바이트는 보장해야된다. )  
(예: 32비트 CPU에서는 32비트, 64비트 CPU에서는 64비트일 수도 있음)

short는 int보다 작도록 설계되며 보통 **16비트**

long은 int보다 같거나 크며, **32비트 또는 64비트**일 수 있음

**float**  
대부분의 현대 컴파일러에서 float는 32비트 IEEE-754 부동소수점 값

**double**

double은 64비트 정밀도(double-precision)를 가진 IEEE-754 float

**bool**  
true/false 값을 표현하지만 크기는 컴파일러마다 다름  
일반적으로 1비트가 아닌 8비트 또는 32비트로 구현됨 (컴파일마다 다르긴 한데, 일단은 1바이트라고만 알고 있자)

=>언리얼 코딩 규에서는 bool의 크기를 추정하지 말라고한다.

### **Portable Sized Types (이식성 있는 고정 크기 타입)**

C/C++의 기본 타입은 이식성(portability)을 위해 크기를 명시하지 않는다.  
하지만 게임 엔진처럼 하드웨어를 다루는 소프트웨어에서는 변수의 정확한 비트 수를 아는 것이 매우 중요하다.

C++11 이전에는 비표준 키워드를 사용했다.

```
__int8, __int16, __int32, __int64
```

이 외에도 각 컴파일러마다 고유한 고정 크기 타입이 있었다.

이러한 플랫폼 차이를 극복하기 위해,

대부분의 게임 엔진은 커스텀 타입을 정의해서 사용했다.

**C++11 부터는 <cstdint> 헤더가 도입되서, 표준화된 고정 크기 정수 타입이 제공된다.**

```
std::int8_t, std::int16_t, std::int32_t, std::int64_t

std::uint8_t, std::uint16_t, std::uint32_t, std::uint64_t
```

이 표준 타입들은 컴파일러별로 직접 타입을 감쌀 필요가 없어졌고,  
코드 이식성과 명확한 타입 크기 보장을 동시에 확보할 수 있도록 해줬다.

### **Multibyte Values and Endianness (다중 바이트 값과 엔디안)**

**8비트를 초과**하는 값(예: 16, 32, 64비트 값)은 모두 **멀티바이트(multibyte)** 값이라고 부른다.

**Endian은 바이트를 정렬하는 방식이다.**

멀티바이트 값은 메모리에 두 가지 방식 중 하나로 저장될 수 있다.  
어떤 방식을 쓰느냐는 CPU 아키텍처에 따라 다르다.

#### 리틀 엔디안 (Little-endian)

**하위 바이트를 더 낮은 주소에 저장함**

예: 0xABCD1234 => 메모리에는 [0x34, 0x12, 0xCD, 0xAB] 순서로 저장됨 ( 인텔 CPU 계열 )

#### 빅 엔디안 (Big-endian)

**상위 바이트**를 **더 낮은 주소에 저장**

예: 0xABCD1234 → 메모리에는 [0xAB, 0xCD, 0x12, 0x34] 순서로 저장됨

(Wii, Xbox 360, PS3 등 에서 기본적으로 사용)

### **Interger Endian-Swapping**

정수를 엔디안 스와핑하는 건 개념적으로 어렵지 않다.  
MSB(가장 상위 바이트)를 LSB(가장 하위 바이트)와 바꾸는 식으로, 양 끝에서 시작해 **중앙까지 쌍으로 바꾸는 작업**을 반복하면 된다

```
0xA7891023 => 0x231089A7
```

**어려운 부분은 바이트 위치 파악이다**.

예를 들어 C/C++ 구조체의 내용을 메모리에서 파일로 저장한다고 할 때,  
구조체 내 각**멤버의 크기와 위치를 파악한 뒤,**  
각각에 대해**적절한 바이트 스와핑을 적용해야 한다.**

예시 구조체

```
struct Example {
    U32 m_a;
    U16 m_b;
    U32 m_c;
};
```

이 구조체를 바이너리 파일로 저장할 때

```
void writeExampleStruct(Example& ex, Stream& stream) {
    stream.writeU32(swapU32(ex.m_a));
    stream.writeU16(swapU16(ex.m_b));
    stream.writeU32(swapU32(ex.m_c));
}
```

바이트 스와핑 함수 (천천히 읽어보면 이해가 될 것이다.)

바이트 별로 함수가 만들어진다.

```
inline U16 swapU16(U16 value) {
    return ((value & 0x00FF) << 8)
         | ((value & 0xFF00) >> 8);
}

inline U32 swapU32(U32 value) {
    return ((value & 0x000000FF) << 24)
         | ((value & 0x0000FF00) << 8)
         | ((value & 0x00FF0000) >> 8)
         | ((value & 0xFF000000) >> 24);
}
```

잘못된 방법

```
// 잘못된 방식
U8* pBytes = reinterpret_cast<U8*>(&ex);
```

이처럼 구조체 전체를 단순히 바이트 배열로 캐스팅해서 **일괄 바이트 스왑하는 것은 잘못된 방식이다.**  
각 멤버마다 크기와 경계가 다르기 때문에,  
모든 필드를 개별적으로 스왑해줘야 정확한 결과를 보장할 수 있다.

### **Floating-Point Endian-Swapping (부동소수점의 엔디안 스와핑)**

IEEE-754 부동소수점은 내부적으로 **부호 비트, 지수 비트, 가수 비트**로 구성되어 있지만,  
엔디안 스와핑에서는 그런 내부 구조를 신경 쓸 필요 없다.

**바이트는 바이트일 뿐이기 때문**이다.

그냥 float 값을 정수처럼 취급해서 바이트를 뒤집고, 다시 float로 해석하면 된다

```
float value = 1.0f;
std::uint32_t* asInt = reinterpret_cast<std::uint32_t*>(&value);
std::uint32_t swapped = swapU32(*asInt);
float* result = reinterpret_cast<float*>(&swapped);
```

이처럼 **포인터 reinterpret\_cast를 사용해 float을 int로 해석**할 수 있는데,  
이건 흔히 타입 패닝(type punning)이라고 부른다.

하지만 C++에서 **Strict Aliasing Rule**이 활성화되어 있을 경우,  
이 방식은 **최적화 오류나 미정의 동작을 유발할 수 있다.**

(strict aliasing: 서로 다른 타입의 포인터는 같은 메모리를 가리키지 않는다는 약속)

**Union을 사용한 표준적인 방식**

```
union U32F32 {
    U32 m_asU32;
    F32 m_asF32;
};

inline F32 swapF32(F32 value) {
    U32F32 u;
    u.m_asF32 = value;
    u.m_asU32 = swapU32(u.m_asU32);
    return u.m_asF32;
}
```

### **킬로바이트(Kilobytes)와 키비바이트(Kibibytes)**

프로그래밍을 하면서 메모리 크기를 표현할 때, 아마 킬로바이트(kB)나 **메가바이트(MB)** 같은 SI 단위(국제단위계)를 자주 사용했을 것이다.

그런데 메모리 용량을 **2의 거듭제곱으로 계산**하는 컴퓨터 시스템에서 이런 단위를 그대로 쓰는 건 **정확하지 않다**.

프로그래머들이 1킬로바이트라고 말할 때는 보통 1024바이트(2^10)를 의미한다.  
하지만 SI 단위에서 kilo는 정확히 1000(10^3)을 뜻하지, 1024는 아니다.

이 혼란을 해결하기 위해, **IEC는 1998년에** 컴퓨터 과학에서 사용할 새로운 접두어 체계를 만들었다.  
이 체계는 10진수(SI)가 아니라 **2진수 기반의 접두어**를 사용한다.

1024바이트 = 키비바이트(Kibibyte), 약칭 KiB

1,048,576바이트(1024×1024) = 메비바이트(Mebibyte), 약칭 MiB

![](https://blog.kakaocdn.net/dna/GS78f/btsPyopK3DV/AAAAAAAAAAAAAAAAAAAAADQljPrNbgUhcVvAU5PRksgXH7yOV28CKF4R5HMA52y5/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=yX58D7oBH29SY8xUpw9BsPBPoD4%3D)

###