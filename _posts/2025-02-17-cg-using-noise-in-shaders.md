---
title: "[CG] Using Noise in Shaders"
date: 2025-02-17
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

시뮬레이션을 할 때 불완전한(imperfection) 물체를 렌더링할 때 랜덤한 변수를 사용합니다.

하지만 pseudorandom로 난수를 생성하는 것은 효율적이지 못합니다.

1. 랜덤하지만 반복적인 데이터가 필요합니다.

(we need data that is repeatable, so that the object will render in the same way during each frame of the animation.)

2. 연속적으로 변하면서 랜덤한 데이터가 필요합니다.

(we actually need data that is continuous, but still gives the appearance of randomness.)

Perlin이 획기적인 아이디어로 Perlin Noise를 만들었습니다.

gradient noise 종류이다.

Perlin Noise는

1. 연속 함수이다.  
2. 반복 가능하다. (동일한 입력에서 동일한 출력을 생성합니다)  
3. 차원 수에 관계없이 정의할 수 있다.  
4.  규칙적인 패턴이 없고 무작위로 보인다.

실선이 noise texture의 범위이다.

![](https://blog.kakaocdn.net/dna/bBWEGn/btsMaRcAPYF/AAAAAAAAAAAAAAAAAAAAAMhaL0dNoNqL9MHyeuYjxDE2iWYjCygL6dRvxJy8B7cJ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=vc3nhrD97jODgPnS28DvKR9wpW0%3D)

When A is close to the lower-left corner of the texture boundary, the value is strongly influenced by the value at B, C, and D

나는 libnoise를 이용해서 perlin noise를 만들어주고 사용했다. 근데 공식 홈페이지의 .lib파일이 x84기준으로 만들어진 것으로 추정된다...

![](https://blog.kakaocdn.net/dna/bYTB10/btsMbvUrJtn/AAAAAAAAAAAAAAAAAAAAAEHIztoow_yUjD2d_6w3ZUDuBHOiseDcX2dcTGq-3XKX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Er792KBOlgHTECbB9e0qLrh1bGU%3D)

아래 링크에 들어가서 x64기준 lib파일을 사용해주면 정삭적으로 작동이된다!

<https://github.com/eldernos/LibNoise64>

[GitHub - eldernos/LibNoise64: LibNoise library built for x64 applications ready for use in Unreal Engine 4 games.

LibNoise library built for x64 applications ready for use in Unreal Engine 4 games. - eldernos/LibNoise64

github.com](https://github.com/eldernos/LibNoise64)

간단한 실습:

### **구름... (근데 가짜인게 티가나는)**

파란색 부분이 노이즈라고 생각하면 될 것 같습니다.

noise.r, g, b, a는 서로 다른 옥타브의 노이즈가 들어있습니다.

g를 사용하는 것은 큰 의미는 없습니다.

1. noise.g => [0,1]

2. ( cos(noise.g \* PI ) + 1.0 ) / 2.0 => [0,1]

범위가 동일해서 1번이나 2번이나 크게 다르지 않지만, 2번이 조금 더 부드럽게 표현해준다고 한다.

```
void main() 
{
	vec4 noise = texture(noiseTex1, texCoord);
	
	vec4 skyColor = vec4( 0.3, 0.3, 0.9, 1.0 );
	vec4 cloudColor = vec4(1.0, 1.0, 1.0, 1.0);

	// Reson why using g, we use 2 octave
	//float t = ( cos(noise.g * PI) + 1.0) / 2.0;
	float t = noise.g;

	vec4 color = mix(skyColor, cloudColor, t);

	FragColor = vec4(color.rgb, 1.0);
}
```

![](https://blog.kakaocdn.net/dna/eoYDBl/btsMmfWCBH3/AAAAAAAAAAAAAAAAAAAAAKrnzLlXK87Jfe-6xShaW_pkg8um4y_mIZD48B_Ztmnk/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=SYqL67n1YH7pzYl13duJoDdBC5M%3D)![](https://blog.kakaocdn.net/dna/GpIWp/btsMlC5OBfW/AAAAAAAAAAAAAAAAAAAAAOTMYMUFg9q1r2llCW01_5nWUDmtLPQI5a_VN-W_-h5t/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FFeUtbYy%2BEYgtqfE0BSEbOaKGZs%3D)

### **야간 투시경**

skybox에도 적용시키면 더 그럴싸하겠지만,,, 여기까지만 ㅎㅎ

![](https://blog.kakaocdn.net/dna/cdO0XF/btsMmeJ93ab/AAAAAAAAAAAAAAAAAAAAADNzfBrZ7_c7naimlxIjkYVAx6H5CIoPNa50vmcGEe8K/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=l7aRvcDckCZPAiVtpvjRhYAZp6c%3D)![](https://blog.kakaocdn.net/dna/bYhPbp/btsMkCFv1Wo/AAAAAAAAAAAAAAAAAAAAAB6p6qZa0flSa0Pq40YsiiKAVyezRR-Rogm2kmWsgkxz/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=iv1n18z3hvE4I0SuqQ1PaPoIpxc%3D)