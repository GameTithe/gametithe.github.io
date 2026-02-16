---
title: "[GameEngineArchitecture] Memory Management"
date: 2025-08-24
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### 

### **Memory Management**

게임 개발자라면 real time으로 게임을 실행시키기 위해서 성능에 대한 신경을 쓰지 않을 수 없다.

성능 중에 메모리(RAM)을 어떻게 활용하는 지도 성능에 큰 영향을 끼친다.

1. malloc, new와 같은 동적할당은 매우 느린 연산이다. (OS를 호출해서 메모리를 요구하고, 할당하고 등등의 이유로) 그렇기 때문에 custom allocator를 사용해 성능을 개선할 필요가 있다.

2. 데이터는 cache hit의 연유로 cache line 크기 내에 원하는 데이터들이 있으면 성능이 좋을 수 밖에 없다. 동적할당은 이를 무시하고 비어있는 공간에 할당하기 때문에 이런 이점을 얻기 어렵다.

### 

### **Optimizing Dynamic Memory Allocation**

malloc과 free, new와 delete 연산자 (heap allocators )를 통한 동적 메모리 할당은 매우 느리다.

**느린 대표적인 이유**

1. heap allocator는 범용 기능으로 1바이트에서 1GB에 대한 동적할당 요청을 모두 처리할 수 있어야하기 때문에 많은 오버헤드를 수반한다.

2. 대부분의 운영체제에서 heap allocators(malloc, new, delete, free) 호출은 먼저 사용자 모드에서 커널 모드로 context switch해서 요청을 처리하고, 다시 사용자 모드로 돌아와야 하는데,

이 과정에서의 contex switch의 비용은 굉장히 크다.

게임 개발에서 자주 따르는 경험적 규칙은 다음과 같다:

**힙 할당을 최소화하라. 그리고 절대 tight loop(빠르게 반복되는 루프) 안에서 힙 할당을 하지 마라.**

그러한 이유들로 게임 개발에서의 암묵적인 룰이 있다.

1. 힙 할당을 최소로하자

2. 절대로 빠르게 반복되는 loop안에서는 동적할당을 하지 마라

당연히 동적할당을 완전히 피할 수는 없을 것이다. 피할 수 없으면 즐겨라!! custom allocator를 구현해서 사용하면 된다...!

custom allolcator가 더 좋을 수 있는 이유는 아래와 같다.

1. custom allocator는 미리 할당된 메모리 블록을 사용해서 사용자의 요청을 충족시킬 수 있다. 이렇게 하면 커널모드로 들어갈 필요 없이 사용자 모드에서 사용자의 요구를 처리할 수 있기 때문에 컨텍스트 스위칭 비용을 완전히 피할 수 있다.

(메모리를 할당하는 최초 1회에서는 context switch가 발생할 것이다.)

2. 범용적인 것 1개만 사용하는 것이 아니라, 사용 패턴에 따라 여러 가지 가정을 세울 수 있다. 덕분에 custom allocator는 효율적으로 동작할 수 있을 것이다.

이후 섹션에서는 일반적인 커스텀 할당자들의 종류를 살펴본다. 이 주제에 대한 추가 자료는 Christian Gyrling의 훌륭한 블로그 글을 참고하라

<https://www.swedishcoding.com/2008/08/31/are-we-out-of-memory/>

