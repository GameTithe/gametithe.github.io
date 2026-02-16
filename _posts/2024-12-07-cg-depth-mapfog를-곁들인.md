---
title: "[CG] Depth Map(fog를 곁들인..)"
date: 2024-12-07
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### **Depth Map 만들기**

Rasterizatiion -> float(MSAA) -> Resolved(No MSAA) -> Post Effects -> Post Processing -> Back Buffer(최종 Swap Chain Present)

Depth Map을 관리하기 위해서 DepthOnlyView를 만들어서 사용한다.

PostEffect에서는 만든 Depth Map을 이용해서 안개효과를 만들어줄 것이다.

**(DepthOnlyDSV에는 MSAA를 사용하지 않고, DepthStencilView는 MSAA를 사용해서 Rendering을 한다.**

postEffectRTV은 MSAA를 사용하지 않도록 Resolved를 해준다.)

안개효과(Depth map을 다른 shader로 넘겨주기 위해서는)를 만들기 위해서 신경을 써야되는 몇가지 작업이 있다.

1. Texture2DMS를 Texture2D로 사용해준다.

Texture2DMS는 다른 Shader에 넣기가 어려우니 MSAA를 OFF해서 일반적인 Texture2D로 만들어서  Shader에 넣기 편한 Type으로 만들어준다.

2. DXGI\_FORMAT을 특정한 형식으로 사용한다.

Depth Map을 만들어주고, 그 값(Depth Map)을 Shader에 보내기 위해서는 일정한 형식을 따라서 만들어줘야된다.)

<https://learn.microsoft.com/ko-kr/windows/win32/direct3d11/d3d10-graphics-programming-guide-depth-stencil>

[Depth-Stencil 기능 구성 - Win32 apps

이 섹션에서는 출력 병합기 단계의 깊이 스텐실 버퍼와 깊이 스텐실 상태를 설정하는 단계를 다룹니다.

learn.microsoft.com](https://learn.microsoft.com/ko-kr/windows/win32/direct3d11/d3d10-graphics-programming-guide-depth-stencil)

**주요내용:**

깊이 스텐실 리소스는 DXGI\_FORMAT\_R32\_TYPELESS 같은 무형식 형식이어야 합니다.

깊이 스텐실 리소스는 D3D10\_BIND\_DEPTH\_STENCIL 및 D3D10\_BIND\_SHADER\_RESOURCE 바인딩 플래그를 모두 사용해야 합니다.  

[**D3D11\_DEPTH\_STENCIL\_VIEW\_DESC**](https://learn.microsoft.com/ko-kr/windows/desktop/api/D3D11/ns-d3d11-d3d11_depth_stencil_view_desc) 전달됩니다. 형식은 형식화된 형식(예: **DXGI\_FORMAT\_D32\_FLOAT**)을 사용합니다. 

DepthOnlyPS

```
m_context->OMSetRenderTargets(1, m_resolvedRTV.GetAddressOf(), m_depthOnlyDSV.Get());
m_context->ClearDepthStencilView(m_depthOnlyDSV.Get(), D3D11_CLEAR_DEPTH, 1.0f, 0);
 
 //물체들 Rendering
```

이렇게 depthOnlyDSV로 설정을 하고 물체들을 Render하면 Depth가 저장된다. (이미 depthOnly는 Stencil을 사용하지 않게 설정을 해서 Depth만 저장된다.)

Rende를 저장한 resolvedSRV와 Depth를 저장환 DepthOnly를 postEffect Shader에 보내서 합쳐주면 된다.

```
   vector<ID3D11ShaderResourceView *> postEffectsSRVs = {
        m_resolvedSRV.Get(), m_depthOnlySRV.Get()}; // 20번에 넣어줌
   m_context->PSSetShaderResources(20, UINT(postEffectsSRVs.size()),
                                             postEffectsSRVs.data());
```

Depth Map만 확인하면 이렇게 잘 만들어 졌음을 알 수 있다.

![](https://blog.kakaocdn.net/dna/c9iTAj/btsLbxdulpJ/AAAAAAAAAAAAAAAAAAAAADn7j-xhiNq_JtvUZK6jyX2II0d6UnnKDqUVVJJWCXGl/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=mYhsLZRuocvxK2v1Kl5hLLh%2BKIY%3D)

DepthMap의 값들을 이용해서 Beer- Lambert 공식을 적용하면  이렇게 안개효과를 줄 수 있다.

![](https://blog.kakaocdn.net/dna/k1WWg/btsLbaQlmLg/AAAAAAAAAAAAAAAAAAAAADv2pUyCQ_4JzONhMo-SCPymqJcxWEdsODr0I4cYfi9l/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Ybw4QSkMorBknwY%2BACaJosl0VMU%3D)

**구현하다가 힘들었던 점:**

처음에는 Smoothness 함수를 사용했었습니다. 그렇게 되면 뿌옇게만 되지 안개같은 느낌을 주지 못합니다.

그래서 Smoothness와 Beer-Lambert 그래프를 비교해보니 smoothness가 너무 완만한 느낌이여서 제곱을 해보았습니다.

그러면 그럴싸해보이긴 합니다. 그래도 Beer - Lamber 쓰는게 더 멋진 것 같습니다 허허..

![](https://blog.kakaocdn.net/dna/V3n9j/btsK9Wsga5N/AAAAAAAAAAAAAAAAAAAAAIv2om63DC7sKmopy84Tk8gL1umANOJMHFVkgjiIE13O/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=J52n0vOK4rOGKSKbMWtgzMXaUqY%3D)

<https://honglab.co.kr/>

[honglab

Introduction to Computer Graphics with DirectX 11 - Part 4. Computer Animation Course • 102 lessons [그래픽스 Part4 - 컴퓨터 애니메이션] 파트1,2,3에서 배운 내용들로 이번에는 요소 기술들이 따로따로 작동하도록 구

honglab.co.kr](https://honglab.co.kr/)