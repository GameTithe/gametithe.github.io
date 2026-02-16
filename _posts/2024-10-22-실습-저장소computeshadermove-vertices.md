---
title: "[실습 저장소]ComputeShader(Move Vertices)"
date: 2024-10-22
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

Vertex Buffer를 사용하지 않고, StructedBuffer를 사용해서 애니메이션을 넣어줬다. StructedBuffer는 1차원 배열로 사용되어진다.

### **VertexShader**

![](https://blog.kakaocdn.net/dna/LfUhq/btsKexsrmFa/AAAAAAAAAAAAAAAAAAAAAKR-ozoYmZjdMuGZVe61vVIUo4fUNl1Z-Jw4Hu4_bULa/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=cCB3NnqRTGjW%2FU7ps8hq%2BQbVrj8%3D)

position을 그대로 다음 shader에게 넘기는 것으로 보인다.

여기서 넘기는 position은 이미 ComputeShader에서 이동 처리가 되었다.