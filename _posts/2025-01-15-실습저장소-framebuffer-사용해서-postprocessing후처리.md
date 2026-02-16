---
title: "[실습저장소] FrameBuffer 사용해서 postProcessing(후처리)"
date: 2025-01-15
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

이론:

<https://tithingbygame.tistory.com/142>

[[CG] FrameBuffer 사용해서 postProcessing(후처리)

Framgbuffer를 적용한 간략한 순서1. 후처리 FrameBuffer를 만든다.2. 후처리 FrameBuffer에 물체들을 그려준다. (texture에 따로 저장)3. 기존 FrameBuffer에 사각형에 후처리 FrameBuffer에 저장된 texture를 입힌다.4.

tithingbygame.tistory.com](https://tithingbygame.tistory.com/142)

1. 후처리 FrameBuffer에 물체들을 그려준다. (texture에 따로 저장)

2. 기존 FrameBuffer에 사각형에 그린다.

3. 사각형에 후처리 FrameBuffer에 저장된 texture를 입힌다.

4. 해당 texture를 shader에서 kernel을 이용해서 색 조정을 한다.

5. 완성된 rendering을 보고 만족해한다.

![](https://blog.kakaocdn.net/dna/ljxsG/btsLNWLaQSO/AAAAAAAAAAAAAAAAAAAAACAqxMKe5h0mRxMs5gYXBjwgMkK06OVaHSsY4ef8p-dd/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=tQ1C2vLB5VdlXejyOZCFWd2Ymd4%3D)
![](https://blog.kakaocdn.net/dna/bbcjw2/btsLN0fHl3g/AAAAAAAAAAAAAAAAAAAAAJdTBdMTxzzE668CPV1tzyylAQ-1rcTGjM86pqa5xoV-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FIo09aQ%2F77G5Lgrs2UhXvtJyncI%3D)
![](https://blog.kakaocdn.net/dna/cjM8rB/btsLOJ5rPmx/AAAAAAAAAAAAAAAAAAAAANMttyK0WmsebzyMTg3wWzviUtjU34MpFuEJhQMwC9RY/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=zHDOkeOqUif1tnTFhTrNm1MjJeQ%3D)
![](https://blog.kakaocdn.net/dna/Fozmy/btsLPkqAAtA/AAAAAAAAAAAAAAAAAAAAAPfX98IsYW1ZOrPkd8qVKlWjTTuo1omEoET-ooiXa-yL/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=YLbDzS7vznD%2B6Cx41DzeOC%2B4i%2Bo%3D)
![](https://blog.kakaocdn.net/dna/bksYDy/btsLUtI3qOw/AAAAAAAAAAAAAAAAAAAAAHKSfdbGIWViJpu26U3Pr6UKF6_3ijKlSajiiZsZmgcv/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=gNl1mNvtheEAU0pANVJGMl4ISAI%3D)