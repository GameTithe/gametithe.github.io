---
title: "[C++/EffectiveC++] Lets go CONST, const, CoNsT"
date: 2024-11-23
toc: true
categories:
  - "Tistory"
tags:
  - "오블완"
  - "티스토리챌린지"
---

const와 \*표시의 상대적인 위치에 따라 의미를 파악할 수 있다.

**const \* : 포인터가 가리키는 대상이 상수**

**\* const : 포인터 자체가 상수**

```
char greeting[] = "Hello"
```

상수 포인터, 비상수 데이터

```
char * const p = greeting​
```

상수 포인터, 상수 데이터

```
const char * const p = greeting
```

상수데이터, 비상수 포인터

```
const char *p = greeting;
```

참고로 const 위치가 살짝 다르긴하지만, 두 줄의 의미는 동일하다.

### **Iterator**

**Iterator에 const를 붙인다면 상수 포인터로 작동한다.**

가리키는 대상을 바꿀 수 없다. (상수 포인터, \* const)

하지만 가리키고 있는 대상의 값을 바꾸는 것은 가능하다. (비상수 데이터)

```
std::vector<int> vec;

const std::vector<int>::iterator it = vec.begin()

*it = 10;	//가능
it++		//불가능
```

혹시  **상수 데이터가** 필요하다면 **const\_iterator**를 사용할 수 있다.

```
std::vecotr<int>::const_iterator cit = vec.begin();

*cit = 10;	//불가능
*cit++; 	//가능
```

책에서는 const를 가능하다면 항상 사용하라고 조언하고 있다.

우리의 실수로 코드를 잘 못짜는 상황이 생겨도, const가 우리를 보좌해줄 것이라고... ㅎ..ㅎ

### **상수멤버함수**

상수함수가 중요한 이유가 2가지가 있다.

**1. 사용자가 인터페이스를 이해하기 쉽다.**

const가 붙은 것은 값을 조정하면 안되는구나~

const가 없으니 값을 조정해도 되는구나~

**2. 상수객체에 대한 참조자 (reference-to-const)**

```
class TextBlock
{
	public:
    
    ...
    
    const char& operator[] (std::size_t position) const
    { return text[position]; }
    
    char& operator[] (std::size_t position) const
    { return text[position]; }
    
    private:
    std::string text
}

void print(const TextBlock& ctb)
{
	std::cout << ctb[0];
    ...
}

std::cout << tb[0];

tb[0] = 'x';

std::cout << ctb[0];

ctb[0] = 'x'; // TextBlock 객체에 대한 쓰기는 불가능
```

**(operator 제일 뒤의 const 때문에****ctb가  const operator로 작동한다. )**

ctb[0] = 'x'가 에러가 생기는 이유는

단순히 const에 접근하기 때문이다.

객체를 읽을 수만 있고, 쓸 수는 없다.

### 

### **const에는 bitwise constness(비트수준 상수성), 논리적 상수(logical constness)가 있다.**

#### **Bitwise Constness**

우리가 아는 기본적인 const입니다. bit단위로도 절대로 바뀌지 않아야하고, 바뀌지 않는 것입니다.

#### 

#### **Logical Constness**

모종의 이유로 string을 사용하지 않고 char형을 사용했다고 해보자.

그리고 operator[]도 오버로딩을 했다. ( 하지만 틀린 문법... char& 앞에 const가 있어야 된다.)

```
class CTextBlock
{
public:
	...
    
   char& operator[] (std::size_t position) const
    { return pText[position]; }
    
private:
	char* pText;
}
```

그리고 이렇게 코드가 진행됐다고 해보자.

```
const CTextBlock cctb("Hello");

char *pc = &cctb[0];

*pc = 'J';
```

\*pc = &cctb[0];에서

상수버전의 operator[]를 호출하여 cctb의 내부 데이터에 대한 포인터를 얻는다.

그리고 J로 바꾼다. ..!

이런 상황 때문에 논리적 상수성이라는 개념이 등장했다.

**객체의 한 비트도 수정을 못하는 것이 아니라, 일부 몇 비트는 바꿀 수 있되, 사용자 측에서 알아채지 못하면 상수 자격이 있다! 라고...;**

```
class CTextBook
{
public:
	...
    
    
    std::size_t length() const;
    
private:
	char* pText;
    std::size_t textLength;
    bool lengthIsValid;
}

std::size_t CTextBook::length() const
{
    if(!lengthValid)
    {
    	textLength = std::strlen(pText);
        lengthIsValid = true;
    }
    
    return textLength;
}
```

**length() 함수는 상수함수이다! 그렇기 때문에 함수 내부에서 값을 변경할 수 없다.**

**하지만 length() 함수는 바꾸지 않고 구현할 수가 없다.**

**이때 혜성같이 등장한 "mutable"**

```
class CTextBook
{
public:
	...
    
    
    std::size_t length() const;
    
private:
    char* pText;
    mutable std::size_t textLength;
    mutable bool lengthIsValid;
}

std::size_t CTextBook::length() const
{
    if(!lengthValid)
    {
    	textLength = std::strlen(pText);
        lengthIsValid = true;
    }
    
    return textLength;
}
```

**mutable을 비정적 데이터 멤버의 비트수준 상수성의 족쇄를 풀어준다!**  
 **이제 const 함수 안에서 값을 변경할 수 있다!**