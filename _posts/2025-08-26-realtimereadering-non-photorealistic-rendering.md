---
title: "[RealTimeReadering] Non-Photorealistic Rendering"
date: 2025-08-26
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

렌더링에 대해서 공부하다가 NPR을 크래프톤 테크랩에서 구현해보고 싶어서, 이론을 먼저 학습해보려고한다.

### 

### **Non-Photorealistic Rendering**

Photorealistic rendering은 이미지를 실제 사진과 구분할 수 없도록 만드는 것을 목표로 한다.

Non-photorealistic rendering(or stylized rendering)은 일러스트와 유사한 이미지를 만드는 것을 목표로 한다.

![](https://blog.kakaocdn.net/dna/dAMZsw/btsP4ysTRS2/AAAAAAAAAAAAAAAAAAAAAEX_FCCaXGZ6RfPPNYpToCPrbPQag9Jvt2XNHVPYLJZn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=uicB%2Bj83eFXwDVVCTD0%2B1f6CrIk%3D)

NPR분야는 매우 방대하 하며, 위의 그림과 같이 다양한 알고리즘으로 다양한 질감을 표현할 수 있다.

여기서는 실시간 NPR에서 사용되는 스트로크(strokes)와 선(line)을 렌더링하는 기법에 집중하겠다.

NPR에 쓰이는 몇 가지 알고리즘을 맛보는 수준이다.

cartoon rendering을 구현하기 위한 논의로 시작해서, 다양항 line rendering 기법으로 마무리할 것이다.

### 

### **Toon Shading**

Toon shading의 가장 단순한 형태로는, 물체를 서로 다른 단색 영역으로 구분하고 이들을 실선으로 구획하여 그린다.

(이 부분은 괸장히 단순하고, 학부 때 구현해본 경험이있다.)

<https://tithingbygame.tistory.com/127>

[[실습저장소] Cartoon Rendering(Non-Photorealistic Rendering)

이론 : https://tithingbygame.tistory.com/128

tithingbygame.tistory.com](https://tithingbygame.tistory.com/127)

Toon rendering은 다른 NPR 스타일에 비해 정의가 명확하고 구현이 쉽기 때문에 컴퓨터에 의한 자동 생성에 적합하다. 실제로 많은 비디오 게임에서 효과적으로 사용되었다.

![](https://blog.kakaocdn.net/dna/bRU2vE/btsP5gywdkP/AAAAAAAAAAAAAAAAAAAAADVcDGPEXbYcVlh2T7q5pmHb51skyz5cEOanoa1p0Q2N/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=RMQ5B3JpW6q1%2B5BSLFFd3mmF3qg%3D)

okami라는 게임에도 사용했다고 한다.

물체의 외곽선은 종종 검은색으로 렌더링되는데, 이는 만화풍을 더욱 강화하는 역할을 한다. (외곽선을 찾고 렌더링하는 방법은 이후에 다룰 예정이다.)

툰 표면 셰이딩에는 여러 접근법이 있는데, 가장 일반적인 두 가지 방법은 다음과 같다:

**1. 메시 영역을 단색(조명 없음)으로 채우는 방법**

**2. two-tone 방식** 밝은 부분과 그림자 부분을 구분하는 방식

two tone 방식은 흔히 hard shading이라고 불린다.

픽셀 셰이더에서 단순히 법선 벡터와 광원 방향의 내적(dot product)이 어떤 임계값 이상이면 밝은 색을, 그렇지 않으면 어두운 색을 사용하는 방식으로 쉽게 구현된다.

조명이 더 복잡할 경우에는 최종 이미지에서 연속적인 값을 소수의 톤으로 변환하여 각 톤 사이에 뚜렷한 경계를 만드는 방식도 존재한다. => quantization(양자화), posterization으로 부른다.

(위에서 공유한, 내가 구현한 방식이 quatization을 방식이다.)

![](https://blog.kakaocdn.net/dna/IVAje/btsP4oK02Bm/AAAAAAAAAAAAAAAAAAAAAM2bi3SUsoV5m0qbH0IPzpL299d8rh1IcJILcv3zPD82/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=5tE0qexr%2BOxnrFNEvQzTU4GrDPk%3D)

RGB 값을 직접 양자화하면, 각 채널이 서로 다른 방식으로 변화하기 때문에 원치 않는 색조 변화(hue shift)가 발생할 수 있다.

(내가 원하는 색감이 나타나지 않고, 단색으로 덮어씌어지는...)

따라서 **HSV, HSL, Y’CbCr**와 **같은 색상 보존(hue-preserving) 색 공간에서 작업하는 것이 더 적합하다. (밝기나 채도를 양자화하면 색조는 유지할 수 있다.)**

또 다른 대안으로는, 1차원 함수나 텍스처를 정의하여 밝기(intensity) 값을 특정 색상 또는 음영으로 재매핑하는 방법이 있다. 텍스처는 사전에 양자화나 다른 필터를 적용해 전처리할 수도 있다.

![](https://blog.kakaocdn.net/dna/yZwmv/btsP4zrMjPN/AAAAAAAAAAAAAAAAAAAAAComuqU7-YupYQkG8cciiYiurj6PDEeV9jL0bseruRdf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=XWGUievUXp74YHCiONuJd72tK%2BQ%3D)

Team Fortress2

이 알고리즘은 다양한 셰이딩 방정식과 페인팅된 텍스처들과 결합되어, 게임 **Team Fortress 2**에서 만화풍과 사실적 스타일이 혼합된 독특한 시각 효과를 구현하는 데 사용되었다.

툰 셰이더의 변형은 다른 목적으로도 사용될 수 있는데, 예를 들어 표면이나 지형의 특징을 시각화할 때 대비를 과장하는 용도로 활용되기도 한다.

### 

### **Outline Rendering**

cel edge rendering에 사용되는 알고리즘들은 NPR의 주요 기법들을 반영한다.

여기서 우리의 목표는 이 분야의 느낌을 전달할 수 있는 알고리즘들을 제시하는 것이다. 사용되는 방법은 대략적으로 표면 셰이딩, 절차적 기하, 영상 처리, 기하학적 에지 검출, 혹은 이들의 혼합 기반으로 분류할 수 있다.

툰 렌더링에서 사용할 수 있는 여러 종류의 에지가 존재한다.

**boundary(경계) edge**

두 삼각형이 공유하지 않는 edge이다. 예를 들어, 종이 한 장의 가장자리 같은 경우이다. solid object는 일반적으로 경계 에지를 갖지 않는다.

**crease(or hard or feature) edge**

두 삼각형이 공유하는 에지인데, 두 삼각형 사이의 각도(이면각, dihedral angle)가 어떤 미리 정의된 값보다 클 때이다. 좋은 기본 크리스 각도 값은 60도이다 [972]. 예를 들어, 큐브는 크리스 에지를 갖는다. 크리스 에지는 더 세분화하여 능선(ridge)과 계곡(valley) 에지로 나눌 수 있다.

**material edge**

공유하는 두 삼각형이 재질에서 다르거나 그 외에 셰이딩에서 변화를 일으킬 때 나타난다. 또한 아티스트가 항상 표시되기를 원하는 에지가 될 수도 있다. 예를 들어, 이마 주름선이나 같은 색의 바지와 셔츠를 구분하기 위한 선 같은 경우이다.

**contour edge**

두 이웃 삼각형이 어떤 방향 벡터(보통 눈으로부터 오는 벡터)에 대해 서로 다른 방향을 향할 때 생긴다.

**silhouette edge**

객체의 외곽을 따라 있는 윤곽 에지로, 즉 이미지 평면에서 객체를 배경으로부터 분리하는 역할을 한다.

![](https://blog.kakaocdn.net/dna/kYFOL/btsP5t5Qu6h/AAAAAAAAAAAAAAAAAAAAAA6_eGkhzaS9b0AnzcfPlNSFWM0HCFMRQJmGBo7IalLV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=SRntYjiSM3LSc0tYWGhAygNK0Sk%3D)

그림 15.4를 보라. 이 분류는 문헌에서의 일반적인 사용에 기초한 것이지만, 몇 가지 변형도 존재한다. 예를 들어, 우리가 크리스 에지와 재질 에지라고 부르는 것이 다른 곳에서는 경계 에지라고 불리기도 한다.

![](https://blog.kakaocdn.net/dna/nzPva/btsP4FZ3MwT/AAAAAAAAAAAAAAAAAAAAAAXmiBbY0FDJFb8lBxrRJkh4vxt1Vhcmt987ezbQdWwK/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=8rKsQJr%2FlmQQMetxLeC0Xp0pfJo%3D)

silhouette => contour => suggestive contour

여기서는 contour(윤곽)과 silhouette(실루엣) edge를 구분한다.

두 경우 모두 한 부분의 표면은 camera(우리의 시점)를 향하고 다른 부분은 반대 방향을 향한다. silhouette edge는 contour edge의 부분집합으로, 객체를 다른 객체나 배경으로부터 분리하는 것이다.\

경계(boundary) 에지는 윤곽(contour)이나 실루엣(silhouette) 에지와 같지 않다는 점에 유의해야 한다.

윤곽과 실루엣 에지는 뷰 방향에 의해 정의되지만, 경계 에지는 뷰와 무관하다.

제안적 윤곽선(suggestive contours) 원래의 뷰포인트에서 거의 윤곽이 되는 위치에서 형성된다. 그것들은 객체의 형태를 전달하는 데 도움이 되는 추가적인 에지를 제공한다.

여기서는 주로 윤곽 에지를 검출하고 렌더링하는 데 초점을 맞추지만, 다른 종류의 스트로크에 대해서도 상당한 연구가 이루어져 왔다 [281, 1014, 1521]. 우리는 또한 주로 다각형 모델에서 이러한 에지를 찾는 방법에 집중한다. Bénard 등 [132]은 세분화 표면(subdivision surfaces)이나 다른 고차원 정의(higher-order definitions)로 구성된 모델의 윤곽을 찾는 접근법을 논의한다.

### 

### **Shading Normal Contour Edges**

### Shading Normal과 Direction to the eye 벡터 사이의 내적을 사용하여 contour(윤곽) edge를 얻을 수 있다.

### 이 값이 0에 가까우면, 표면이 눈에 거의 옆으로(edge-on) 보이는 것이므로 윤곽 에지 근처에 있을 가능성이 높다. 이러한 영역은 검은색으로 칠하고, 내적 값이 증가할수록 흰색으로 서서히 전환되도록 한다.

![](https://blog.kakaocdn.net/dna/dDCIMH/btsP7dU8fgM/AAAAAAAAAAAAAAAAAAAAAKNmeNkmWbJ8U7s049NywUOWYVkvBF-j1XQA2mi33o2Q/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hIi%2F2I2IFKN%2FsEP%2BP0JVe7mg9QQ%3D)

이 방법의 특징 혹은 단점은, 윤곽선이 표면의 곡률에 따라 가변적인 두께로 그려진다는 점이다. 이 방법은 crease edge(두 삼각형이 공유하는 에지)가 없는 곡면 모델에서 잘 작동한다.

실루엣을 따라 있는 영역에서는 보통 노멀 벡터가 뷰 방향에 거의 수직을 이루는 성질을 이용해서 구현하는데, 큐브 값은 모델(crease edge를 갖는)은 이런 특성이 없기 때문에 이 알고리즘을 사용하기 어렵다.

또한 곡면 모델에서도, 객체가 멀리 있거나 윤곽선 근처의 일부 노멀들이 뷰 방향에 거의 수직이 아닐 경우, 끊어지거나 보기 좋지 않게 나타날 수 있기 때문에 조명, 곡률, 거리 등을 결합하여 스트로크의 두께를 결정하는 방법을 고려해야된다.

### 

### Procedural Geometry Silhouetting

실시간 윤곽선 렌더링을 위한 일반적인 아이디어는 전면 폴리곤(frontfaces)을 정상적으로 렌더링한 후, 후면 폴리곤(backfaces)을 그들의 윤곽 에지가 보이도록 렌더링하는 것이다. 이러한 후면 폴리곤을 렌더링하는 방법에는 다양한 방식이 있으며, 각각의 장단점이 있다.

각 방법의 첫 단계는 전면 폴리곤을 그리는 것이다.

그 다음, frontface culling을 켜고 후면 backface culling을 끄면, 오직 후면 폴리곤만이 렌더링된다.

이렇게 얻은 back face를 이용하면된다. biasig이나 기타 방법을 사용해서 back face를 translate를 시키고, front face를 그리면 edge를 그릴 수 있는 것이다.

![](https://blog.kakaocdn.net/dna/cXfRs7/btsP5pPZJK1/AAAAAAAAAAAAAAAAAAAAAClS3mq4qIsWN9hGsx9SKmjN9eI2dVBykBOVguAVOI1n/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=PhtGy6d9OunmiazcP8AGN7ujn9I%3D)

이 선들을 더 두껍게 만드는 한 가지 방법은 후면 폴리곤 자체를 검은색으로 렌더링하면 된다.

이 때도 back face를 앞으로 biasing하면 된다.

biasing을 조절하기 위해서는 고정된 양만큼 변환, z-깊이(z-depth)의 비선형적 성질을 보정하는 양만큼 변환, 투영 행렬을 수정하여 더 세밀한 깊이 제어하는 등 여러가지 방법이 존재한다.

![](https://blog.kakaocdn.net/dna/bhTCDa/btsP7coyKRl/AAAAAAAAAAAAAAAAAAAAAJdpOu1sxu2VvQnDuvMWA84ph-rLOD9IRF6sq70pr2wc/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=VOAeH0RTfbdOGVzlrqLLhTSh%2BiQ%3D)

이러한 모든 방법들의 문제는 **균일한 두께의 선을 생성하지 못한다**는 점이다. 그렇게 하려면, 앞으로 이동하는 양이 후면 폴리곤뿐만 아니라 이웃하는 전면 폴리곤에도 의존해야 한다. 후면 폴리곤의 기울기를 사용하여 폴리곤을 앞으로 바이어스할 수 있지만, 선의 두께는 또한 전면 폴리곤의 각도에도 의존하게 된다. (front face의 기울기에 따라서 보여지는 edge의 두께가 상의하다.)

![](https://blog.kakaocdn.net/dna/csHXDZ/btsP45Ejt4H/AAAAAAAAAAAAAAAAAAAAAKZPwd8lzBaDsBcGf7jKb1CSPqsy7Vp9r9fdxmnHs_92/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ru5%2Bfc2rROFEoiFmJAOl2k52RNE%3D)

Raskar와 Cohen은 각 후면 삼각형을 보이는 선의 두께가 일관되게 유지되도록 필요한 양만큼 **에지를 따라(out along its edges)** 두껍게 만드는(fattening) 방식으로 이 이웃 의존성 문제를 해결했다. 즉, 삼각형의 기울기와 뷰어로부터의 거리가 삼각형이 얼마나 확장될지를 결정한다.

한 가지 방법은 각 삼각형의 세 꼭짓점을 그 평면을 따라 바깥쪽으로 확장하는 것이다. 삼각형을 렌더링하는 더 안전한 방법은 삼각형의 각 에지를 바깥쪽으로 이동시키고 에지들을 연결하는 것이다. 이렇게 하면 꼭짓점이 원래 삼각형에서 멀리 떨어져 나가는 것을 피할 수 있다. 그림 15.8을 보라. 이 방법은 전면 폴리곤의 에지 너머로 후면 폴리곤이 확장되기 때문에 바이어싱이 필요 없다. 세 가지 방법의 결과는 그림 15.9를 보라. 이 fattening 기법은 더 제어 가능하고 일관적이며, Prince of Persia [1138]와 Afro Samurai [250]와 같은 비디오 게임에서 캐릭터 외곽선 표현에 성공적으로 사용되었다.

(thin triangle은 왼쪽 그림의 오른쪽 꼭지점 부분 처럼, 실루엣이 무너질 수 있다. 오른쪽 그림처럼 모서리 각을 맞춰서 이 문제를 피할 수 있다.)

 

![](https://blog.kakaocdn.net/dna/HufPx/btsP6bDBBf6/AAAAAAAAAAAAAAAAAAAAAIDXtmB0Iz4-tqHdK4Cj69i_po0ozhb6EO2OyBZ3I8sf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=P4anik2AYciIMTnXKyAg1czm4U4%3D)

또 다른 방법으로 Shell, Halo 방법이있다.

후면 삼각형들의 꼭짓점을 공유하는 꼭짓점 노멀을 따라 눈으로부터의 z-거리 비율에 따라 바깥쪽으로 이동시키는 것이다.

 

꼭짓점을 노멀을 따라 바깥쪽으로 이동시키는 것은 정점 셰이더(vertex shader)에게 딱 맞는 작업이다. 이러한 종류의 확장은 \*\*셸 매핑(shell mapping)\*\*이라고 불리기도 한다. 이 방법은 구현이 간단하고, 효율적이며, 강건하고, 일정한 성능을 제공한다.

![](https://blog.kakaocdn.net/dna/CqYRV/btsP4oLa17a/AAAAAAAAAAAAAAAAAAAAANzjSCscInMr-clt5ovlB0DETG2uPKdVmiA8h4pqJjRq/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=OM3VO%2FnlpbhLenjCZ%2FsmiIbTgLI%3D)

cell damage의 인게임 스크린샷

이러한 후면 폴리곤들을 각도에 따라 확장하고 셰이딩하면 포스필드(forcefield)나 헤일로 효과를 만들 수 있다.

![](https://blog.kakaocdn.net/dna/F6Fx9/btsP4sGk1W0/AAAAAAAAAAAAAAAAAAAAACueXRdBprUj-IbzekIBD_IXO7ICdU2tPDIivt_8UEM7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=zXdhaiCpULY0TchzeguQsxd9yGg%3D)

이 셸 기법에는 몇 가지 잠재적 함정이 있다. 정면에서 큐브를 바라봐서 한 면만 보이는 상황을 상상해 보라. 윤곽선을 형성하는 네 개의 후면 폴리곤 각각은 그에 해당하는 큐브 면의 방향으로 이동하므로, 모서리에서 틈이 생기게 된다. 이는 각 모서리에 단일 꼭짓점이 존재하지만, 각 면이 서로 다른 꼭짓점 노멀을 갖고 있기 때문이다. 문제는 확장된 큐브가 진정한 셸을 형성하지 못한다는 점인데, 각 코너 꼭짓점이 다른 방향으로 확장되기 때문이다.

![](https://blog.kakaocdn.net/dna/9B9Q6/btsP56idhh0/AAAAAAAAAAAAAAAAAAAAAKVbQ1uOP2IWjLr_DVpuGq5Klx4gkfrqrZcFAFcSRWFI/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2Blv4T4IX2N%2FkwLmp62Y27tkMOP0%3D)

하나의 해결책은 동일한 위치에 있는 꼭짓점들이 단일한 새로운 평균 꼭짓점 노멀을 공유하도록 강제하는 것이다.

이 기하 기법 전체의 주목할 만한 특징은 렌더링 중에 연결성(connectivity) 정보나 에지 리스트가 필요 없다는 점이다. 각 삼각형은 다른 삼각형과 독립적으로 처리되므로, 이러한 기법들은 GPU 구현에 적합하다.

### 

### **Edge Detection by Image Processing**

또 다른 유형의 알고리즘은 이미지 기반인데, 이는 이미지 버퍼에 저장된 데이터만을 전적으로 다루며 장면의 geometry를 수정하지 (혹은 직접 알지도) 않는다.

Saito와 Takahash는 처음으로 이 G-버퍼 개념을 도입했으며, 이는 deferred shading에서도 사용된다.

Decaudin은 G-버퍼의 사용을 확장하여 툰 렌더링을 수행했다. 기본 아이디어는 간단하다.

NPR은 다양한 정보 버퍼에 대해 이미지 처리 알고리즘을 수행함으로써 가능하다. 많은 윤곽선 위치들은 인접한 z-버퍼 값들의 불연속성을 찾음으로써 발견될 수 있다.

불연속 속성이 무슨의미냐 하면!  
노멀 값을 확인했을 떄 주변 픽셀들과의 차이가 크다면 (불연속) contour, boundary edge 위치를 의미할 것이다.

scene의 ambient color, object identification value를 통해서, material, boundary, true silhouteee edge를 검사할 수 있을 것이다.

![](https://blog.kakaocdn.net/dna/rreQa/btsP6b4JiJ6/AAAAAAAAAAAAAAAAAAAAAAE8YsozeuaPlRFXJNa_iEIZA7pdqWc3WWPguwshgVjV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=FZebmZI%2B0JL%2FsRvVhUpWIFRm2Rg%3D)

sobel edge detection 사용된 예시

이렇게 에지를 검출하고 렌더링하는 것은 두 부분으로 구성된다.

우선, 장면의 geometry를 렌더링하면서, 픽셀 셰이더가 depth, 노멀, 객체 ID / 원하는 다른 데이터를 다양한 렌더 타깃에 저장한다.

그 다음, post-processing passes가 수행되는데, post-processing passes는 각 픽셀 주위의 이웃을 샘플링하고 이 샘플들에 기반하여 결과를 출력한다. (이웃을 샘플링하는 이유는 불연속성을 확인하기 위해서)

예를 들어, 장면의 각 객체에 대해 고유한 식별 값(객체ID와 같은)을 가지고 있다고 가정해보자.

각 픽셀에서 우리는 이 ID를 샘플링하고, 테스트 픽셀의 네 모서리 인접 픽셀들의 ID와 비교할 수 있다. 만약 주변 픽셀의 ID가 테스트 픽셀 ID와 다르면, 검은색을 출력하고, 그렇지 않으면 흰색을 출력한다.

이러한 간단한 테스트로 대부분의 boundary, outline edgees를 그리는 데 사용할 수 있다.

contour edge는 노멀과 depth 버퍼에 다양한 필터를 적용하여 찾을 수 있다.

예를 들어, 인접 픽셀 간의 깊이 차이가 어떤 임계값(threshold) 이상이면, contour edge가 존재할 가능성이 높으므로 해당 픽셀을 검정색으로 칠한다.

더 정교하게 검출하기 위해서는 Roberts cross, Sobel, Scharr 같은 edge detection filter가 존재하는데 여기서 다루지는 않겠다.

하지만 난 궁금하니까 찾아봐야겠다

더보기

**Sobel**: 가장 기본적인 edeg detection filter

수평/수직 방향의 밝기 변화를 중심으로 기울기를 계산한다.

```
Gx = [ -1  0  1 ]      Gy = [ -1 -2 -1 ]
     [ -2  0  2 ]           [  0  0  0 ]
     [ -1  0  1 ]           [  1  2  1 ]
```

**Scharr**

계산 비용은 Sobel과 비슷하지만 더 정밀하게 기울기를 계산한다.

```
Gx = [  -3   0   3 ]      Gy = [  -3  -10  -3 ]
     [ -10   0  10 ]           [   0    0   0 ]
     [  -3   0   3 ]           [   3   10   3 ]
```

노멀 버퍼 역시 crease edge를 검출할 수 있는데, 이는 노멀 간의 큰 차이가 contour edge(두개의 삼각형에서 눈으로 들어오는 벡터의 방향이 다른)든 crease edge(2개의 삼각형이 공유하는) 든 둘 중 하나를 의미할 수 있기 떄문이다.

dilation(팽창) operator는 검출된 edge를 두껍게 만드는 데 사용되는 morphological(형태학적) 연산자의 일종이다.

edge 이미지가 생성된 후, 별도의 패스를 적용한다.

각 픽셀에서, 픽셀 값과 일정 반경 내의 주변 값들이 검사하고, 가장 어두운 픽셀 값을 출력한다. 이렇게 해서, 얇은 검은 선은 탐색 영역의 지름만큼 두꺼워지게 된다. 여러 번의 패스를 적용하여 선을 더욱 두껍게 만들 수 있다

(알아두어야 할 점은 큰 kernel을 만들어서 한 번의 패스로 edge를 두껍게 만드는 것 보다, 작은 kernel을 만들어서 여러 번의 패스를 통과시키는게 비용적으로 더 싸다.)

이런 유형의 알고리즘에는 몇 가지 장점이 있다.

대부분 다른 기법들과 달리, 이미지 기반이기 때문에 평면이든 곡면이든 모든 종류의 표면을 처리할 수 있다. mesh는 연결되어 있을 필요도 없고, 일관될 필요도 없다.

![](https://blog.kakaocdn.net/dna/Uh3rf/btsP4zySYb3/AAAAAAAAAAAAAAAAAAAAAHWxMwy7fFglw7oDB9FLXE4oR6unPqyslGWKJ_ipuVx6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=v5SlkrE42Nq1HWmbWuhlIaGK1m4%3D)

왼쪽은 너무 적은 가중치, 오른쪽은 너무 큰 가중치로 인한 아티팩터 => edge 검출은 오차없이 가능한 작업은 아님

이러한 유형의 기법에는 오직 몇가지 문제만 존재하는데,

**1. edge-on(옆에서 본) 표면의 경우, z-깊이 비교 필터가 표면을 가로질러 잘못된 윤곽선 픽셀을 검출할 수 있다.**

z-깊이 비교의 또 다른 문제는, 차이가 미미하다면 윤곽 에지를 놓칠 수 있다는 점이다. 예를 들어, 책상 위의 종이 한 장은 보통 그 에지가 검출되지 않는다.

마찬가지로, 노멀 맵 필터 역시 이 종이의 에지를 놓치게 되는데, 이는 노멀 값이 동일하기 때문이다.

**2. edge detection은 오작동 할 수 있다.**

예를 들어, 얇은 원기둥으로 만들어진 장미 줄기를 상상해보자.

줌인을 많이해서 매우 가까이서 본다고 가정하면, 우리의 샘플 픽셀에 인접한 줄기 노멀들은 크게 변하지 않을 것이므로, 노멀 값 파차이로 인한 edge검출은 안될 것이다.

그러나 줄기에서 멀어질수록, 노멀은 픽셀마다 더 빠르게 변하게 될 것이고, 모서리 근처에서 잘못된 에지 검출이 발생할 수 있다.

깊이 맵에서 에지를 검출할 때도 비슷한 문제가 발생할 수 있는데, 여기에 perspective깊이에 미치는 효과도 추가적으로 보정해야 하는 요인이다.

**Decaudin은 단순히 값 자체를 처리하는 대신 노멀과 깊이 맵의 기울기(gradient)를 처리하여 변화를 찾는 개선된 방법을 제시했다.** 다양한 픽셀 차이가 어떻게 색상 변화로 번역되는지는 콘텐츠에 따라 조정되어야 하는 과정이다.

스트로크(이미지)가 생성된 후에는, 원하는 만큼 추가적인 영상 처리를 수행할 수 있다. 스트로크는 별도의 버퍼에서 생성될 수 있으므로, 그것들은 독립적으로 수정된 후 표면 위에 합성될 수 있다. 예를 들어, 노이즈 함수를 사용하여 선과 표면을 각각 풀리거나 흔들리게 만들어, 두 요소 사이에 작은 간격을 생성하고 손으로 그린 듯한 느낌을 줄 수 있다. 종이의 height field를 사용하여 렌더링에 영향을 주면, 아래와 같은 손 그림 느낌을 줄 있다.

![](https://blog.kakaocdn.net/dna/DBCRI/btsP7fezqtc/AAAAAAAAAAAAAAAAAAAAAFd8W89m7jT79bp2p9JElTWgVyGmkZuN-PM8T5AZlZ4r/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9JhqtVIfZg9ru8v8hg3zxA%2BTkac%3D)

우리는 여기서 노멀, 깊이, ID와 같은 기하학적 혹은 비-그래픽 데이터들을 사용하여 에지를 검출하는 데 초점을 맞췄다.

당연히, 영상 처리 기법은 원래 이미지들을 위해 개발되었으며, 이러한 에지 검출 기법들은 컬러 버퍼에도 적용될 수 있다. 한 가지 접근법은 Difference of Gaussians (DoG)라 불리는데, 이미지를 두 가지 다른 가우시안 필터로 두 번 처리한 다음 하나를 다른 하나에서 빼는 것이다.이 에지 검출 방법은 NPR에서 특히 만족스러운 결과를 내는 것으로 알려졌으며, 연필 그림, 파스텔 등 다양한 예술적 스타일의 이미지를 생성하는 데 사용된다.

=>나중에 DoG논문과 XDoG논문을 읽어봐야겠담..

## 

## Geomtry Contour Edge Detection

지금까지의 접근법에서의 문제점은, 가장 잘 해도 윤곽선의 stylization(스타일링)이 제한적이라는 점이다.

선을 점선처럼 보이게 한다거나, 손으로 그린 듯한 붓터치 느낌을 내기는 어렵다. 이런 작업을 하려면, 윤곽선을 직접 찾아내고 렌더링해야 한다.

별도의, 독립된 edge entities를 가지면, 메시가 정지한 상태에서 Contour Edge가 깜짝 놀라 뛰는 듯한 효과 같은 다른 표현도 가능하다.

contour edge이란, 인접한 두 삼각형 중 하나는 카메라를 향하고, 다른 하나는 카메라 반대 방향을 향할 때의 에지를 말한다.

이를 판별하는 식이다.

![](https://blog.kakaocdn.net/dna/x38Ec/btsP54SnJie/AAAAAAAAAAAAAAAAAAAAALdnSY2f5DmphgVoQAp96-cxKvd8lBIuTIbA0yThpJL-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=7IDVvBAf6zZUn38W%2FTZVA9S3txk%3D)

여기서 n0과 n1은 두 삼각형의 법선이고, v는 카메라에서 edge로 향하는 방향 벡터다.

모델에서 윤곽선을 찾는 가장 단순한 방법은 모든 에지를 훑으면서 이 테스트를 수행하는 것이다.

Lander는 최적화 방법을 제시했는데, 연결된 삼각형 메시에서 양쪽 삼각형이 같은 평면에 있으면, 그 edge는 윤곽선일 수 없다는 것이다. 단순한 시계(clock) 모델에 이 테스트를 구현했을 때, edge 개수가 444개에서 256개로 줄었다.

더 나아가, 모델이 실체(solid object)를 정의한다면, 오목(concave) 에지는 결코 윤곽선이 될 수 없다. Buchanan과 Sousa [207]는 각 에지마다 따로 내적(dot product) 테스트를 수행하지 않고, 이미 계산한 각 면의 내적 테스트를 재사용하는 방식을 사용했다.

명시적(edge list 기반) 윤곽선 검출 방식은 CPU 부하가 크고 캐시 효율이 낮다. 왜냐하면 윤곽선을 형성하는 에지들이 에지 리스트 전체에 흩어져 있기 때문이다. 이런 비용을 피하려면, 버텍스 셰이더를 사용해 contour edge를 검출하고 렌더링할 수 있다.

구현 방법은 모델의 모든 edge를 파이프라인에 내려보내고, => geometry shader를 사용하면 패스가능

각 정점에 인접한 삼각형의 법선 정보를 추가로 포함시킨다.

위의 정보로 버텍스 쉐이더에서 contour edge인지 판정을하고,

contour edge라면 그려주면 된다.

(파이프라인에 geometry shader가 포함되어 있다면, 이런 추가적인 edge list를 미리 저장할 필요가 없고, 즉석에서 생성할 수 있다.)

## 

## Hidden Line Removal

윤곽선을 찾아낸 후에는, 선들을 렌더링한다.  
edge를 명시적으로 찾은 장점은, 펜 스트로크, 페인트 스트로크 등 원하는 다른 매체로 스타일링할 수 있다는 것이다. .

기하학적으로 찾은 모든 edge가 화면에 보이는 건 아니다.

단순히 Z-buffer만 써도 가려지는 선분을 판별할 수 있지만, 연속적인 스트로크를 표현하려면 hidden line rendering으로 어떤 선분이 어디서 시작되고 끝나는지 정확히 계산해야 한다.

(붓 터치 같은 렌더링은 시작과 끝을 알아야지 자연스럽게 그려질 것이다. 만약 z buffer로만 처리한다면 잘려나가는 느낌이 들 것이다.)

![](https://blog.kakaocdn.net/dna/cwR9oA/btsP4mNjS0A/AAAAAAAAAAAAAAAAAAAAAFBtzDPxoTpnCQOTumyFUPtmlurToQc7gX27WnYvdDTD/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=CsPUjW9tsRgCdP7Ow9H%2B3njQQKI%3D)

이 문제를 해결하기 위해, 객체의 모든 삼각형과 윤곽선을 렌더링하면서 각각 다른 ID를 할당했다.

이 ID 버퍼를 다시 읽어들여, 어떤 contour edge가 가시적인지 판정한다. 그런 다음, 이 가시적 선분들을 겹침 여부를 검사하고 부드러운 스트로크 경로로 연결한다. 스트로크 자체는다양한 방식으로 스타일링할 수 있다.

Cole & Finkelstein의 Segment Atlas 방식 + Rougier의 절차적 점선 패턴이 존재한다.