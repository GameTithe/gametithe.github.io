---
title: "[실습저장소] 3D Stable Fluids(+free slip)"
date: 2025-05-31
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

![](https://blog.kakaocdn.net/dna/UrVfm/btsOlatFCZc/AAAAAAAAAAAAAAAAAAAAADot6UWu7mhXOTZLL4PnCMYHvFb60RsPonLOB0flbfdS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=C1kyZtYQEgLfhMWYP2axKH3l2IQ%3D)

![](https://blog.kakaocdn.net/dna/UH9kj/btsOldQ7IjB/AAAAAAAAAAAAAAAAAAAAAMIWbfQqPeOmI-KA0QOCOeQCti_g9ik_1V46aM9VG_wD/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ymVRjbJAbTiBZzX%2Bm4%2FZXs18ijg%3D)

이건 움직이지 않는 장애물



이건 움직이는 장애물에도 반응할 수 있게 추가했습니다.



원래는 속도 field까지 만들어주는 것이 정석인 것 같지만,

임의의 움직임에도 반응할 수 있게 만들고 싶어서,

curPos, prvePos로 gradient구하고, 그걸 사용해서 장애물 속도를 단순하게 구했습니다.