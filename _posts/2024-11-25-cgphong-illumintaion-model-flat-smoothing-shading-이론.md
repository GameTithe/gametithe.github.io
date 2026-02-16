---
title: "[CG]Phong Illumintaion Model: Flat, Smoothing Shading 이론"
date: 2024-11-25
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

굵직하게 보면 이렇게 됩니다.

**Phong illumination modeling**

1.Flat shading

2.Smoothing shading

 - Gouraud shading

 - Phong Shading

### 

### **Flat Shading**

Flat Shading은 한 점에 여러 삼각형의 꼭짓점이 맞닿아있을 때, 각각의 삼각형의 normal vector를 모두 사용하는 것입니다.빨, 초, 파의 noraml vector가 다음과 같을 때,,

**가운데 점은 빨,초,파 색의 normal vector를 삼각형 그릴 때 마다 색에 맞게 사용한다.**

![](https://blog.kakaocdn.net/dna/RZuGq/btsKT5v4gNg/AAAAAAAAAAAAAAAAAAAAAKXEjrd7J3osNa_xw4xnoarlNMYVOlK6WKIWf7IislUN/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=tUipxtR8qCk5Hilv8fkTl%2FqwCwk%3D)

코드로 보면, n을 하나하나 할당해주는 것을 볼 수 있다.

a,b,c,d가 정점이고, normal vector는 cross 로 간단히 구할 수 있다.(아래 그림과 같은 원리이다 ..ㅎㅎ)

![](https://blog.kakaocdn.net/dna/5Mz8Z/btsKVq7myPW/AAAAAAAAAAAAAAAAAAAAAMy62NBA9bofhbreTWAF98aRIBAIRsCyz76gDgqNRlJr/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=c58xKrytov9qPQNk6jJFjTeX%2FZM%3D)
![](https://blog.kakaocdn.net/dna/9tEwq/btsKT7tUxCc/AAAAAAAAAAAAAAAAAAAAAFaxutkW7GCIzsCojQwyHAA_g-1eElbimqwrpxpY0gyW/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=murEkDJ%2B4rpNf3Ae%2F7iQn2yyj1Q%3D)
![](https://blog.kakaocdn.net/dna/bpfMB7/btsKT87q3pc/AAAAAAAAAAAAAAAAAAAAAD32URIaG-rF7rgUK3TEc9IpynHe_IKdnPM-BPmoJ2Y8/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=epiRAkd%2B8an612TFBQo5cWt8y1c%3D)

### **Smoothing Shading**

Flaat Shading 과 다르게, 여러개의 normal vector를 평균을 내서 사용한다.

![](https://blog.kakaocdn.net/dna/bwxdNM/btsKUhjizfn/AAAAAAAAAAAAAAAAAAAAAF2nb8pHIYopn0j-rNHpncA6HQgSbHo19T3Yyu78wHoz/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=H597KphMFjQvFkeIfsyDqw6dV8U%3D)

Flat Shaing과 다른 점은,  갈색 지점에서는 어떤 삼각형이던 같은 normal vector를 할당해준다.

normal vector에 정점(a,b,c,d)으로 할당해주고 있다.

(이게 가능한 이유는 0,0,0 에 위치한 구이기 때문에 가능한 것이다. 다른 도형이면 위의 설명처럼 평균을 내줘야할 것이다.)

![](https://blog.kakaocdn.net/dna/b3wcLm/btsKUC76cqA/AAAAAAAAAAAAAAAAAAAAANuNyLfSuYDmCN0ou6SuHueDp420r1rJeyMzqxYqm59H/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1dzMhDWcmhFkIP5zgEH9%2BaAEFeA%3D)
![](https://blog.kakaocdn.net/dna/ybEu6/btsKVzQtBbb/AAAAAAAAAAAAAAAAAAAAAF0kQ4Scw3GdAwXAGJlj7P4P8Z9esomyeHsbwnsBSccg/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=M%2BbUF8B7kjprDJUqJkNZ%2Bh4V6kM%3D)

두개의 차이점은 영상을 보면 확실히 알 수 있다.

<https://tithingbygame.tistory.com/manage/posts>

[티스토리

좀 아는 블로거들의 유용한 이야기, 티스토리. 블로그, 포트폴리오, 웹사이트까지 티스토리에서 나를 표현해 보세요.

www.tistory.com](https://tithingbygame.tistory.com/manage/posts)