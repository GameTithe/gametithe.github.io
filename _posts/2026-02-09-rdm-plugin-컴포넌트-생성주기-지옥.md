---
title: "[RDM Plugin] 컴포넌트 생성주기 지옥"
date: 2026-02-09
toc: true
categories:
  - "UE5_Plugins"
tags:
  - "UE5_Plugin"
---

### 핵심

언리얼은 대규칙(?)은 값이 변경되면 해당 Actor,Comp를 삭제 후 값을 변경한 상태에서 재생성합니다.

### 문제상황

![](https://blog.kakaocdn.net/dna/bkwkuj/dJMcabQosdB/AAAAAAAAAAAAAAAAAAAAAOA_HyvpXpP_kt_4BPzysTGTVL_jbz6oy5C1_ZAsBF82/img.gif?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3b9cUbLBjtMtL7xk5Bq0YQUkSE4%3D)

 여기서부터 시작된 디버깅의 시간...

Source Static Mesh를 Detail Panel에서 수정해도 반영이 안되는 버그까지...

![](https://blog.kakaocdn.net/dna/cBSEvL/dJMcad1HX2O/AAAAAAAAAAAAAAAAAAAAAMzLhuvizvJGdx0hRy--e_vYIc12lp03ihyj2TK69Wbs/img.gif?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9N%2FOeqOnnlXa8ywCdHbaE5mqkj0%3D)

### 문제 원인

Blurprint Actor 에 붙은 컴포넌트의 Property를 에디터에서 변경하면 RerunConstructionScripts -> re-instancing이 발생하게 된다.

이 과정에서

1. CDO(Class Default Object)로 새 컴포넌트를 생성

2. OnRegister에서 CDO의 SourceMesh로 초기화하게 된다.  

3. 그리고 그 Source Mesh로 생성되게 된다. 

순서를 보면,

  1. GetComponentInstanceData() 호출   
     => 컴포넌트 삭제 전에 변경된 값 저장   
  
  2. 컴포넌트 삭제   
  
  3. CDO에서 새 컴포넌트 생성   
     => SourceStaticMesh에 기본값 할당  
  
  4. OnRegister #1   
     => 기본값으로 초기화    
   
  5. ApplyToComponent() 호출   
     => 저장해둔 값(Stopway)으로 복원   
     => ReregisterComponent() 호출 (내부적으로)   
  
  6. OnRegister #2   
     => 복원된 값으로 다시 등록

![](https://blog.kakaocdn.net/dna/byGZEn/dJMcaiIJnvs/AAAAAAAAAAAAAAAAAAAAAOMDh06m0y5XgQ_Kjmi0cSZ9IjShLR8Sf3wf1-zrKHzU/img.gif?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=a6gRnkjoR9e2lKYPlJe8FuyjPWc%3D)

(이제 Mesh 변경도 잘됩니다.)