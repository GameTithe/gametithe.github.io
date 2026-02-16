---
title: "[C++] virtual function( 생성자와 소멸자 )"
date: 2024-10-31
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

아래의 코드 구조는

Character class와 Characetr를 상속받은 Knight class가 있다.

각각의 클래스에는 Attack함수가 있고, main에서 Character의 Attack과 Knight의 Attack을 호출했다.

![](https://blog.kakaocdn.net/dna/bBpGBo/btsKqWLKGI4/AAAAAAAAAAAAAAAAAAAAAHWpjQM1aPZ2DGDpyPCIYEU6qrXuEIVLAW2anEewWNNk/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hxc5n6xugV2rI9Fsn8czS4%2FGbmk%3D)

![](https://blog.kakaocdn.net/dna/b5lD7L/btsKqnXlVHj/AAAAAAAAAAAAAAAAAAAAAGIVzrZBlnFbbM4OhqxRlnWuyjQ_uBrmiQyz7K66Vwf-/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=11Su5S2pJWFOshbXIxA4gTSMAzo%3D)

1. Character가 만들어질 때 Chatacter Constructor만 호출된다.

2. Knight가 만들어질 때 Character, Knight  Constructor가 호출된다.

3. 각 클래스에서 만들어진 Attack이호출된다.

4. Knight가 소멸자가 호출 될 때 Knight, Character  Constructor가 호출된다.

### 

### 여기까지는 예상가능한 결과들이다.

그렇다면 이렇게 변경되면 어떨까

p1,p2 모두 Character로 선언하고, new를 할 때 p2를 Knight로 해줬다.

![](https://blog.kakaocdn.net/dna/w41pB/btsKrcOkIQn/AAAAAAAAAAAAAAAAAAAAAKqXrD4kn6Njf-IEzgpXOkpnujCFnZPb7vsOccTSPh0T/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KA%2FqtwOJeKcEXBBcwLF8Sb5U1nU%3D)

![](https://blog.kakaocdn.net/dna/Rjszy/btsKpj9v33W/AAAAAAAAAAAAAAAAAAAAAHunOGbIR2m1nd3UnNqY21l8KhDh7u4JXYSysmdt83p3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FHzjwuMfxxM9EpARaDO7HZuytHk%3D)

p2는 Knight이지만 Characetr의 Attack이 호출된다. 그 이유는 컴파일을 할 때 p2는 Character이니 Character Attack을 호출하는 것이다. 하지만 런타임에서는 p2는 Knight가 된다.  
  
이것을 컴퓨터에게 알려주는게 Virtual이다.

![](https://blog.kakaocdn.net/dna/cNjFti/btsKp7N4npo/AAAAAAAAAAAAAAAAAAAAACgBtowPQE9Zse6CYhrd2-8QSfrIG_nPBXPHCpZIiCca/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=RXSa9%2ByR2sc9FfmvFfmyny1FNyU%3D)
![](https://blog.kakaocdn.net/dna/bcGGal/btsKp62GE0d/AAAAAAAAAAAAAAAAAAAAAGFW90JQp8i2H6ci3rIxm-x2dTUb9dJLeVXVZeZTjsNw/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GSurDPhAdbR9Pr1h3OMcUfdeddM%3D)
![](https://blog.kakaocdn.net/dna/dfIiGN/btsKpjaCuGt/AAAAAAAAAAAAAAAAAAAAALRcbL0k34XIlr0ZgcllZLWyIUjsq76oUBagCzlDFVsS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=wGm78RJJ5FBV1LmLE93h2TQCcMM%3D)

이렇게 함수 앞에 Virtual 키워드를 붙혀준다면 우리가 의도한대로 작동한다.

### 

### **소멸자**

**이제 소멸자를 살펴보자**

main코드가 아래와 같다면

**생성자 2번이 호출이 되니, 소멸자도 2번이 호출되는 것이 정상적인 흐름일 것이다.**

하지만 아래와 같이 **소멸자는 character 소멸자만 호출된다.**

![](https://blog.kakaocdn.net/dna/b3of4G/btsKulfo6k7/AAAAAAAAAAAAAAAAAAAAALg0WuUeKLMIEALmvE948ZrSqKw6qMrIEI8hZ1AjYFoX/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FZmXTD%2BKK%2BNpuojShRoVcRhJ1Co%3D)![](https://blog.kakaocdn.net/dna/0AV1v/btsKwlkxjR9/AAAAAAAAAAAAAAAAAAAAAFscdnJTvKlCsCuebNFc7Q8JwpYxsaVcnOtF601047JB/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GQJy7f%2FxDiFe1L5ytVg0Su3Jw8M%3D)

**그 이유는 어떤 소멸자를 호출할지는 컴파일단에서 결정한다. p1의 데이터 타입이 Character이기 때문에 p1소멸자로 Character 소멸자가 호출이된다.**

그렇기 떄문에 런타인에서 소멸자 주소를 판별할 수 있도록 virtual 키워드를 붙혀주자.

![](https://blog.kakaocdn.net/dna/bfXG0J/btsKwouFhv3/AAAAAAAAAAAAAAAAAAAAAOtemICnAM9fuZKTLRs-wnhJbe4u_X-g3DyGkgPlH1ju/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=gWp4io0wG3V85xk2T0Iu%2BIyQb6c%3D)
![](https://blog.kakaocdn.net/dna/oDmTp/btsKwh3wj5n/AAAAAAAAAAAAAAAAAAAAAO1Ev0swtgsIagoLyzvolzRxKjAPuLy08BabFvEcIoja/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KWhzarJpuWt0cxHwQHg%2BdTZ2JEk%3D)

이러한 이유 때문에 **소멸자에는 vritual**을 붙혀주자!

소멸자 호출되는 순서도 봐두자.

~kinght -> ~character 순이다

**+주희할 점**

만약에 소멸자or 생성자에서 또 다른 virtual 함수를 호출하면 어떻게 될까??

Character의 소멸자에서 Attack을 호출하면 어떻게 될까?

![](https://blog.kakaocdn.net/dna/bZAt8R/btsKuUu9rsh/AAAAAAAAAAAAAAAAAAAAAMlDk6NBFX-nNi0JHB6Wlo3oXX_VnMr-bPgAJXdyVOYQ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=965Z7ahnxd%2B1uzLTof7tva9LKhs%3D)

**Knight로 캐스팅하고 delete를 했으니 Knight의 attack이 호출되나?**

![](https://blog.kakaocdn.net/dna/barsKS/btsKwtiJfB6/AAAAAAAAAAAAAAAAAAAAAG4p5FdMovm6gW-BLW5E8SLAlSVyzBzeql-HYFeZtQUb/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Y10FKd3eRC71ASmNxT5%2FHxIqwOc%3D)

생성자나 소멸자에서는 virtual 키워드를 무시하고 함수를 호출한다. 그렇기 때문에 character의 attack이 호출된다. 그렇기 때문에 생성자나 소멸자에서는 virtual 함수를 사용하지 않도록 조심해야된다!

### 

### **번외**

**UpCasting, DownCasting에 대해서 설명하겠다.**

**UpCasting:** 부모 클래스가 자식 클래스로 참조 또는 할당 하는 것

![](https://blog.kakaocdn.net/dna/bXPAKH/btsKrct2MZo/AAAAAAAAAAAAAAAAAAAAAJpSEjp0KqDLSLpHQlkDqIHxO0-pDO7XP9v_nldzPWPD/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=uwDT6WfH%2F2aOnDMYdQOi1f3mNco%3D)

**DownCasting:** 자식 클래스가 부모클래스로 참조 또는 할당 하는 것

![](https://blog.kakaocdn.net/dna/cz9U7z/btsKpTWQlD9/AAAAAAAAAAAAAAAAAAAAAOBhFIUDlK29coVWbjFBc1JzCmV2O87iBA-VJAx15Z2o/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=EaS0go%2F7danaPIUi0uilhzjNXr8%3D)

Knight를 Chracter로 할당하는 것은 불가능하다! (강제로는 할 수 있다.)

굉장히 위험하기 때문이다.

만약 Knight로 선언하고 Character를 할당했을 때 (DownCasting)

Knight에 SwingSword라는 함수가 있다고 해보자 (Character에는 없는...)

![](https://blog.kakaocdn.net/dna/TdjpA/btsKpupowtE/AAAAAAAAAAAAAAAAAAAAAHuwbiWk9T8kv3N_0WXvg36-546a_uKCulpAntENYQ8W/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=C1ZWsNGK6NVBRVtSffMVJWe7oSY%3D)

우리는 Character로 만들어져서 swing sword까지 메모리를 사용하지 않는데,

SwingSword를 호출할 수 있게된다.. 크래쉬가 나거나 엉뚱한 메모리를 참조해서 큰 사단이 날 것이다....