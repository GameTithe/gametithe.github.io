---
title: "[실습 저장소] Projected Texture(+alpha blending)"
date: 2025-01-21
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **Projected Texture**

주요 내용은 프로젝터(카메라)가 하나 더 있다고 생각하고, 프로젝터가 보는 곳을 하나의 이미지라고 생각합니다...   
그리고 그 이미지 위에  내가 새로운 이미지를 쏴주는 겁니다. 빔프로젝터처럼

카메라 위치에서 살짝 왼쪽에 있는 프로젝터입니다. 대부분 카메라와 비슷하게 셋팅을 해주는데 하나 이상한(?)짓을 합니다.

translate(0.5f) \* scale(0.5f)를 해주는 것입니다. 그 이유는 오브젝트에 projection matrix까지 곱해졌다면 vertex의 위치 값은 [-1, 1]입니다. 하지만 이미지 좌표계는 [0,1]이기 때문에 normalize를 해주는 것입니다.

그리고 여기서 얻은 좌표를 texture 좌표로 써서 이미지를 읽어들이는 것입니다.

```
//projectorMatrix 
vec3 projPos = camera.Position + vec3(-0.2f, 0, 0.2f); 
vec3 projAt = camera.Orientation;
vec3 projUp = camera.Up;

mat4 projView = glm::lookAt(projPos, projPos + projAt, projUp);
mat4 projProj = glm::perspective(glm::radians(30.0f), 1.0f, 0.1f, 100.0f);
//normalization
mat4 projScaleTrans = glm::translate(vec3(0.5f)) *
	glm::scale(vec3(0.5f));
mat4 m = projScaleTrans * projProj * projView;

// Set the uniform variable
SetMatrixUniform(shaderProgram, "projectorMatrix", m);
```

```
	vec4 projTexColor = vec4(0.0);
	if( ProjTexCoord.z > 0.0 )
		projTexColor = textureProj(tex1,ProjTexCoord);
```

![](https://blog.kakaocdn.net/dna/W480U/btsLUtIGt3M/AAAAAAAAAAAAAAAAAAAAAKS4LHQNSV86TyWHXAGskRfcL5WMM_afP_D6_HokLf58/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=CjJA8%2Fr2Q2qJNr4uR3ep0duTCDU%3D)

### 

### **Discard**

**사실 이건 너무 간단합니다. alpha 값을 비교문으로 사용해서 discard(); 를 붙여주면 끝납니다.**

**discard는 return null;로 생각하면 편할 것 같습니다.**

![](https://blog.kakaocdn.net/dna/nzsuJ/btsLUsbYEox/AAAAAAAAAAAAAAAAAAAAAAJtEhi4r6n8A1e0OBz3tw-t9eyTWClN3yTbYUEbHnAw/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=5bm0m%2FFpw0tHRaFNFTQy%2BxrkZXU%3D)


![](https://blog.kakaocdn.net/dna/bYWo3w/btsLUjTQ0K6/AAAAAAAAAAAAAAAAAAAAALzo1_DY-vlXad5zufS9faHJXhT0643YCrulirmhGwuD/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FJP7fO5WifJlRbvYmp9J0SppGOE%3D)![](https://blog.kakaocdn.net/dna/byEQ9I/btsLVCEDfp0/AAAAAAAAAAAAAAAAAAAAAJFgQGoZv3nAaf45sA6uv0Kl7G8Bta7tFJ1nvpiixIeK/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=32AgcxtOI0uMK3p174wz13hL9WE%3D)