---
title: "[논문저장소] Gaussian Splatting (미완..이여서 미안...해서 실행시키는 법을 곁들였습니다)"
date: 2024-11-10
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

Gaussian Splashing, Raytracing을 읽는데 필요한 지식이지만,,,, 정리 순서는 어쩌다보니,, 마지막이 될 것 같아서 일단은 간단히만 정리해두고  
나중에 다시 와서 추가하겠다!!!

일단 이미지를 많이 가져온다. (적어도 괜찮지만 성능은 안나온다.. 그럼 안괜찮은건가..?)

(아래 이미지는 사실 가우시안 스플랫팅 완료된 모습인데, 이미지랑 거의 같아서 썼습니다...ㅎ..ㅎ, 본래는 이미지들을 넣어주는 겁니다)

![](https://blog.kakaocdn.net/dna/bQtc9U/btsKD2ybc3Y/AAAAAAAAAAAAAAAAAAAAAPDE43uOVOBlcHy9WH_ubkVK7OADRLGhoAqGhqDEcqAF/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=aLke8tBx8jfJJsjVQgQl%2B%2BgTXpk%3D)![](https://blog.kakaocdn.net/dna/n8yD5/btsKDYQd4w5/AAAAAAAAAAAAAAAAAAAAAGWWzA04bO_fGHWQiMejGAuQEJ3OEo7sls2xggpORnjU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3z9fi9mSk5wM0yTTlpZYA1zSJvc%3D)



![](https://blog.kakaocdn.net/dna/bermKK/btsKC5ifGVN/AAAAAAAAAAAAAAAAAAAAACZAKBMI8kCUJDsTAIbPcwLZqBaLH89yRCH4aLcbtsqQ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1b03CryzRH%2Fj8JJi6TQLNcHlzfs%3D)![](https://blog.kakaocdn.net/dna/VBdis/btsKDgKCdI4/AAAAAAAAAAAAAAAAAAAAAPyhhVhFiIKZ0DKFemxKC7S_ya0gMsDk7B_UOqEGQbsX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=qxmwj97cPpy2b%2B8pE2hUZpSMmYM%3D)

이렇게 360도 각도로 쭉~ 찍는다 여기서는 300장을 사용했다.

이렇게 이미지를 3d로 만드는 것이 목표인데... 이 오브젝트들 어떻게 저장하고 만들어야 되지? 2D를 3D로도 만들어야되고,,,

### **그럼 점으로 만들어볼까?**

![](https://blog.kakaocdn.net/dna/T4gTq/btsKDqfq2Op/AAAAAAAAAAAAAAAAAAAAAEeQT5GiFmGT6W5ZpzC0dny4yS4OPx3WFlO9_FOD9nSU/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=qUCUxXfN3cFVF4kInLM%2Fk7vGlUs%3D)

따란~

근데 빈 곳이 너무 많은데? 이거 저장은 되도 성능이 안나오잖아요!

### 

### **그럼 이 점을 늘려서 타원으로 만들어볼까?**

![](https://blog.kakaocdn.net/dna/cTWdcJ/btsKCUH9iUH/AAAAAAAAAAAAAAAAAAAAAL1DiY6O66Zt6UXYdSAi02mSb8blaXcCNX9xX95IC_9r/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=oazAGUBhTM2pMW1y8DdEEDze4SQ%3D)

따란~

타원들의 크기가 제가각인데요?

=> 여기서 Gaussian kernel을 사용하는데 그 값에 맞춰서 생성된다.

![](https://blog.kakaocdn.net/dna/buCC8j/btsKC6O1b9F/AAAAAAAAAAAAAAAAAAAAAJjSCvCYFFUZb65YO5_W7rHWKtoUKaLKmkqmfkPI6rt7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9uLhEXc8%2Bqjm9MGHbPIcXeTUUVA%3D)

공식을 외우라고 보여주는게 아니라 , 표를 봐보자

가운데에서 멀어질수록 0에 가까워진다. 그리고 그걸 3D로 면 타원처럼 만들어진다.

2번 째 그림에서 튀어나온 부분이 아래로도 있다면? 그게 타원이다!

이제 원본과 비교하면서 가장 복원을 잘시키는 색상을 가져오도록 학습시키자!!

그러면!

완료~~



이런 흐름인데,,,, 이렇게만 알아도 Gaussian Splashing, Gaussian Ray-tracing 논문을 읽을 수 있을 것이다!! 다음 스텝으로 가보자~

사실 이 글을 쓰게 된 90%의 이유는 저도 3DGS을 실행시켜보고 싶었는데, 컴퓨터 성능이 안좋아서 못시켜보다가   
코랩으로 해봐야겠다는 생각이 들어서 이리저리 서칭하고 실패하고 하다가 하는 법을 알아내서 기분좋아서 공유하려고 쓴 글입니다 :)  
  
Gaussian splatting colab 이라고 검색하면 바로 나옵니다.   
<https://github.com/camenduru/gaussian-splatting-colab>

[GitHub - camenduru/gaussian-splatting-colab

Contribute to camenduru/gaussian-splatting-colab development by creating an account on GitHub.

github.com](https://github.com/camenduru/gaussian-splatting-colab)

여기서 colab으로 들어가면 됩니다.

그리고 실행시키면 30-40분 정도 걸립니다. (학습시키는데 이미지 300장을 써서 오래걸리나봅니다..) 

저는 여기서 이제 뭘해야되지..하고 헤맸는데..

**GaussianViewTest라는 폴더안에 zip파일이 있을겁니다. 이거를 다운 받으면 됩니다.** (코랩을 닫았어서 정확한 경로가 기억이 안나네요.. 혹시 못찾으면 댓글 달아주세요)

압축을 풀고

GaussianViewTest\viewers\bin  
SIBR\_gaussianViewer\_app.exe 실행시키면~~~~

크래쉬가 납니다 :(  
SIBR\_gaussianViewer\_app.exe 가 있는 폴더에서   
**.SIBR\_gaussianViewer\_app.exe --model-path "{여러분의 경로}\GaussianViewTest\model" 이렇게하면 실행시켜볼 수 있답니다~~**

![](https://blog.kakaocdn.net/dna/xYg8h/btsKDBnq85X/AAAAAAAAAAAAAAAAAAAAABNcIbZ2xuByuSHaiKONz5IjG34OibY-r_uRBeoNlHkK/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=vloCiMnMFOR6x31H59G1LFAcSjY%3D)