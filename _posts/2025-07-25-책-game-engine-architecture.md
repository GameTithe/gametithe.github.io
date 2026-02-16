---
title: "[책] Game Engine Architecture"
date: 2025-07-25
toc: true
categories:
  - "Tistory"
tags:
  - "BSS"
  - "class"
  - "data"
  - "float"
  - "Heap"
  - "memory"
  - "Stack"
  - "virtual"
  - "부동소수점"
  - "컴퓨터 구조"
---

크래프톤 게임 테크랩의 추천(?) 도서여서 읽기 시작했지만,

CS면 CS, Engine이면 Engine

폭 넓고, 깊은 정보를 제공해주는 책이다. 정말 좋은 책인 것같다..!

## 

## **Fundamentals of Software Engineering for Games**

#### 

#### **Data Part**

Data의 표현법

특히 float의 표현 방법에 대해서 매우 상세히 다룬다.

float에 대한 깊은 이해를 하고 싶으 사람은 꼭 읽어보기 바란다.

또한   
데이터 타입에 대해서도 다룬다.

Edian에 대한 개념과, struct,class는 어떻게 edian변환을 하는 지 설명한다.

<https://tithingbygame.tistory.com/236>

[[GameEngineArchitecture] Data, Code and Memory Layout(1)

숫자는 게임 엔진 개발의 중심에 있습니다.모든 소프트웨어 엔지니어는 숫자가 컴퓨터에 의해 어떻게 표현되고 저장되는지를 이해해야 합니다.이 절에서는 책의 나머지 내용을 위해 필요한 기

tithingbygame.tistory.com](https://tithingbygame.tistory.com/236)

#### 

#### **Code Part**

링커가 어떻게 작동하는지, 주의해야 되는 점은 무엇인 지에 대해서 다룬다.

<https://tithingbygame.tistory.com/238>

[[GameEngineArchitecture] Data, Code and Memory Layout(2)

Translation Units Revisited(번역 단위 다시보기)C/C++ 프로그램은 번역 단위(translation unit)로 구성된다. .cpp 파일 하나가 번역 단위가 되며, 컴파일러는 이 파일을 하나씩 따로 번역해서 오브젝트 파일(.o,

tithingbygame.tistory.com](https://tithingbygame.tistory.com/238)

#### 

#### **Memory  Layout part**

컴퓨터가 메모리는 어떻게 구성되어 있고, 데이터를 어떻게 저장하는 지 다룬다.

<https://tithingbygame.tistory.com/239>

[[GameEngineArchitecture] Data, Code and Memory Layout(3)

C/C++ 프로그램의 메모리 레이아웃C나 C++로 작성된 프로그램은 다양한 메모리 영역에 데이터를 저장한다. 저장이 어떻게 할당되고 C/C++ 변수들이 어떻게 동작하는지 이해하려면, 프로그램의 메모

tithingbygame.tistory.com](https://tithingbygame.tistory.com/239)

#### 

#### **Memory Part**

이거 완적 컴퓨터 구조 액기스다.

virtual ~ cache 와  main memory의 관계 등등

찬찬히 읽어보면 많은 도움이 될 것 같다.

<https://tithingbygame.tistory.com/250>

[[GameEngineArchitecture] Memory Architectures

간단한 폰 노이만 컴퓨터 구조에서는, 메모리가 CPU에 의해 동일하게 접근 가능한 동일한 블록으로 취급된다.하지만 실제로 컴퓨터의 메모리는 그렇게 단순하게 설계되는 경우는 거의 없다. 오

tithingbygame.tistory.com](https://tithingbygame.tistory.com/250)

### **Engine Support Systems**

Subsystem start-up, shut-down

서브시스템의 생성, 소멸에 대한 간단한 정리

<https://tithingbygame.tistory.com/253>

[[GameEngineArchitecture] Support Systems Start-Up and Shut-Down

모든 게임 엔진에는 low level support system들을 필요로 합니다. 당연하게 느끼고 있지만, 중요한 작업들을 관리하는 역할을합니다.(엔진의 시작과 종료, 메모리 관리, 게임 기능 설정, 파일 시스템&as

tithingbygame.tistory.com](https://tithingbygame.tistory.com/253)

Memory managment

동적할당에 대한 게임엔진의 태도 ( 스포하면 지양함 )

그리고 이를 피하기 위한 방법들...  상용엔진을 사용하다보면 생각하지 않을만한 부분이지만, 읽어보면 많은 도움이 될 것이다.

<https://tithingbygame.tistory.com/255>

[[GameEngineArchitecture] Memory Management

Memory Management게임 개발자라면 real time으로 게임을 실행시키기 위해서 성능에 대한 신경을 쓰지 않을 수 없다.성능 중에 메모리(RAM)을 어떻게 활용하는 지도 성능에 큰 영향을 끼친다. 1. malloc, new

tithingbygame.tistory.com](https://tithingbygame.tistory.com/255)