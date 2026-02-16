---
title: "[실습저장소] Cloud (ShaderToy에서 편집)"
date: 2025-07-17
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

Modeling:

<https://tithingbygame.tistory.com/226>

[[논문 정리] The Real-time Volumetric Cloudscapes of Horizon: Zero Dawn(1) - 구름(모델링)

siggraph 발표 글을 정리했으니,, 논문정리 카테고리를 선택했습니다..ㅎㅎ구름 렌더링 글을 적으면서 참고한 글 주로 이 글을 봤습니다. https://www.guerrilla-games.com/read/the-real-time-volumetric-cloudscapes-of-

tithingbygame.tistory.com](https://tithingbygame.tistory.com/226)

Lighting:

<https://tithingbygame.tistory.com/227>

[[논문 정리] The Real-time Volumetric Cloudscapes of Horizon: Zero Dawn(2) - 구름(Lighting)

구름을 렌더링하기 위해서 첫 번째로 한 일은 modeling이 였습니다. https://tithingbygame.tistory.com/226 [논문 정리] The Real-time Volumetric Cloudscapes of Horizon: Zero Dawn(1) - 구름(모델링)siggraph 발표 글을 정리했

tithingbygame.tistory.com](https://tithingbygame.tistory.com/227)

Rendering:

이번 실습은 shaderToy에 존재하는 구름 데모를 편집해서 조금 더 발전시켜봤습니다.

좌측이 제가 수정한 구름이고, 우측이 shaderToy에 있던 구름 원본입니다.

뭐가 바뀌었을까요????



좌측 구름에는 curl noise texture를 사용해서, 정적 구름처럼 가만히 있는게 아니라 동적 구름처럼 구름 끝자락이 뭔가 피어오르고, 사라지고 ... 그런 느낌을 추가했습니다 하하;;

(티는 안나지만, 구름을 생성하는 noise texture도 바꿨습니다.) => poslin-worley texture로 동일 계열이긴합니다.



이건 위의 모델에서 Light 까지 추가했습니다.