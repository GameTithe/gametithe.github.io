---
title: "[CG] Shadow Map(PCF, Edge with Random Sampling)"
date: 2025-02-07
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### 일단 기본적인 ShadowMap에 대해서 설명을 하고 심화(?)로 들어가겠습니다.

### 

### **ShadowMap**

### **1. light source에서의 depth map이 필요하다.**

**( camera 위치가 아닌 light 위치에서의)**

(shadow map이 함축하고 있는 의미는

light에서의 거리를 저장할 뿐아니라 **light에서 물체가 보이는지에 대한 여부를 저장을 하는 것**이다.)

개구리를 비추고 있는 빨간 조명에서 depth buffer를 그린것이다. 우측을 보면 잘 그려지고 있는 것 같다.

(지금은 1개의 조명을 사용하고 있지만, 나중에 2개 이상일 때는 우예해야될까..흑흑)

![](https://blog.kakaocdn.net/dna/ca9fd7/btsL4KDcam5/AAAAAAAAAAAAAAAAAAAAAOcpdChzms6rKxIgo1c0flYyAS54i0b9tdbiBlti9SCQ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wYkbywxZY6yDYXyoMdowMi2KUP0%3D)![](https://blog.kakaocdn.net/dna/bkaU0P/btsL22ytygE/AAAAAAAAAAAAAAAAAAAAAJXuKnWmjXYNF9Al0sWdyFH0aHRGFneYJ7KUJ0oMb1Sw/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9bofXoKJsZBBo3KxlDOBXUpvEIk%3D)

### **2. 물체를 렌더링 할 때 depth map가 비교를 그림자 부분인지를 판별한다.**

헷갈릴만 한 것들

1. depth map에서 0이 의미하는 것은 near plane의 거리에 있다는 것이다. 그러니 z가 0일 때와는 다른 의미이다.

2.

우리는 shadow map을 사용하기 때문에 texture의 범위를 벗어났을 때 (1보다 큰)를 고려해야된다.

기본적으로는 (0,0,0,0)으로 Wraping되기 때문에,

아래의 코드를 사용해서, 1.0으로 바꿔 우회해줘야된다.( 1.0은 그림자 생성을 피할 수 있음)

```
GLfloat border[] = { 1.0f, 0.0f, 0.0f, 0.0f };
glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border);
```

3.

clip 좌표계에서의 z의 범위는 [-w, w]이고, viewport 변환 이후에는 0~1이다.

clip coordinate ( z range: [-w, w] )  => NDC( z range: [-1, 1]) => viewport transformation( z range: [0,1])이라고 정리할 수 있다. (glDepthRange로 viewport transformation에서의 depth값을 조정할 수 있다.)

clip 좌표계를 texture(depth map)좌표계로 변환하기 위해서는 아래와 같은 변환 행렬이 필요하다.

**(잠시 집고 넘어갈게 책에서는 clip좌표계의가 perspective division을 한 이후로 가정하고 말하고 있다.)**

clip 좌표계의 범위가 [-1, 1]이니, texture 좌표계인 [0, 1]로 바꾸기 위해서 x0.5 +0.5를 해서 정규화해주는 bias matrix이다.

![](https://blog.kakaocdn.net/dna/c6U0qd/btsL3i8YOCk/AAAAAAAAAAAAAAAAAAAAAIpAMFqTbWyNl5LLbTR0SCYAOj7fYCsJSxb7Ac4SB62B/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=aoGtyEm96TnbL0IksyywY5fGXAk%3D)

![](https://blog.kakaocdn.net/dna/wlQdi/btsL3PyFWOU/AAAAAAAAAAAAAAAAAAAAAGkJMQCZzKAHqR0D9zyq-feR1uyB8Cnv2fF2ulhGKFus/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=HmIza1kwXmKBXD%2BOgiNYXBVm9fo%3D)

q를 사용해서 shadowMap의 Coordinate로 사용할 것 이다.

W: model matrix -> world space로 변경

V: View Matrix(광원의) , P: Perspective Matrix(광원의) : VP를 이용해서 light의 ClipSpace로 이동한다.

B: Bias를 사용해서 texcoordinate[0,1]로 변경해준다.

(perspective division을 해주는 것을 잊지말자,

사실 openGL의 textureProjOffset는 내부적으로 perspective division을 해준다. ㅎㅎ)

이렇게 까지하면, 1번에서 만든 shadowMap의 texel에 접근이 가능하다.

shadowMap을 sampler2DShadow로 만들고 사소한 셋팅만 해주면 자동으로 비교하고, 0 or 1을 반환해준다.

```
uniform sampler2DShadow shadowMap; 

float shadowDepth = textureProj(ShadowMap, ShadowCoord).r;
  
FragColor = vec4(diffAndSpec * shadow + ambient, 1.0);
```

### **따란**

그림자가 잘 만들어진자. 하지만 aliasing이 나타난다..!

![](https://blog.kakaocdn.net/dna/bF8Sst/btsL51ky0iV/AAAAAAAAAAAAAAAAAAAAAG4PRujzWxKcWYoqPoqBgb2UHokGuhinjvMKT9bNC8bY/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=mOUw6y8EfWXLzA%2B3xRIOfIYMBZM%3D)![](https://blog.kakaocdn.net/dna/cFy9Ik/btsL50srXT4/AAAAAAAAAAAAAAAAAAAAAD44lNf74SB9eETpntxYf4xBStbRqMtojeyl-RauKo7S/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ScVeWZiObplBlphcjdhqV7nXCqc%3D)

여기서 더 부드럽게 하는 방법은

**주변 texel로부터 sampling을 많이하는 것이다.**

**그리고 이게 PCF라고 볼 수 있다.**

```
vec4 shadowCoords = shadowMatrix * pos;
//shadowCoords /= shadowCoords.w;
	
//PCF
//float shadow = 1.0;
//if( shadowCoords.z >= 0 ) {
//    shadow += textureProjOffset(shadowMap, shadowCoords - 0.05, ivec2(-1,-1));
//    shadow += textureProjOffset(shadowMap, shadowCoords - 0.05, ivec2(1,-1));
//    shadow += textureProjOffset(shadowMap, shadowCoords - 0.05, ivec2(-1,1));
//    shadow += textureProjOffset(shadowMap, shadowCoords - 0.05, ivec2(1,1));
//}
//
//shadow *= 0.25;
```

![](https://blog.kakaocdn.net/dna/bYs3b9/btsL470thyB/AAAAAAAAAAAAAAAAAAAAAO1WdV7kmr3bN-U5htW9vdVTzJIoIyRvx6wvBYtmfGvR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9I1siGzsWMPjC6ChF9ZfWF18arA%3D)

하지만,, I want more soft .... penumbra

위의 방법에서는 문제점 2개가 있다.

1. 더 부드럽게 하기 위해서는 더 smapling을 많이해야된다.

2. sampling을 많이 할 수록 wastede effort가 생긴다. ( 중심부 그림자는 sampling을 많이 하던 안하던 동일한 값을 유지하기 때문에 대부분의 연산은 필요없는 연산이다. )

여기에 대한 해결방법이다. ( GPU Gems 2 에 실린 방법이다.)

1. 원형 패턴의 offset으로 샘플링을 한다.

2. 원형 패턴에서 바깥 쪽에 있는 offset을 먼저 sampling해서 그림자 내부인지 외부인지를 판단하다.

아래와 같이

![](https://blog.kakaocdn.net/dna/Pdr9G/btsL8VlMFZE/AAAAAAAAAAAAAAAAAAAAAANDV7j7J2PN8HK9tDAKB-P_tWR1w3HiNG8YXUr35W7o/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=tMxXWhGN8ZAfNb%2BnC34ydm9RT6o%3D)![](https://blog.kakaocdn.net/dna/bxc1yV/btsL7eRcXMR/AAAAAAAAAAAAAAAAAAAAAIkzuvW3N5JizXdRaZuIcU8uXVHydrUq65ovSxE5_T9I/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=OnNqyEWwBzXDypV7I%2FuDJuTqCYU%3D)

내가 사용한 코드를 살짝 설명하겠다

1. xyzw모두 사용

중요한 것은 xyzw를 알차게 사용중이다.

x,y에는 첫 번째로 sampling할 x1,y1을 할당하고

z,w에는 두 번째로 sampling할 x2,y2를 할당한다.

jittering은 이런과정이다. random으로 뿌려주는

![](https://blog.kakaocdn.net/dna/d39enJ/btsMaPRLz4y/AAAAAAAAAAAAAAAAAAAAAJJqW17niUNdfK_eG1oRMjWYhFShQkKzole_uTT8R_zc/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=FCcY9PqCme0j2GYZuAAjGdhTxnw%3D)

여기서 x은 [0,samplesU -1], y는 [0, samplesU - 1]이다.

각각의 값들이 아래의 식으로 디스크로  변환된다. ( sin, cos에 값을 넣어보면 바깥쪽부터 만들어지는 것을 알 수 있다. shader에서 texture 순서대로 사용할 것이기 때문에, 바깥쪽부터 만들어지는 sample들을 순서대로 값을 할당한다.)

![](https://blog.kakaocdn.net/dna/dMcQfL/btsMcgORKO1/AAAAAAAAAAAAAAAAAAAAAPhQ6QDMvtt-_ZAMp6cU42Kg4XaCShGVJrbLK57vdo9e/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=dK9%2BHkSxuJE76HDKg57V%2BKn7hpk%3D)![](https://blog.kakaocdn.net/dna/bteo4k/btsMcjrg5cC/AAAAAAAAAAAAAAAAAAAAAEkA5Ea6zKOc3bVCCNRIj9gRXe4l8ojpyOjUB7XNv5pZ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xrgwSL2ng%2FkDLDsRiIpF8kBTeSk%3D)

```
    x1 = k % (samplesU);						 
    y1 = (samples - 1 - k) / samplesU;		 
    x2 = (k + 1) % samplesU;				 
    y2 = (samples - 1 - k - 1) / samplesU;		 
	
    //...
  
    data[cell + 0] = sqrtf(v.y) * cosf(glm::pi<float>() * 2 * v.x);
    data[cell + 1] = sqrtf(v.y) * sinf(glm::pi<float>() * 2 * v.x);
    data[cell + 2] = sqrtf(v.w) * cosf(glm::pi<float>() * 2 * v.z);
    data[cell + 3] = sqrtf(v.w) * sinf(glm::pi<float>() * 2 * v.z);
```

```
float* Utils::makeRandTex(int texSize, int samplesU, int samplesV)
{
	// texSize : texture Size
	// smaplesU, samplesV: 샘플링할 범위 ?  

	//float* data = makeRandTex(texSize, samplesU, samplesV);
	int size = texSize;
	int samples = samplesU * samplesV;  //각 픽셀마다 생성할 샘플 개수
	int bufSize = size * size * samples * 2;
	// size * size * 2: 2D 해상도 + (xy)(zw)


	float* data = new float[bufSize];

	for (int i = 0; i < size; i++)
	{
		for (int j = 0; j < size; j++)
		{
			for (int k = 0; k < samples; k += 2)
			{
				int x1, y1, x2, y2;
				  
				x1 = k % (samplesU);						// [0, samplesU) -> 0 ~ U-1 순서대로
				y1 = (samples - 1 - k) / samplesV;			// [0, samplesV)
				x2 = (k + 1) % samplesU;					// [0, samplesU)
				y2 = (samples - 1 - k - 1) / samplesV;		// [0, samplesV)
				
				vec4 v; 
				// Center on grid and jitter
				v.x = (x1 + 0.5f) + jitter();
				v.y = (y1 + 0.5f) + jitter();
				v.z = (x2 + 0.5f) + jitter();
				v.w = (y2 + 0.5f) + jitter();
				   

				// Scale between 0 and 1
				v.x /= samplesU;
				v.y /= samplesV;
				v.z /= samplesU;
				v.w /= samplesV;

				 
				// Warp to disk
				// k로 depth를 쌓는다..
				int cell = ((i)+(size * j) + size * size * (k / 2)) * 4;

				data[cell + 0] = sqrtf(v.y) * cosf(glm::pi<float>() * 2 * v.x);
				data[cell + 1] = sqrtf(v.y) * sinf(glm::pi<float>() * 2 * v.x);
				data[cell + 2] = sqrtf(v.w) * cosf(glm::pi<float>() * 2 * v.z);
				data[cell + 3] = sqrtf(v.w) * sinf(glm::pi<float>() * 2 * v.z); 
			}
		}
	}

	return data; 
}
```

이렇게 생성한 texture를 shader로 넘겨서 계산을 해준다.

우선 반을 계산했을 때, 0이나 1이 아니면 ( 테두리일 경우) 남은 반절을 계산해서 soft shadow를 만들 수 있게 했다.

```
float randomSampling(vec4 shadowCoords)
{
	ivec3 offsetCoords;
	// [0, texSize) 
	offsetCoords.xy = ivec2( mod( gl_FragCoord.xy, offsetTexSize.xy) );

	float sum = 0.0;

	int samplesDiv2 = int(offsetTexSize.z); 

	float bias = 0.005;
	for(int i = 0; i < samplesDiv2; i++)
	{
		offsetCoords.z = i;
		vec4 offsets = texelFetch(offsetTex, offsetCoords, 0) * radius * shadowCoords.w;
		
		{	
			vec4 sc = shadowCoords;
			sc.xy = shadowCoords.xy + offsets.xy;
			sc.z -= bias;
			sum += textureProj(shadowMap, sc);
		}

		{
			vec4 sc = shadowCoords;
			sc.xy = shadowCoords.xy + offsets.zw;
			sc.z -= bias;
			sum += textureProj(shadowMap, sc);
		}
		 
	}
	float shadow = sum / float(samplesDiv2 * 2.0); 
	 
	if(shadow < 1.0 && shadow > 0)
	{
		for(int i = 0; i < samplesDiv2; i++)
		{
			offsetCoords.z = i;
			vec4 offsets = texelFetch(offsetTex, offsetCoords, 0) * radius * shadowCoords.w;
			
			{	
				vec4 sc = shadowCoords;
				sc.xy = shadowCoords.xy + offsets.xy;
				sc.z -= bias;
				sum += textureProj(shadowMap, sc);
			}

			{
				vec4 sc = shadowCoords;
				sc.xy = shadowCoords.xy + offsets.zw;
				sc.z -= bias;
				sum += textureProj(shadowMap, sc);
			}
			 
		}
		float shadow = sum / float(samplesDiv2 * 2.0); 
	}

	return shadow;
}
```

### **이렇게 예쁘게 만들었다!**

![](https://blog.kakaocdn.net/dna/L9J5G/btsL9oHIT5i/AAAAAAAAAAAAAAAAAAAAAOsy6O4iYKlE-CBz9aXiD1dZR5xdr85pBhN8Uygb3TpL/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hUTTRb1EicTEutHMgGe3txtLFlM%3D)![](https://blog.kakaocdn.net/dna/cQBWgn/btsL9sXE5Ph/AAAAAAAAAAAAAAAAAAAAALxexEXOOqvuovNiinBsejVSEtH285b6Hkwb8Lrr-S-g/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=kB0OgBiX00noqNQGz0QLNbQz2jM%3D)

![](https://blog.kakaocdn.net/dna/bddDw0/btsL9nWkQ5G/AAAAAAAAAAAAAAAAAAAAAPXwDLg0uUR1zKsIsi43sNzbIwZBRC-ke4gT6LTU-DT6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=lov4ZusM9NrGviKmtfJiVojZo3Y%3D)

구현하면서 고민하고 힘들었던 부분:

1.

bias중복으로 빼주는 실수

이 코드가 반복되는데 그럼 sc.z가 계속 줄어들고 있었다.

{}를 사용해서 bias가 중복으로 빠지지 않도록 수정했다.

```
		sc.xy = shadowCoords.xy + offsets.xy;
		sc.z -= bias;
 		sum += textureProj(shadowMap, sc);
```

이를 해결하니 노이즈가 조금은 줄었지만,, 여전히...

![](https://blog.kakaocdn.net/dna/Bkcin/btsL8ILWDMK/AAAAAAAAAAAAAAAAAAAAAOMUcaXOejcG-jrTuAWSdr7U61IhHu1BxQNVY-dZw73g/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GLROn1p1RjNmFDRj3QjmPRvVR%2Fw%3D)

![](https://blog.kakaocdn.net/dna/egTHaW/btsL9cMAKi4/AAAAAAAAAAAAAAAAAAAAAKprxr6sYkl6eIY1ePp7S8mfDGh2z3Q904TnhElsX6ep/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=cSNgof9WH4%2B4ECg0%2BQrF3e5xHTY%3D)

2.

샘플링할 부분을 랜덤으로 설정하면 무늬가 사라지지 않을까 해서 random으로 sampling을 해보니 노이즈가낀다...

k대신 random을 사용한 것인데 그러면 생기는 문제   
1번 디스크(원)의 바깥쪽부터 검사하지 못함. 2번 오히려 더 편향되게 생성될 수 있음

=> 탈락

```
x1 = k % (samplesU);
y1 = (samples - 1 - k) / samplesU;
x2 = (k + 1) % samplesU;
y2 = (samples - 1 - k - 1) / samplesU;
```

![](https://blog.kakaocdn.net/dna/coI1M4/btsL9RB5MDT/AAAAAAAAAAAAAAAAAAAAAEMUPpzcDen6yFIUvyjUjYOprcqO3DA4SZ5cwLLywCab/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=QJ0TWLfFB7Il8TCjAyYsPY9nKeU%3D)

.

3.

중간 중간 흰색으로 칠해진 픽셀이 존재, jittering 과정에서 그림자 바깥부분만 sampling하는 부분이 존재한다고 생각했습니다.

그래서 pos,neg 버전의 jittering을 사용해서 반드시 기준 pixel의 좌상단, 우상단, 좌하단, 우하단을 sampling하도록 변경하면 noise가 줄어들지 않을까 가설을 세웠습니다..!

총 8개의 데이터를 이용했습니다. 모든 방향으로 jittering해주고 렌더링을 해보니

```
	// Center on grid and jitter
	v1.x = (x1 + 0.5f) + posJitter();
	v1.y = (y1 + 0.5f) + posJitter();

	v1.z = (x2 + 0.5f) + negJitter();
	v1.w = (y2 + 0.5f) + negJitter();
	
  	v2.x = (x1 + 0.5f) + posJitter();
	v2.y = (y1 + 0.5f) + negJitter();
	
  	v2.z = (x2 + 0.5f) + negJitter();
	v2.w = (y2 + 0.5f) + posJitter();
```

예쁘게 생긴 똥이 나왔습니다...

=> 탈락

![](https://blog.kakaocdn.net/dna/tSYIJ/btsL9n2Z33P/AAAAAAAAAAAAAAAAAAAAAHiN7Fy3Q-sgwf-2uGNHpJOyoRYqSg3Jq3TQ-96k56ws/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=038fzDrbSh2nxagRglTgVQhYpG4%3D)![](https://blog.kakaocdn.net/dna/pbbDt/btsL9bu8H0n/AAAAAAAAAAAAAAAAAAAAALpFBu9Tlben6wTM39Yx7CnZGD-wE5nCJNfFe0k6BHsx/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KH%2B6s5EUbHboImFGQp8BWVN8VbI%3D)

  


\

근데 색을 입히니까 또 괜찮아보인다!!! 네.. 그렇습니다.. 넘어갈게요

![](https://blog.kakaocdn.net/dna/vOdFo/btsMa7EHT8W/AAAAAAAAAAAAAAAAAAAAAPPjgg1Lo8MdYaO9X8Iz85S03lfiO4b7S6-baAxoOLWT/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hV6767IAQXibj6ygK2%2BXtOH4LgI%3D)

4.

이거를 통해 해결했고, 그냥 코드 이슈? 였습니다.

큰 실수인데,,

shader에서 edge인것이 검출됐을 때 sampling하는 for문이 작동이 안되고 있었다.

( for문 범위 이슈,,, 교재와 내 코드가 살짝 달라서 생긴 이슈입니다...)

이를 조정하니 예쁘게 나왔습니다 ^^

![](https://blog.kakaocdn.net/dna/L9J5G/btsL9oHIT5i/AAAAAAAAAAAAAAAAAAAAAOsy6O4iYKlE-CBz9aXiD1dZR5xdr85pBhN8Uygb3TpL/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hUTTRb1EicTEutHMgGe3txtLFlM%3D)![](https://blog.kakaocdn.net/dna/cQBWgn/btsL9sXE5Ph/AAAAAAAAAAAAAAAAAAAAALxexEXOOqvuovNiinBsejVSEtH285b6Hkwb8Lrr-S-g/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=kB0OgBiX00noqNQGz0QLNbQz2jM%3D)

![](https://blog.kakaocdn.net/dna/bddDw0/btsL9nWkQ5G/AAAAAAAAAAAAAAAAAAAAAPXwDLg0uUR1zKsIsi43sNzbIwZBRC-ke4gT6LTU-DT6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=lov4ZusM9NrGviKmtfJiVojZo3Y%3D)