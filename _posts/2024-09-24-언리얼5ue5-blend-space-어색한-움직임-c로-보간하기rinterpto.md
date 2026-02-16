---
title: "[언리얼5/UE5] Blend Space 어색한 움직임 C++로 보간하기(RInterpTo)"
date: 2024-09-24
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

## **문제1**

1. 좌우로 왔다갔하면 애니메이션이 덜컹 덜컹 거린다.

## **해결법**

![](https://blog.kakaocdn.net/dna/2IFMc/btsJKksJnvK/AAAAAAAAAAAAAAAAAAAAAFso8eeOWwL-aX7pFkN3GU8WgOSnnHgqG7KHWf-4Qh5Y/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=x%2BLklfONN99JXxsGIVJJ542nQPs%3D)

Smoothing Time을 0.2정도로 주면

interpolation이 되면서 좌우 움직임이 자연스럽게 이동된다

## **문제2**

![](https://blog.kakaocdn.net/dna/6TZmn/btsJKw0ViiJ/AAAAAAAAAAAAAAAAAAAAAErmwr_mjfy8Zr9eJ0S_1d8d9krywMZX0vpQRAeZYjiW/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=NDUXBdPnEitfX%2FPO6o%2BYm6YFPuU%3D)

Yaw가 -180에서 바로 180으로 이동이되는데

이것마저도 interpolation이 되면서 뒤로 가는 애니메이션이 덜컹거린다.

## **해결법2**

![](https://blog.kakaocdn.net/dna/bgJ44W/btsJIVHSArI/AAAAAAAAAAAAAAAAAAAAAIxMCMsmK2OjpGwlHw6IaRb14Xru7D5NP6wfz0b0zbfL/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=TMK%2FyBuUMo4Jx6AA0uDvxh47Wvg%3D)

RInterpTO는 제일 빠른 보간 방법을 찾는다. 그래서 -180에서 180으로 이동할 때 0을 거쳐서가는 것이 아니라

바로 180으로 이동한다.

때문에 RInterpTo를 사용하면 덜컹거리는 애니메이션이 없어진다.