[Are we out of memory?

<!-- ← GDC Presentation – Creating a Character in Drake’s Fortune Book Review: Game Engine Architecture → --> Are we out of memory? August 31st, 2008 by swedishcoding\_1ggc23 — Game Coding — No Comments If I had a dollar every time I heard the q

www.swedishcoding.com](https://www.swedishcoding.com/2008/08/31/are-we-out-of-memory/)

더보기

=> 간단하게 요약하면, new / delete를 커스텀해서 사용하자

=> 정렬해서 사용하자 (1. 하드웨어 성능/제약 2. 캐시라인 정렬로 cache hit을 노리자 )  
=> new를 자주하지 않기 위해 미리 크게 new를 하고, 그 안에서 사용하자

![](https://blog.kakaocdn.net/dna/4A7vK/btsPWoKeyoU/AAAAAAAAAAAAAAAAAAAAAGk3PRPKJ2R0GfQfIFNjpr1P7gwaoDcbk8s_nT9G1BW7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=alpVp%2Bst3kN6ckLnMg15TNBhTWg%3D)

persistent: 한 번 할당 후에는 종료할 때 delete할 객체들

Dynamic: 객체 new/delete가 예측 불가

one-frame: 한 프레임이 끝날 때 한번에 폐기 처분

### 

### **Stack-Based Allocators**

많은 게임들은 메모리를 stack 방식으로 할당한다.

stack allocator 는 구현이 아주 간단하다. 큰 연속적 메모리 블록을 malloc 이나 전역 new 로 할당하거나, 혹은 전역 바이트 배열을 선언해서 할당한다(이 경우 메모리는 실행 파일의 **BSS 세그먼트** 에서 할당될 것이다.) 그리고 stack의 top을 가리키는 포인터를 유지하면 된다.

![](https://blog.kakaocdn.net/dna/x8WPz/btsPWjic8Il/AAAAAAAAAAAAAAAAAAAAAKX4PaaY802ZfzCBMLyo9SWPJe3msUw6_5bfMnaTu7az/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GZeLFIawWM3Ut7yVzZZKVV%2FJ5bk%3D)

stack allocator에서는 메모리를 임의의 순서로 해제할 수 없다. 모든 해제는 반드시 할당된 순서의 반대로만 수행되어야 한다.

할당을 해제하는 방법으로는 메모리를 새로 할당하기 전에 marker로 기록을 하고, 메모리를 할당해준다.

그리고 메모리를 해체할 때 top ~ marker 사이를 할당해제하는 것이다. ( 해제하고 top의 위치를 marker로 되돌리는 것을 잊지말자)

### 

### **Double-Ended Stack Allocators**

하나의 메모리 블록에는 실제로 두 개의 stack allocator를 포함시킬 수 있다.

하나는 블록의 아래쪽에서 위로 , 다른 하나는 블록의 위쪽에서 아래로 메모리를 할당한다.

![](https://blog.kakaocdn.net/dna/bxeVsF/btsPXxzZw2b/AAAAAAAAAAAAAAAAAAAAANT58ZErAyEnMLh0ZT_1AW9h9Fy4WpSX5nR5J9VXa5f9/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=PkI7QoyDrTn9MvQYMfOILTxV9QU%3D)

이중 스택 할당자는 메모리 효율성을 높일 수 있는데, 그 이유는 아래쪽 스택의 메모리와 위쪽 스택의 메모리가 공유되고 있기 때문이다.

(일반적인 stack allocator가 50MB의 메모리를 가지고 있을 때  70MB를 요청받으면 70MB이상을 가지고 있는 allocator를 새로 만들어야할 것이다.

하지만 double-ended stack allocator는 50MB 2개가 붙어있고, 70MB요청을 받으면 한 쪽에서는 70MB를 사용하고, 다른 한쪽에서는 30MB를 사용하면 되기 때문에 메모리 효율성이 높다고 하는 것이다.)

즉, 두 스택 중 하나가 훨씬 많은 메모리를 사용하더라도, 두 스택의 총 메모리 사용량이 블록 전체 크기를 넘지만 않으면 모든 할당 요청을 만족시킬 수 있다.

Midway의 Hydro Thunder 아케이드 게임에서 double ended stack allocator를 아래와 같이 사용하였다.

Lower stack은 레벨을 로드하거나 언로드할 때 사용되었고,

Upper stack은 매 프레임마다 할당되고 해제되는 임시 메모리 블록에 사용되었다.

이 메모리 할당 방식은 매우 효과적이었으며, 메모리 단편화(memory fragmentation) 문제를 전혀 겪지 않았다고 한다.

### 

### **Pool Allocators**

게임 엔진 프로그래밍에서는 동일한 크기의 작은 메모리 블록(iterator, link 등)을 많이 할당하는 일이 매우 빈번하고, 이 때 pool allocator가 유용하다.

Pool Allocator는 먼저 큰 메모리 블록을 미리 할당하는데, 이 블록의 크기는 할당할 element들의 크기의 정수배로 설정한다. (동일한 크기의 메모리 블럭들을 사용한다고 가정했으니)

Pool 안의 각 요소는 모두 free element의 연결 리스트에 추가된다.

초기에는 모든 pool의 element들은 free element 연결 리스트에 할당될 것이다.

메모리 할당 요청이 들어오면, free element list에서 메모리를 꺼내주면되고,

메모리 해제 요청이 들어오면 free element list에 연결해주면 된다.

(메모리 할당/해제 모두 time complexity는 O(1)이다.)

그렇다면 **memory pool에서 free인 부분은 어떻게 관리해야될까?**

free입니다!! 라는 배열이나 열결리스트를 만들어서 따로 보관해야될까?

그렇게 하면 보관하는 공간을 새로 할당해야되고, 낭비로 이어질 것이다.

그렇게 하지말고, 어차피 free인 부분은 안에 어떤 데이터가 있던지 신경쓰지 않아도 된다. 그러니 연결리스트처럼 next pointer하나를 할당해서 free들을 linked list로 만들어주면 메모리 낭비 없이 보관할 수 있다.

단, free node 한개에 pointer 1개가 저장될 공간이 있어야한다는 조건이 생긴다.

만약 free node의 크기가 16bit(2byte)라면 ( 64bit 환경이여서 pointer를 저장하지 못하는 것을 의미), 포인터 대신 인덱스(uint16자료형을 사용하면 된다)를 저장하는 방법을 사용할 수 있다.

단, 이런 상황에서 pool의 크기는 2^16 element를 넘어서는 안된다.

본인이 헷갈렸던 부분

더보기

=> free list 를 따로 안만든다고 했는데, 지금 할당된 데이터가 free list여서 다음 노드의 pointer 값인지 실제 데이터 값인 지 어떻게 구별한다는 거지 라는 의문이 들었다.

결론 여기서 말하는 free list를 따로 만들지 않는다는 의미를 새로운 공간을 할당해서 관리하지 않는다는 것이고,

free list node 자체는 존재한다는 것이다.

사실 시작지점만 만들고 여기에 연결되는 것은 free list입니다 라고 하면 다 해결된다.

### 

### **Aligned Allocations**

모든 변수와 데이터 객체에는 정렬 요구사항이 있다.

1. 8bit(1byte) 정수 변수는 어느 주소에든 배치될 수 있다.

2. 32bit(4byte) 정수나 부동소수점 변수는 반드시 4byte 정렬되어야 한다. 그러므로 주소가 0x0, 0x4, 0x8, 0xC로 끝나야 한다.

3. 128bit SIMD 벡터 값은 일반적으로 16byte 정렬이 필요하므로, 주소는 0x0에서만 끝나야 한다.

모든 메모리 할당자는 정렬된 메모리 블록을 반환할 수 있어야 한다.

구현 방법

1. 실제 요청보다 약간 더 큰 메모리를 할당한다. (정렬을 위해서 align -1 을 더해서 할당해준다.)

2. 원하는 크기보다 크고, 정렬된 상태의 메모리 주소를 반환한다.

3. 최소한 요청보다 메모리를 더 확보했기 때문에, 올려 조정한 뒤에도 블록 크기는 여전히 충분하다.

대부분의 구현에서는 추가로 할당하는 바이트 수가 (정렬 크기 – 1)인데, 이는 최악의 경우 필요한 정렬 이동량이다.

```
// 주어진 주소를 위로 올려서 원하는 바이트 정렬에 맞추기
inline uintptr_t AlignAddress(uintptr_t addr, size_t align)
{
	//addr이상인 align 중에서 가장 작은 값을 구하는 연산 
    const size_t mask = align - 1;
    
    // align은 2의 제곱수 ( 하나의 비트만 1인 상태 )
    // mask는 align - 1 ( align = 0b1000이면, mask=  0b0111)     
    assert((align & mask) == 0); // align은 2의 제곱 수 일 때를 의미한다.
  	
    return (addr + mask) & ~mask;
    // (addr + mask) & align은 안된다.
    // 이건 align값과 같은 비트 위치만 남기게 된다.
}

// 주어진 포인터를 위로 올려 원하는 바이트 정렬에 맞추기
template<typename T>
inline T* AlignPointer(T* ptr, size_t align)
{
    const uintptr_t addr = reinterpret_cast<uintptr_t>(ptr);
    const uintptr_t addrAligned = AlignAddress(addr, align);
    return reinterpret_cast<T*>(addrAligned);
}

// 정렬된 메모리 할당 함수. 'align'은 반드시 2의 제곱수여야 함 (예: 4, 8, 16).
void* AllocAligned(size_t bytes, size_t align)
{
    // 최악의 경우 필요한 바이트 수 계산
    // bytes가 align + 1일 떄가 최악이다. 
    size_t worstCaseBytes = bytes + align - 1;

    // 정렬되지 않은 블록을 먼저 할당
    U8* pRawMem = new U8[worstCaseBytes];
    // 정렬된 포인터 반환
    return AlignPointer(pRawMem, align);
}
```

### 

### **Freeing Aligned Blocks**

정렬된 블록이 나중에 해제될 때는, 우리가 받는 주소는 실제로 할당된 원래 주소가 아니라 정렬된 주소다.

하지만 메모리를 해제하려면 실제로 new가 반환했던 원래 주소를 해제해야 한다

(메모리를 정렬하면서 메모리 시작 위치가 바뀔 수 있음 그렇기 때문에 new한 메모리 주소로 delete를 해줘야됨)

원래 주소를 받기 위한 간단한 방법은 정렬된 주소와 원래 주소 간의 차이를 free 함수가 찾을 수 있는 곳에 저장해 두는 것이다.

AllocAligned()에서 우리는 정렬을 위해 약간의 여유 공간을 두기 위해 align-1 바이트를 추가로 할당하는데 이 추가 byte 공간에shift 값을 저장하면 된다.

![](https://blog.kakaocdn.net/dna/LHPpe/btsP4g5Tk4I/AAAAAAAAAAAAAAAAAAAAAL32RrBqdkpd0BnsjSNfEFj8KZh7vgyc81TG6ZlMm3FE/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=0fN4tdYaLAORLL%2F%2BXNsr6yOCjes%3D)

우리가 만드는 가장 작은 shift는 1바이트이니, shift 값을 1byte로 저장하면 된다.된다.

하지만 문제가 하나 있다.

new가 반환한 원래 주소가 정렬되어 있었다면, align - 1을 더한 공간이 다시 해제되고, 1byte라는 추가 공간이 없어진다.

(할당하는 코드를 이해했다면, 이 말도 무슨 말인지 알겠죠..?)

이를 해결하기 위해,  align-1을 더하는게 아니라 align을 더해주면 된다.

이럴 경우 정렬된 상태의 byte를 할당하게 되어도, aling byte만큼 크게 공간을 잡게 될 것이다.

최종 적으로 1~align 크기 만큼 offset을 설정하게 되는 것이다.

다음은 수정된 AllocAligned()와 이에 대응하는 FreeAligned() 구현이다.

```
// 정렬된 메모리 할당 함수. 'align'은 반드시 2의 제곱수여야 함 (예: 4, 8, 16).
void* AllocAligned(size_t bytes, size_t align)
{
    // 필요한 크기보다 'align' 바이트 더 할당.
    size_t actualBytes = bytes + align;

    // 정렬되지 않은 블록을 할당.
    U8* pRawMem = new U8[actualBytes];

    // 블록을 정렬. 이미 정렬된 경우에도
    // 항상 'align' 바이트만큼 위로 올려서
    // shift를 저장할 공간을 확보한다.
    U8* pAlignedMem = AlignPointer(pRawMem, align);
    if (pAlignedMem == pRawMem)
        pAlignedMem += align;

    // shift 값을 계산하고 저장한다.
    // (256바이트 정렬까지 동작 가능)
    ptrdiff_t shift = pAlignedMem - pRawMem;
    assert(shift > 0 && shift <= 256);

    pAlignedMem[-1] = static_cast<U8>(shift & 0xFF);
    return pAlignedMem;
}

void FreeAligned(void* pMem)
{
    if (pMem)
    {
        // U8 포인터로 변환.
        U8* pAlignedMem = reinterpret_cast<U8*>(pMem);

        // shift 값을 추출.
        ptrdiff_t shift = pAlignedMem[-1];
        if (shift == 0)
            shift = 256;

        // 원래 할당된 주소로 되돌아가서 삭제.
        U8* pRawMem = pAlignedMem - shift;
        delete[] pRawMem;
    }
}
```

### 

### **Single-Frame Allocator & Doubled-Buffered Allocator**

게임 엔진에는 game loop가 한 번 도는 동안에만 사용되는 데이터가 존재할 것이다.

이 데이터는 루프가 끝나면 버려지거나, 바로 다음 프레임에서만 사용된 뒤 버려질 것이다.

이런 할당 패턴은 너무나 흔해서, 많은 엔진들이 single-frame 또는 double-buffered allocator를 지원한다.

#### 

#### **Single-Frame Allocators**

단일 프레임 할당자는 메모리 블록을 예약하고, 이를 단순 stack allocator로 관리하는 방식으로 구현된다.

1. 각 프레임의 시작 시, stack allocator를 clear해준다.

2. 프레임 중에 이루어진 할당은 블록의 상단을 향해 커진다.

다시

1. 각 프레임의 시작 시, stack allocator를 clear해준다.

2. 프레임 중에 이루어진 할당은 블록의 상단을 향해 커진다.

이렇게 반복되어진다.

```
StackAllocator g_singleFrameAllocator;

// 메인 게임 루프
while (true)
{
    // 매 프레임마다 단일 프레임 할당자의 버퍼 초기화
    g_singleFrameAllocator.clear();

    // ...
    // 단일 프레임 버퍼에서 할당. free 필요 없음!
    // 단, 반드시 이 프레임 안에서만 사용해야 한다.
    void* p = g_singleFrameAllocator.alloc(nBytes);
    // ...
}
```

**장점**

메모리를 개별적으로 free할 필요없이 allcoator 전부를 clear한다.

매 프레임 시작 시 전체가 초기화되므로 매우 빠르다.

**단점**

프로그래머의 규칙(discipline)이 필요하다.

단일 프레임 버퍼에서 할당된 블록은 현재 프레임까지만 유효하다. 해당 프레임을 넘어서 포인터를 캐싱해서는 안 된다.

#### 

#### **Double-Buffered Allocators**

doubled-buffered allocator는 i frame 에서 할당된 메모리를  i+1 frame 까지 사용할 수 있도록 허용한다.

이를 위해 크기가 같은 single-frame allocator 두 개를 만든 뒤, 매 프레임마다 두 버퍼를 번갈아 사용한다.

```
class DoubleBufferedAllocator
{
    U32 m_curStack;
    StackAllocator m_stack[2];

public:
    void swapBuffers()
    {
        m_curStack = (U32)!m_curStack;
    }

    void clearCurrentBuffer()
    {
        m_stack[m_curStack].clear();
    }

    void* alloc(U32 nBytes)
    {
        return m_stack[m_curStack].alloc(nBytes);
    }
    // ...
};

DoubleBufferedAllocator g_doubleBufAllocator;

// 메인 게임 루프
while (true)
{
    g_singleFrameAllocator.clear();

    // 더블 버퍼의 활성/비활성 버퍼 교환
    g_doubleBufAllocator.swapBuffers();

    // 이제 활성화된 버퍼를 초기화, 이전 프레임의 데이터는 그대로 둔다
    g_doubleBufAllocator.clearCurrentBuffer();

    // ...
    // 현재 버퍼에서 할당. 이전 프레임 데이터는 건드리지 않는다.
    // 단, 이 데이터는 이번 프레임 또는 다음 프레임까지만 사용해야 한다.
    void* p = g_doubleBufAllocator.alloc(nBytes);
    // ...
}
```

### 

### **Memory Fragmentation**

동적 힙 할당의 또 다른 문제는 시간이 지나면서 메모리가 단편화될 수 있다는 점이다.

![](https://blog.kakaocdn.net/dna/vuLez/btsP5vBKPJT/AAAAAAAAAAAAAAAAAAAAAO0mBVemaYfWKwFhCypL36U5-D4B-Wrsim-XYKMc7mih/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=B8EgoZ4W1DaCUGNSRA0FTjI4nW8%3D)

메모리 단편화의 문제는 메모리를 할당할 수 있는 공간에 있음에도 할당에 실패할 수 있다는 것이다.

문제의 핵심은, 할당되는 메모리 블록은 항상 연속적이어야 한다는 것이다

메모리 단편화는 가상 메모리를 지원하는 운영체제에서는 그다지 큰 문제가 되지 않는다. 가상 메모리 시스템은 페이지(pages)라고 알려진 비연속적인 물리 메모리 블록들을 가상 주소 공간에 매핑하여, 애플리케이션에는 그 페이지들이 연속적으로 보이게 한다. 물리 메모리가 부족할 때, 오래된(stale) 페이지들은 하드 디스크로 스와핑(swap)될 수 있으며, 필요할 때 다시 디스크에서 로드된다.

대부분의 임베디드 시스템은 가상 메모리 시스템을 구현할 여유가 없다. 일부 최신 콘솔은 기술적으로 이를 지원하긴 하지만, 대부분의 콘솔 게임 엔진은 본질적인 성능 오버헤드 때문에 여전히 가상 메모리를 사용하지 않는다.

#### 

#### **Avoiding Fragmentation with Stack and Pool Allocators**

메모리 단편화의 해로운 영향을 stack allocator 또는 pool allocator를 사용하여 피할 수 있다.

**stack allocator**는 단편화에 영향을 받지 않는다. 왜냐하면 할당은 항상 연속적이고, 블록은 할당된 순서의 반대 순서로 해제되어야 하기 때문이다.

![](https://blog.kakaocdn.net/dna/bolnng/btsP4s6Efii/AAAAAAAAAAAAAAAAAAAAAE0tH1MxnxMylN0xknmiCRYolr0w_iray7bwJIIyy7BA/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=OX4p5XIN1XqphlrmNMVRvSqOTc0%3D)

**pool allocator**또한 단편화 문제로부터 자유롭다.

pool에서 사용되는 block 내부에서는 단편화되긴 하지만, 일반 목적의 힙에서처럼 단편화 때문에 할당할 수 있는 공간이 있음에도 out of memory가 발생하지는 않는다.

![](https://blog.kakaocdn.net/dna/d4fRwU/btsP4h5hMmr/AAAAAAAAAAAAAAAAAAAAAGoVLaz3MkMZ8t9ME2EQjVl99UVSVyypjVeUa_y6fWvn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=S9j0EFuLicwlR0uXUCLcGsbHBZg%3D)

### 

### **Defragmentation and Relocation**

stack allocator은 할당/해제 순서를 무작위로 설정할 수 없다.

pool allocator는 서로 다른 크기의 객체(메모리) 사용할 수 없다.

이러한 경우에는, 힙을 주기적으로 defragment(조각 모음)함으로써 단편화를 피할 수 있다.

defragment는 더 높은 메모리 주소에 있는 할당된 블록들을 더 낮은 주소로 **이동**시켜 힙의 모든 빈 “구멍”들을 하나로 합치는 작업을 포함한다(이렇게 하면 구멍들은 더 높은 주소로 “밀려 올라간다”).

간단한 알고리즘 하나는 첫 번째 “구멍”을 찾은 다음, 그 구멍 바로 위에 있는 할당된 블록을 구멍의 시작 지점으로 아래로 이동시키는 것이다. 이렇게 하면 그 구멍이 더 높은 메모리 주소로 “거품처럼 위로 떠오르게(bubbling up)” 되는 효과가 생긴다. 이 과정을 반복하면, 결국 모든 할당된 블록들이 힙 주소 공간의 하단(low end)에 있는 연속적인 메모리 영역을 차지하게 되고, 모든 구멍들은 힙의 상단(high end)으로 떠올라 하나의 큰 구멍으로 합쳐지게 된다. 이는 그림 6.7에 나와 있다.

![](https://blog.kakaocdn.net/dna/0aGwc/btsP28A42tH/AAAAAAAAAAAAAAAAAAAAAPTkDzxS9Ir4U_BGVCajR_0T_si9L_Je6Gu-rxUvvT6P/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=LfOrYPy99CFwHfGOQQiKOve2H8w%3D)

위에서 설명한 메모리 블록의 이동 자체를 구현하는 것은 특별히 까다롭지 않다. 까다로운 점은, 우리가 할당된 메모리 블록들을 이리저리 옮기고 있다는 사실을 감안해야 한다는 점이다. 누군가가 이들 할당된 블록 중 하나의 내부를 가리키는 포인터를 가지고 있다면, 그 블록을 이동시키는 순간 그 포인터는 무효가 된다.

안타깝게도, 어떤 특정 메모리 영역을 가리키는 모든 포인터를 찾아낼 수 있는 범용적인 방법은 없다. 따라서 게임 엔진에서 메모리 defragment를 지원하려면, 프로그래머들이 재배치를 해줘한다. 이를 위해서 스마트 포인터나 핸들를 사용해야 한다.

**스마트 포인터**는 포인터를 담고 있으며, 대부분의 의도된 목적에 대해 포인터처럼 동작하는 작은 클래스이다. 클래스이기에 메모리 재배치를 올바르게 처리하도록 코드를 작성할 수 있다.

한 가지 접근은 모든 스마트 포인터가 자신을 전역 연결 리스트에 등록하도록 하는 것이다.

heap 내에서 어떤 메모리 블록이 이동될 때,

모든 스마트 포인터의 연결 리스트를 훑으면서,이동된 블록을 가리키는 각 포인터를 조정된 만큼(이 값은 알겠지) 적절하게 조정할 수 있다.

**핸들**은 보통 이동 불가능한(non-relocatable) 테이블에 대한 **인덱스**로 구현된다.

그 테이블 자체에 실제 포인터들을 담고 있다. 할당된 블록이 메모리에서 이동되면, 핸들 테이블을 훑어 관련된 모든 포인터를 찾아 자동으로 갱신할 수 있다.

#### 

#### Amortizing Defragmentation Costs

defragmentation은 메모리 블록을 복사하는 작업을 포함하기 때문에 느릴 수 있다.

하지만 heap 전체를 한번에 defragmentation할 필요는 없다. 이를 분산하면 된다. 초당 30frame의 게임이라면 각 프레임은 1초에 30번 그려질 것이고, 한 프레임당 8-16 같은 작은 수의 block만 defragment해도 대부분 1초 이내에 완전이 deframgmentation 작업이 끝날 것이다.

(deframgmentation은 동적 게임 오브젝트에만 적용 될 것이니, 그 절대 크기는 작을 것이다. 그러니 대부분 1초 안에 해결될 것이다.)