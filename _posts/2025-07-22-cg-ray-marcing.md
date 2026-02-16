---
title: "[CG] Ray Marcing"
date: 2025-07-22
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

<https://www.youtube.com/watch?v=BNZtUB7yhX4&t=2s>



<https://www.youtube.com/watch?v=S8AWd66hoCo&t=1788s>



<https://jamie-wong.com/2016/07/15/ray-marching-signed-distance-functions/>

[Ray Marching and Signed Distance Functions

One of the techniques used in many demo scenes is called ray marching. This algorithm, used in combination with a special kind of function called

jamie-wong.com](https://jamie-wong.com/2016/07/15/ray-marching-signed-distance-functions/)

Ray marching을 설명하고 실습을 해봅시다.(사실 봐봅시다가 맞음, 실습하시려면 링크타고 가시면 됩니다!)

우선 렌더링 과정을 잘 모르고 계신다면,

Ray Marching은 뭐야!! 라는 질문하실 것이고,

렌더링 과정을 알고 계시다면, 드는 첫 질문은 왜 ray marching을 써? 일 것입니다.

### 1. ray marching이 뭔데?

ray 광선, marching 행진

행진하는 광선입니다..!

내가 가고 싶은 방향이 있을 때, 앞의 물체들과 충돌처리를 하면서 앞으로 나아가는 방법입니다.

엉 충돌처리는 어떻게 하는데??

아래의 그림과 같이 a->b-c->d 이렇게 전진합니다!

![](https://blog.kakaocdn.net/dna/Xxbxp/btsPooyeJjR/AAAAAAAAAAAAAAAAAAAAAPAJiTBjqX98UyQXij10GaKymcEw92bigp_T4ECp0wNX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=CuTy2LTPUW7qyCDkZy3axDA%2B%2FaA%3D)

## 2. 왜 Ray Marching을 사용하는데?

프랙탈 구조를 한 번씩 들어봤을 것이다. 만약 프랙탈 구조를 렌더링하고 싶으면 어떻게 해야될까?

![](https://blog.kakaocdn.net/dna/SHNUa/btsPssFNyFM/AAAAAAAAAAAAAAAAAAAAAOtL0Ol4uX-2U1x8q1LEsxQO0z_z6W4eubBqce-4U4iQ/img.jpg?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=sNWHHlOHcAP7ahd3DDXYZshmzVk%3D)

우리가 일반적으로 알고 있는 방법은 폴리곤을 만들어서 렌더링하는 것이다.

무한대의 프랙탈을 만들려면 일단은 불가능이고, 흉내내려고만 해도 엄청난 용량을 잡아 먹을 것이다.

하지만 이런 정보 없이 렌더링을 해보자는 것이다.

이때 사용되는 방법이 Ray Marching 이다. ( signed distance function을 곁들인... )

SDF를 먼저 설명해보겠다.

### SDF(signed distance function)

반환 값의 보호는 해당 점이 표면 내부에 있는 지, 외부에 있는 지를 나타낸다.

반지름이 1인 구로 예를 들면 이럴 것이다.

![](https://blog.kakaocdn.net/dna/cF5bM4/btsPrbrspcy/AAAAAAAAAAAAAAAAAAAAAJS5JxAmr2MhxN-Oje3qqjlWFuJu-4Pe7uBbEz6ykZ-o/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=2Ndfgf3bojUsDHJRY9uL%2BEaTiEE%3D)
![](https://blog.kakaocdn.net/dna/b3h8L8/btsPs0B0EzR/AAAAAAAAAAAAAAAAAAAAAPDKo4_Ac7e6rmI7q2j7zV_eKQBKcqlvzMBtPp0QcetX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=i7wqXGnQ62EFjHseRi%2FJa02jQ%2Bw%3D)

음수면 구의 내부일 것이고, 양수면 구의 외부일 것이다.

이것을 GLSL 코드로 한다면

![](https://blog.kakaocdn.net/dna/b9M5pZ/btsPrhyFHJF/AAAAAAAAAAAAAAAAAAAAANNAgANknDf38MyJSrVdlBN_1V0gSog-VYYV4DtYzq6K/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=vDTujbEGRtg15XZaTEpSd0nwXhc%3D)

이렇게 될 것이다.

## Ray Marching Algorithm

SDF로 모델링 한 이후에 사용되는 렌더링 알고리즘이 ray marching이다.

Ray Tracing은 삼각형, 구 같은 기하 도형으로 장면을 구성하고, 각각의 도형과 광선이 교차하는지를 모두 테스트 해봐야한다. (AABB, BVH와 같은 구조로 최적화 가능)

반면 Ray Marching은 장면을 SDF(거리 함수)로 정의하고, 현재 위치에서 표면까지의 거리를 계산해 한 번에 이동하기 때문에 훨씬 적은 비용으로 충돌 여부를 판단할 수 있습니다.

```
if( 어딘가 닿음 (dist < EPSILON) ) return depth;

depth += dist;

if( 어디도 부딪히지 않고, 최대거리에 도착 ) return end;
```

![](https://blog.kakaocdn.net/dna/dRhngt/btsPqy1P003/AAAAAAAAAAAAAAAAAAAAAAH-LU1EnHNdKUgQ5NLkYKb0Fn2WPpcijM4lE37I7pgW/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=HnCydEnCkWnhh9vnoxMBznRB0mM%3D)

이렇게 하면 구를 그릴 수 있습니다.<https://www.shadertoy.com/view/llt3R4>

[Shadertoy

0.00 00.0 fps 0 x 0

www.shadertoy.com](https://www.shadertoy.com/view/llt3R4)

![](https://blog.kakaocdn.net/dna/dae36P/btsPrNqaFUe/AAAAAAAAAAAAAAAAAAAAABjETXJqkUfbt_TKS3KSy_s3qMbBKXC2hPGeWcxogFrB/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=tiaw9L%2FD3utxHNPRJBKhsn%2Bpj30%3D)

에ㅔ게게?

이게 뭐야 라고 할 수 있지만, phong shading을 더해주면

![](https://blog.kakaocdn.net/dna/cpK5iy/btsPsRejNfS/AAAAAAAAAAAAAAAAAAAAABYwyn7TGdsE_rFsnL-KTiZhiQ4yxyTWE2bKpcWP95ia/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=eWTJ5yiNyLfMLbQjq2a0iPmGOhg%3D)

이렇게 계속 그럴싸하게 쌓아갈 수 있다.

아래의 코드와 같이 경계에 부딪히기 직전, 직후 값들을 사용해서 normal을 유추할 수 있고, 이를 통해 여러 효과를 만들 수 있다.

```
vec3 estimateNormal(vec3 p) {
    return normalize(vec3(
        sceneSDF(vec3(p.x + EPSILON, p.y, p.z)) - sceneSDF(vec3(p.x - EPSILON, p.y, p.z)),
        sceneSDF(vec3(p.x, p.y + EPSILON, p.z)) - sceneSDF(vec3(p.x, p.y - EPSILON, p.z)),
        sceneSDF(vec3(p.x, p.y, p.z  + EPSILON)) - sceneSDF(vec3(p.x, p.y, p.z - EPSILON))
    ));
}
```

<https://www.shadertoy.com/view/lt33z7>

[Shadertoy

0.00 00.0 fps 0 x 0

www.shadertoy.com](https://www.shadertoy.com/view/lt33z7)

아래의 그림 처럼 조합하면 저런 도형도 얻을 수 있다.

이제는 수식 싸움이다.

![](https://blog.kakaocdn.net/dna/bg1qfF/btsPr5xACXl/AAAAAAAAAAAAAAAAAAAAALuZNCz4s2q_lakWNlXV0CT9B9w91J1ooIKcebhBOwrH/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=SKRRWQv4QZx71jfENClYhXYko90%3D)