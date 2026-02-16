---
title: "[RealTimeRendering-4th] Image-Space Effects(1)"
date: 2024-10-21
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

## **Image Processing**

렌더링 이후에 이미지를 변환하는 것을 Post-Processing 이라고 한다.

single frame을 렌더링하는 동안 수많은 passes, accessing image, depth 등이 동작한다. Battlefield4 게임에서는 한 프레임당 50개의 서로 다른 렌더 패스가 진행되었다.

post-processing 기술의 키는 GPU활용이다. 장면은 offscreen(back buffer같다)에 렌더링 되는데, 컬러 이미지나 z-depth 버퍼와 같은 형태로 존재할 수 있다. 이 결과 이미지는 texture로 다루어자며, 화면 전체를 채우는 사각형으로 적용된다. post-processing은 이 사각형을 렌더링하면서 이루어지는데, 각 픽셀마다 픽셀 셰이더 프로그램이 실행된다.

실제로 화면을 채우는 사각형보다 삼각형을 사용하는 것이 더 효율적일 수 있다.

예를 들어, AMD GCN 아키텍처에서는 두 개의 삼각형으로 구성된 사각형 대신 하나의 큰 삼각형을 사용했을 때 약 10% 더 빠르게 이미지 처리가 진행되었다고 한다. 이런 렌더링 방식을 풀스크린 패스(full screen pass)라고 부른다. 

또한, ComputeShader를 이용해 이미지 처리 작업을 수행할 수도 있다.

ComputeShader는 커널 크기가 클수록 픽셀 셰이더보다 성능이 좋아진다.

예를 들어, 스레드 그룹 메모리(thread group memory)를 통해 여러 픽셀의 필터 계산 시 이미지를 공유하여 대역폭을 줄일 수 있다.

![](https://blog.kakaocdn.net/dna/7Bryz/btsKe8egpsy/AAAAAAAAAAAAAAAAAAAAAAx6FqELJh9AFHhcEKuIQElZ97yL4dnGYYIFu-HekwqQ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1YMyXqzvA4nzBVkLkZoesgt5IoY%3D)

GPU의 하드웨어는 내장된 보간(bilinear interpolation)과 밉매핑(mipmapping) 기능을 활용해 텍셀 접근 횟수를 줄일 수 있다.

예를 들어, 3×3 박스 필터(box filter)를 사용하여 중심 텍셀 주변의 9개 텍셀의 평균을 구하는 경우, 픽셀 셰이더는 이 9개의 텍셀을 직접 샘플링하지 않고도 네 번의 텍스처 접근으로 동일한 결과를 얻을 수 있다.  (위에 그림 참고)

박스 필터처럼 모든 텍셀의 가중치가 동일한 경우, 4개의 텍셀 사이에서 한 번만 샘플링하여 평균 값을 얻을 수 있다. 예를 들어, 두 개의 텍셀의 가중치가 다를 때도 보간 위치를 조정하여 적절한 가중치 비율을 반영할 수 있다.

블러링을 수행할 때, 이미지를 더 작은 해상도로 줄여서 처리하는 방법을 사용할 수 있다. 예를 들어, 이미지의 해상도를 절반으로 줄이면 전체 픽셀 수가 줄어들어 성능이 개선된다.

다운샘플링된 이미지를 블러링한 후, 원래 해상도로 확대하여 사용하는 방식은 큰 면적의 블러링에 효과적이고, 시각적으로 유사한 결과를 얻을 수 있다. 밉맵을 활용한 블러링 가속화에도 사용될 수 있다.

또한, 다운샘플된 이미지를 사용하는 경우 메모리 접근 비용이 줄어든다