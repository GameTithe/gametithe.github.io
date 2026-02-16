---
title: "[논문 정리] The Real-time Volumetric Cloudscapes of Horizon: Zero Dawn(1) - 구름(모델링)"
date: 2025-07-17
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

siggraph 발표 글을 정리했으니,, 논문정리 카테고리를 선택했습니다..ㅎㅎ

### **구름 렌더링 글을 적으면서 참고한 글**

**주로 이 글을 봤습니다.**

<https://www.guerrilla-games.com/read/the-real-time-volumetric-cloudscapes-of-horizon-zero-dawn>

[The Real-Time Volumetric Cloudscapes of Horizon Zero Dawn - Guerrilla Games

Real-time volumetric clouds in games usually pay for fast performance with a reduction in quality. The most successful approaches are limited to low altitude fluffy and translucent stratus-type clouds. For Horizon Zero Dawn, Guerrilla need a solution that

www.guerrilla-games.com](https://www.guerrilla-games.com/read/the-real-time-volumetric-cloudscapes-of-horizon-zero-dawn)

이건 맛만 봄

<https://patapom.com/topics/Revision2013/Revision%202013%20-%20Real-time%20Volumetric%20Rendering%20Course%20Notes.pdf>

테스트 해본 Base Shader Toy

<https://www.shadertoy.com/view/XtBXDw>

[Shadertoy

0.00 00.0 fps 0 x 0

www.shadertoy.com](https://www.shadertoy.com/view/XtBXDw)

폴리곤으로 했지만, 두꺼운 구름은 그럴싸해도, 얇은 구름은 별로임

![](https://blog.kakaocdn.net/dna/wf630/btsPljpmeiw/AAAAAAAAAAAAAAAAAAAAAEQ9TQunDn1Pu0jioxNmJHpJQjl9sI3-_0YPqPDKjCca/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=99PGf3Nu1fU1LBdJaXiZGRGlAaw%3D)

빌보드(2D 평면에 이미지 불러오는거라고 생각) 방식으로 어떻게 돌파해보려했지만, 시간에 따른 inner shadow가 구현이 안됨

![](https://blog.kakaocdn.net/dna/cF05rR/btsPmdhvh7N/AAAAAAAAAAAAAAAAAAAAAEVchoT-f067on7MclQ_DJowO4IaN8FDa5odNrQMEAjJ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=um1ze9U0fUJAC2CqulVorUa4rbM%3D)

그럼 sky dome 형식은?

voxel(asset) 기반 구름들을 구름세트로 만들어서 배

어느 정도 괜찮은데 역시 시간에 따른 구름 형태 + 머리위로 지나가는 구름 + 성능 이렇게 문제들이 존재했다.

![](https://blog.kakaocdn.net/dna/KqK3g/btsPla0njDE/AAAAAAAAAAAAAAAAAAAAALm7eFPv5AB7bDaKWMAJQCrAXTn231tGxCBfAv032CL1/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=sNjwk7qtz4vH0rPvhgtrOvyG8WE%3D)

그냥 volumetric Rendering을 해볼까?

이거의 문제

1. 많은 texuture read

2. 비용 비싼 ray marching

3. 많은 반복문

그래도 이전에 volumetric lighting을 빠르게 할 수 있는 방법들이 연구되었기 때문에 한 번 해보자라는 생각

일단 3D Perlin Noise로 첫 번째 테스트를 해봤다.

굉장히 느렸지만, 가능성이 보였고 volume rendering을 진행하기로 결정!

![](https://blog.kakaocdn.net/dna/M53Yg/btsPmeN8EMA/AAAAAAAAAAAAAAAAAAAAAHiBvBoN-BCJuiH0bINlgx36YIyg7FaiU4Abd7tAb9W2/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ZJ5drjMSawCyRClCKKpcJLvCetw%3D)

후디니를 커스텀해서 여차저차 구름을 만들어냈지만, 1초당 1frame만이 완성될 정도로 매우 느렸다.

이렇게 된거 저해상도 노이즈를 개발하는 방향으로 선회

![](https://blog.kakaocdn.net/dna/F9nvb/btsPkm1zIXp/AAAAAAAAAAAAAAAAAAAAAG5-fxxQgtHfOzxS1V_vRdjsQzL0KH_MPPgL8ggsPPMG/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=WEOvyxxUT93RrQZKBoKSNWqRFSQ%3D)

일반적인 volume rendering은 카메라 위쪽에 구름을 배치하고, fBm(fractal Brownion motion)으로 구름을 그럴싸하게 만드는 방법들이였다.

fBm은 여러 옥타브의 Perlin noise를 여러겹을 쌓아 구름처럼 풍부하고 세밀한 볼륨 구조를 만들어준다.

(옥타브가 높다는 것 => 주파수가 높다는 것

주파수가 높다는 것은 세밀함이 높다는 의미)

![](https://blog.kakaocdn.net/dna/b4g6Ix/btsPliqvOQC/AAAAAAAAAAAAAAAAAAAAAAnQi0lgc2SqsiZaJ-5yIif0z-9GuhwSokb-zZtC0yIH/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Tc0IatWSDQnz7By4TBYzP4SxGj8%3D)

일단 ray marching으로 렌더링하고

높이에 따라 밀도를 변화하기 위해서 noise에 gradient를 결합한다.

![](https://blog.kakaocdn.net/dna/0bOVD/btsPlQNPLIP/AAAAAAAAAAAAAAAAAAAAAMMy1e4_4dG0E_uw_cFbIV-6wjZpuwAItwDKaxVYY2vk/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=NlQPsBVWPbiJmacTuFk%2Fx5eM7ao%3D)![](https://blog.kakaocdn.net/dna/n27m4/btsPkEAXe2w/AAAAAAAAAAAAAAAAAAAAAAA4TbOU9L476ECr-lk8ATbm0DzYCtB6PN6djp9LiVOX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=DuWT4RKm%2FeWMonc75Ff8Ro8fMyk%3D)

오케이, 나이스 구름 처럼보이네 (왼쪽이 shader로 만든거, 오른쪽이 사진)

근데 사진을 보면 **구름이 마치 공장 굴뚝에서 증기처럼 솟아오르는 형상**이 보인고,

위쪽은 **둥글고 부풀어 오른 형태,** 아래쪽은 **희미하고 퍼지는 형태로 보이는데**

우리 구름은...  너무 랜덤 노이즈 같다

fBm만으로는 어렵네...

(shader toy에서 이것저것 만져보는 중인데, 아마 이렇게 보여져서 그런 것 같다.)

왼쪽: perline noise, 오른쪽 fbm perlne noise

![](https://blog.kakaocdn.net/dna/maY9F/btsPk5eqgmH/AAAAAAAAAAAAAAAAAAAAAAdexXuQepCqVWDXn_zB8p9AH7B7VdaucMeoRsQ_FPKf/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=T0uOSPy3xXd%2BnNanZS0TJ%2FX6mw8%3D)![](https://blog.kakaocdn.net/dna/xjZTG/btsPmpo3YHJ/AAAAAAAAAAAAAAAAAAAAAPTv848OpobbcJsqumIvevpOAQuNmkUE7sC0r36bpkFk/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=FyrNYtOwqoWwPr3KFND8vDE7Szg%3D)

뭐가 문제였을까? 부풀어오르는 느낌이 없는게 문제 아닐까?

![](https://blog.kakaocdn.net/dna/c17X02/btsPmcCYgOm/AAAAAAAAAAAAAAAAAAAAAP0EC6BdLi8U4dh7-eio9PF5yXMq1jeV8Dk4sHDuwC8f/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3q3cY2GZ7YU%2Bqb%2BdZc15gy2c7X8%3D)

사진

어떻게 해결하냐?

뭐 어째 노이즈 텍스처 써야지... 좋은거 없나? Worley noise는 어때?

Worley noise는 원래

caustics나 water effect에 쓰이던 노이즈 였다.

아래의 이미지가 caustics이다.

![](https://blog.kakaocdn.net/dna/bkmNrk/btsPkqJzYG8/AAAAAAAAAAAAAAAAAAAAAJDwg86YmJ23O7WATwgoBRii_thipKJtC2LY40P5n0Fr/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=zR7wGZjHCG2BNDcPDlcyAkV7ibI%3D)

worleynoise를 생을 사용하면 이렇게 보인다. 살짝 아쉽죠잉

왼쪽이 worleynoise, 오른쪽이 worleynoise fBm

![](https://blog.kakaocdn.net/dna/sAm3e/btsPm03oPlt/AAAAAAAAAAAAAAAAAAAAAIf2kf3-O1DvR3aUy-Pb-85X4VAJNOzYSHWQAaUIQMv0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=0zH9kH4c2desLDfq2efXyjs8x2o%3D)![](https://blog.kakaocdn.net/dna/cOr9MZ/btsPkSe9nje/AAAAAAAAAAAAAAAAAAAAAEFh7VywlYFoSUnGEk7nAnfxVen7uTWnxWkPLPvgOzMu/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=8glUd%2F5t3KwQFtkKOx5Dg%2FWdpqU%3D)

covergae를 조정하면 더 아쉽죠잉...

![](https://blog.kakaocdn.net/dna/ABVkk/btsPmnY5jcs/AAAAAAAAAAAAAAAAAAAAAJiqDc0hANprpPIMBp_7TqJBlvaqd6W4xJNiBllBuSum/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Go9lQ0S1Jsc5QAKbOh0nOnCTvB8%3D)![](https://blog.kakaocdn.net/dna/dYqj00/btsPmeVrDnM/AAAAAAAAAAAAAAAAAAAAAKuo3lhxQQJmjd-czZkX6ijsEm9u8PfJKkxZum7Ra9Al/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=lAG8DXpkMXtzY80fnQCHAn0Om%2FA%3D)

Worley noise를 invert하면 둥글한 모양을 만들 수 있고, 이를 fBm처럼 여러겹을 쌓고, 여러겹 쌓은 것을 perlin noise의 offset으로 주면

Perlin의 연속성은 유지되면서, Worley의 둥글한 모양은 유지되는 노이즈가 만들어진다..!  
이를  Perlin-Worley noise라고 하기로 했다.

좌측은 invert한 직후, 우측은 perlin noise와 잘 섞었을 때 생긴 noise texture

![](https://blog.kakaocdn.net/dna/X7y8a/btsPkoZl96m/AAAAAAAAAAAAAAAAAAAAAC8E9SRTR9_Qtvv4_laajJ4DAuGClz9v-5T3N6SXX42n/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=R3E1M4AM4R3EifhhSClRP4i6Fyc%3D)![](https://blog.kakaocdn.net/dna/ZjoVV/btsPlIoQZk9/AAAAAAAAAAAAAAAAAAAAABNuhmC-MpcFXMjLFpPD7d5hyAIrEAIMxQRj3-YJHssv/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=M%2Fjz56KbaHC7fvLAlq1wWhy0%2BFA%3D)

제가 본 문서에서는 이렇게 두룽뭉실하게만 설명을 해줬습니다. 다행이 shaderToy에 누군가 Perlin-Worley를 구현해주었습니다. <https://www.shadertoy.com/view/3dVXDc>

[Shadertoy

0.00 00.0 fps 0 x 0

www.shadertoy.com](https://www.shadertoy.com/view/3dVXDc)

<https://www.shadertoy.com/view/XljBzt>

[Shadertoy

0.00 00.0 fps 0 x 0

www.shadertoy.com](https://www.shadertoy.com/view/XljBzt)

perlin-worley noise를 사용한 구름

파라매터를 잘 조정하니까 오른쪽과같이 이쁘게 된다.

![](https://blog.kakaocdn.net/dna/bK95y7/btsPmvXPrf1/AAAAAAAAAAAAAAAAAAAAAHFcTWtVb0bqSxsI5e93MBzbX1ixDNTtYDKwMiGmH-Kk/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=gij5VW7ys%2BqWfUWkTGDkCKraag0%3D)![](https://blog.kakaocdn.net/dna/QIJSQ/btsPmiLeUex/AAAAAAAAAAAAAAAAAAAAAFpHeij0zRm49aMmipL6AT2V8Vf30G79PHqWSKbWT4Ki/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=qzA%2FU0GRz6PMmy2lCAHRcFzLqMw%3D)

이렇게까지가 구름에 사용되는 nosie texture 에 대한 것이다.

이제 우리가 이 texture를 사용해서 어떻게 구현했는 지 알려주겠다.

우리는 구름을 위한 총 3가지의 texture를 사용하는데,

**첫 번째는 Perlin- Worley noise ( 128 ^ 128 ^ 128 )**

**R 채널**: Perlin-Worley noise (하이브리드 billow 기반 노이즈)

**G/B/A 채널**: Worley noise at increasing frequencies (fBm 방식)

![](https://blog.kakaocdn.net/dna/H02Iy/btsPkJ91fmJ/AAAAAAAAAAAAAAAAAAAAAO1dSxPh5CnjZeeKBm_7Lcgr0DFF3EIGzWdRN_j9hJTt/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=jitBWvMNfpnyFWrlOooUcflCxXA%3D)

shader toy에서 확인할 수 있다. <https://www.shadertoy.com/view/3dVXDc>

첫 번쨰가 perlin-worley, worley(주파수 낮), worley(주파수 중), worley(주파수 고), cloud

![](https://blog.kakaocdn.net/dna/SH2Ox/btsPkJB9Vgh/AAAAAAAAAAAAAAAAAAAAAN0WH6OCosg77wvbK2WkvQBOFqmIrJGQ680JKlmfGZXy/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=sVK3Yxf4mzTdp93n5XFLFMAn6PM%3D)

**두 번째는 texture는 Worley noise인데 저해상도이다 ( 32 ^ 32 ^ 32 )**

첫 번째 텍스처로 만들어진 구름 주변에 추가할 디테일들이다.

( shadertoy로 만져보면서 느낀건 mipmap을 만져주면 같은 효과가 날 것으로 예상 )

![](https://blog.kakaocdn.net/dna/dunC1U/btsPlVhcU32/AAAAAAAAAAAAAAAAAAAAALEKrRP1XXe78sQZFF-V-1ZlSrFLJBT4sEuETDM-DbOb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fG%2BJ0oiF8rpBOyfUjwsNKsPelGs%3D)![](https://blog.kakaocdn.net/dna/qrlsm/btsPldJ0TMs/AAAAAAAAAAAAAAAAAAAAAP16FSQVneHlOD8YKGVdzfZpDGC0zmswSb3PpSxmOEEX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=DTHNlc0XFUOB8R3JBdhza43G0Q4%3D)

**마지막 texture는 2d texture이다. (128 ^ 128)**

용도는 curl(회전) noise이다. 난류, 유동성 느낌을 내기 위해서 사용된다고 보면 된다.

![](https://blog.kakaocdn.net/dna/c1Juqk/btsPlwPHmqx/AAAAAAAAAAAAAAAAAAAAAMr4VdlfDtMthodGkMYjmMKkvYJ38SOSR6QJpl7Czvbn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=SngQBx2Zf1vRbIhe%2BrQ0w6DRi%2FM%3D)

기존에는 위로 갈 수록 밀도를 낮추는 방법을 사용했는데,

우리는 여러종류의 구름을 나타내기 위해서 3가지 유형의 구름 texture를 준비해두었다.

그리고 얼마나 구름을 노출할 지에 대해서 coverage 변수를 사용할 것이다. 이 값은 [0,1]이다.

![](https://blog.kakaocdn.net/dna/rs1eL/btsPlHwIMIY/AAAAAAAAAAAAAAAAAAAAAIUAQLL8lAZusolk25phcQ1-pRR_9tMN1xIjS5LlDDnG/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=i83Ru04Zipf1zgu8vgG6vb1xQOk%3D)

이렇게 우리가 사용한 texture들에 대해서 설명을 했고,

진짜 구름을 그려보자

### **1. Base Shape 잡기**

![](https://blog.kakaocdn.net/dna/bV7IkV/btsPkJvphyx/AAAAAAAAAAAAAAAAAAAAALJRo2IAos71UB9ZQElqUhCn6OU1pqwghyqZ8iBw8s61/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Bf4raQYZTVGkVB5wtB%2FAMR694wM%3D)![](https://blog.kakaocdn.net/dna/bcFpJx/btsPlMxVMTr/AAAAAAAAAAAAAAAAAAAAAEXWcik9f7GgHhFNBKN2fc9KId1U5XSzp7jelSfPamek/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ZU0eBwnu5alBVk50vN91l3dHOi0%3D)

첫 번째 3d텍스처(perlin-worley + worley)를 사용해서 기본 구름을 생성한다.

여기에 height signal을 곱해서 고도가 높아질 수록 밀도가 많아지게 만든다.

(물리적으로 고도가 높을 수록 온도가 낮고, 온도가 낮을 수록 밀도값은 커진다.) 

### **2. Coverage & Bottom Fade 적용**

![](https://blog.kakaocdn.net/dna/b0VSkl/btsPmnYDnKt/AAAAAAAAAAAAAAAAAAAAAIacUX-VrUU9LCM-0rmGZyAvvaHZw5-NI3r5-Q4oWvl9/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=DsIATZ5cylA6aSyMK9crhMZbH7Y%3D)

Coverage: 구름이 존재할 확률

Base Cloud에 coverage를 곱한다.

그리고 구름의 바닥 부분의 밀도를 줄인다.

soft fade 또는 cut off

이렇게 만들어진 구름에 2번째 3D texture를 빼서, 가장자리 디테일을 만들 수 있다.

( 2번째 3D Texture를 3번째 2D curl texture로 왜곡시키면 난류 효과도 낼 수 있다. )

결과적으로 이렇게 렌더링이 가능해진다.

![](https://blog.kakaocdn.net/dna/b0YtEF/btsPlOvMgin/AAAAAAAAAAAAAAAAAAAAAGUrjdcX5pD8FZGvHy1RSeu2ihzxIv22yVd9XxR8QLTE/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=DRgMZLu57OmQ%2BW8PAk05W2JriwE%3D)

좌측: Perlin-Worley Noise Texture + Curl Noise Texture를 사용

우측: Perlin-Worley Noise Texture



제가 조금 사기를 쳤는데요. 무슨 사기일까요?

### **Lighting**

사실 언급은 안했지만, 우리가 shaderToy에서 시작한 덕분에 빛 계산이 자동으로 되고 있었다.

lighting  함수를 주석처리해봤다... 뭔가 사기당한 것 같다.

![](https://blog.kakaocdn.net/dna/ljr9u/btsPonKW7dv/AAAAAAAAAAAAAAAAAAAAABNEAPNMagI1RCXHGM3rdiVDfW79ncO2I-czBtXxu8sR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Sz%2Bnp5BZG0AnVpemZ5N3sN9dfio%3D)

다음 글에서는 Lighting에 대한 글로 돌아오겠습니다 :)