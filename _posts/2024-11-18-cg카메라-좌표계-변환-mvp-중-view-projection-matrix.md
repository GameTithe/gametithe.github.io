---
title: "[CG]카메라 좌표계 변환 (MVP 중 View, Projection Matrix)"
date: 2024-11-18
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **Model View Matrix**

모델 뷰 행렬은 **월드 좌표계**에서 **카메라 좌표계**로 변환하는데 사용된다.

즉, 카메라의 시점(카메라가 0,0,0에 있을 때 )을 기준으로 물체가 어떻게 보일지 결정하는 것이다. 카메라 좌표계로 변환하기 위해서는 다음의 두 가지 변환이 필요하다. (카메라를 0,0,0으로 돌려놓기 위해서 T,R했던 것을 반대로(역행랼) 다시 취해줘야 된다는 작업)

전체 변환 행렬 W는 W=T⋅R로 나타낼 수 있으며, **카메라 좌표계로 변환된 행렬 V는 W의 역행렬로 얻을 수 있다.**

![](https://blog.kakaocdn.net/dna/pcdQw/btsKEsQ30yI/AAAAAAAAAAAAAAAAAAAAAAxvA_ObAR3TkJioLkJEWiAyaNgro2IqElWqpEB-Zxqz/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=sqWGDclFZY%2Bofdwtr4ynrXHZOR4%3D)

### **Rotation Matrix**

카메라의 위치와 방향을 설정하는 함수로, 카메라 위치를 기준으로 한 좌표계 변환을 수행합니다. Look-At 함수의 주요 수식은 다음과 같습니다:

* **단위 벡터 n: (f - e)/|f - e|,** 카메라의 시선 방향을 나타낸다.​
* **단위 벡터 v: (u – (u · n) n) / |u – (u · n) n|** 카메라의 '위쪽 방향'을 나타내며, '위 벡터' u와 시선 벡터 n을 이용해 수직 성분을 계산하여 얻을 수 있다.​
* **단위 벡터 w**: n과 v의 외적을 통해 계산해서 얻는다.

![](https://blog.kakaocdn.net/dna/cFpWJB/btsKMHBj3S5/AAAAAAAAAAAAAAAAAAAAALvtyd7wjWbUxv00y1B6NOfrFJKm3ubV9r-n8MFdtiso/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=P91p73pFAOvMbywINdtWkYsx2R0%3D)

회전 행렬 R는 이렇게 구성된다.

![](https://blog.kakaocdn.net/dna/brKlO6/btsKMhJ3c3m/AAAAAAAAAAAAAAAAAAAAAPTaSr4hzc0s89UafHzi0y86WvuupPZ4QDuFNrnY0X36/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=NBAfxwinSmTvf07Li7pNRVhpWq4%3D)

Translation은 간단하니 바로 합치면 아래와 같이 된다.

![](https://blog.kakaocdn.net/dna/y2Csg/btsKMCHbVuw/AAAAAAAAAAAAAAAAAAAAACcrujtxxZRzBG_faUToUnjNyRUTxERgLmmaVHgCW2BP/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ENgJsVQH8Axwc0ZD1PITLoWIolw%3D)![](https://blog.kakaocdn.net/dna/bjAZkK/btsKN3i2UAf/AAAAAAAAAAAAAAAAAAAAABz3p0b9brWsfSSfi-RsAlBOpqS5_w7-MbEZ6u6UxhL5/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=rBQx%2BromwuqGZ1giVxVXx8EXFEI%3D)

### 

**여기까지가 원점으로 카메라를 가지고 와서 물체들을 본 것이고 ,**

**이제 cliping을 하는 단계라고 볼 수 있다. ( view frustum안에 들어온 물체만 판별해서 그리기)**

### **Projection Matrix**

#### 

#### **직교 투영 (Orthographic Projection)**

직교 투영은 물체의 거리에 관계없이 동일한 크기로 보이게 하는 투영 방식이다.

NDC()에 x,y 값을 유지한체로 투영한다고 생각하면 간단하다.

그래서 Translation은 ox,oy는 가운데정렬해주, oz는 nearPlane으로 가져오기만한다.

Scale또한 x,y좌표를 -1~ 1로 맞춰주는게 끝이다.

```
mat4 myOrtho(float xmin, float xmax,
	float ymin, float ymax,
	float znear, float zfar)
{
	mat4 m;
	float ox = (xmin + xmax) / 2;
	float oy = (ymin + ymax) / 2;
	//float oz = -1.0f*(nearr + farr) / 2;
	float oz = -1.0f * (znear);

	mat4 T = Translate(-ox, -oy, -oz);

	float sx = (xmax - xmin);
	float sy = (ymax - ymin);
	float sz = (zfar - znear);
	mat4 S = Scale(2 / sx, 2 / sy, 1 / sz);

	m = S * T;
	return m;
}
```

### **원근 투영 (Perspective Projection)**

원근 투영에서는 거리에 따라 물체의 크기가 달라진다.

여러 단계로 나뉘는데,

찬찬히 해보자

**Z**

far plane의 위치를 (볼 수 있는 최대 범위) 1로 만들어 줄 것이다. (계산하기 편하게)

=>  z = 1 이건 far을 far로 나눠주면된다.

**X,Y**

x,y Scale Matrix에 필요한 값을 tan을 이용해서 구할 수 있다.

그림을 보면 쉽게 이해할 수 있다.

![](https://blog.kakaocdn.net/dna/n2FKm/btsKNrkIXWx/AAAAAAAAAAAAAAAAAAAAAGFAo5-YCvHsKaOPd6HJIlVbB26BSaN9V4xWogci6Dmq/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xtRW5fkJyR1fuvYjamrAAg94EL8%3D)![](https://blog.kakaocdn.net/dna/qq49z/btsKNZ8YkDo/AAAAAAAAAAAAAAAAAAAAAEzDQ7OJhwfFYClk4GNqUb0dGyVA-Kj8jcXTXOitZ_Tp/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=tq7ubx%2FIEYEw2LS27pmbsoU67Ro%3D)

그렇기 때문에 Scaling Matrix는 아래와 같다.

![](https://blog.kakaocdn.net/dna/xEFED/btsKNZHUhH3/AAAAAAAAAAAAAAAAAAAAAMmgGuWt-Uw7fOvmgYfhK0LYBZbrCsx8J5Y-aNc9E5K-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hfYpgH9jvaHICixQLads1%2B2VksE%3D)

여기까지 하면 아래와 같은 모양으로 완성된 것이다. 여기서 간단하게 물체를 그릴 수 있는 방법은 NearPlane을 확대하는 것이다. 그러면 가까이 있는 물체도 같이 커질 것이고, 자연스럽게 원근감이 형성이 될 것이다.

이때 사용하는 matrix가 hinging matrix인데 이건 필요할 때 찾아서 쓰자 ..ㅎ

![](https://blog.kakaocdn.net/dna/bwzNGt/btsKMOHsQtT/AAAAAAAAAAAAAAAAAAAAAGHkBvXgY_6S5Py_4akKA1bXX4gMAG41DsNKRzhGuYAf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xCTm3upD70LfVaeiOTsvhSFDN2c%3D)![](https://blog.kakaocdn.net/dna/bQ2qqt/btsKN3pTvqF/AAAAAAAAAAAAAAAAAAAAAGLPoY9EFx7h0X8FXPXS_JoNJ61fFQE4sbQg5mYwfA1R/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=RWaguPXmNhUWk2BEXbmha476iow%3D)

그래서 H\* S가 결론적으로 아래와 같이 되는 것이다.

![](https://blog.kakaocdn.net/dna/njYLR/btsKMk7RexB/AAAAAAAAAAAAAAAAAAAAAFUc9umedJL01o9_wH9G_uSerXF7xRS1-xBYI4BPX9uY/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=TUQCDUy%2Bagnjo3BxwgUG7IKIT7M%3D)

```
mat4 myPerspective(float fovy, float aspect, float zNear, float zFar)
{

	float theta = fovy / 180.0f * 3.141592f;
	float ymax = zFar * tan(theta / 2.0f);
	float ymin = -ymax;

	float xmax = ymax * aspect;
	float xmin = -xmax;


	mat4 S; // Scaling matrix for making canonical view volumn
	// -1 ~ 1 => 2
	S = Scale( 2.0f /  (xmax - xmin),  2.0f / (ymax - ymin), 1 / zFar );
	float c = -1 * zNear / zFar; // z는 음수
	
	mat4 H(1.0f); // following unhingin transformation
	H[2][2] = 1.0f / (c + 1);	H[2][3] = -c / (c + 1);
	H[3][2] = -1.0f;			H[3][3] = 0.0f;

	return H * S;
}
```

### **구현:**

**<https://tithingbygame.tistory.com/106>**