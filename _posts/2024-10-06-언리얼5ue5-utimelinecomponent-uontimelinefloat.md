---
title: "[언리얼5/UE5] UTimelineComponent, UOnTimelineFloat"
date: 2024-10-06
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

우선 필요한 것은

UTimeComponent\*

UOnTimelineFloat

UCurveFloat\*

와

Update함수

Start함수이다.

변수, 함수의 이름을 다음과 같이 설정했다.

![](https://blog.kakaocdn.net/dna/EDric/btsJUvnEqb1/AAAAAAAAAAAAAAAAAAAAAD2X1Ml9fD-nPXBdj8X4Ua_je-QevprMZ3yGo9lop4vh/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=c8mwwTfkF8vA34jpVIXi%2BgFqAzY%3D)

우선 순서를 먼저 설명하겠다.

1. **Timeline Component 생성 및 바인딩**: 타임라인 컴포넌트 생성 후, **DissolveCurve**와 **DissolveTrack** 바인딩
2. **StartDissolve** 함수 호출로 타임라인 재생 시작
3. **UpdateDissolveMaterial** 함수로 실시간으로 머티리얼 파라미터 업데이트'

StartDissolve함수는 실행 조건이되면 외부에서 호출한다.

DissolveTimeline(UTimelineComponent)을 이용해서 DissolveTrack(FOnTimelineFloat)에DissolveCurve(UCurveFloat)를 등록한다.

그리고 Play를 해주면  
미리 설정해둔  Curve의 값들이 Parameter로 들어가면서 실행이된다.

![](https://blog.kakaocdn.net/dna/cl0pMN/btsJToJWfN9/AAAAAAAAAAAAAAAAAAAAAF96kuWxRdig8Y2oTwebSNOygxCg9uo_EHN56fpWie5F/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=jSNuf46ogyjKtKfOgkm1hPh9YNk%3D)