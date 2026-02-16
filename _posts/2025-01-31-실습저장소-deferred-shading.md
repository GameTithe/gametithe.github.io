---
title: "[실습저장소] Deferred Shading"
date: 2025-01-31
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

구현

<https://tithingbygame.tistory.com/150>

[[CG] Deferred Shading

Deferred Shading 이란복잡한 조명효과에 대한 계산 부하를 줄이기 위해서 등장한 방법이다. 화면에 그려질 물체를 조명 효과 없이 그리고 그 뒤에 조명 효과를 적용하는 것이다.이렇게 하면 화면에

tithingbygame.tistory.com](https://tithingbygame.tistory.com/150)

![](https://blog.kakaocdn.net/dna/d2zu3k/btsL3nII9Rq/AAAAAAAAAAAAAAAAAAAAAPgQrmU-Y1h1X8Q6DvuKZzdpXwLnRRXRAp8BQRR4x6fS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=INLte0w02wRNu%2FMEMBGPOm%2B80DM%3D)

아래와 같이 G-buffer를 만들어주었습니다. deferred Shading을 했다는 인증...? 입니다 하하

![](https://blog.kakaocdn.net/dna/8ndfY/btsL3QwNDCN/AAAAAAAAAAAAAAAAAAAAANuDHoTH_8zFndNQblMsxayCPmtpf0IIIHD3ud74nJUX/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=acsvJylQgUKZ4jVlnwY5T9F%2BNvg%3D)![](https://blog.kakaocdn.net/dna/vOsMY/btsL4HlDeyM/AAAAAAAAAAAAAAAAAAAAAKtDRf3Qfv09eARVGbY4BpGAdZk44YwFHjqgizy5ZA5Y/tfile.dat?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=oPJAiLMJ%2FmK8MuyK6xBfODQB4c8%3D)