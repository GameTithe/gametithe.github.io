---
title: "[언리얼/UE5] Online Subsystem 설정하기 (Steam)"
date: 2024-09-23
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

우리는 이전에 local Ip를 가지고 연동하는 것을 해봤다.

그럼 같이 게임하기 위해서는 항상 같은 wifi를 써야되는 것인가?

그럼 멀티게임은 친구가 없으면 못하는 것인가...? 당연히 아니다 이를 극복하기 위해 도움을 주는 것이

OnlineSubsystem이다.

우리는 스팀(steam)을 이용해보자

## 

## **Steam Setting**

Edit -> Plugin -> Online Subsystem Steam 을 설치한다.

![](https://blog.kakaocdn.net/dna/4qhXn/btsJDrNZu5w/AAAAAAAAAAAAAAAAAAAAAF_suLPa55wNQtxtQJrf09uTPBnGj1na_sUx_B_-q906/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GZ4C1yKvp%2FCScLCdt9zGx%2BbPuXs%3D)

프로젝트에서 .cs 파일을 찾고 OnlineSubsystemSteam, OnlineSubsystem 을 추가한다 ( onelinesubsystem과 interact하기 위함)

![](https://blog.kakaocdn.net/dna/bBbkQA/btsJEH3hOQO/AAAAAAAAAAAAAAAAAAAAACqp_CepuPUiwBaRIQCYptCEM2V16YwoPjo7qUd0JoVZ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=we6y0ypEAmxdker142xHi95SguI%3D)

언리얼 문서이다.    
이 주소로 가면 DefaultEngine.ini 에 추가해야 될 것들을 알려준다  
모두 추가하고 visualStudio와 UE5을 재시작해주자

(Config에 들어가면 DefaultEngine.ini를 찾을 수 있다.)

<https://dev.epicgames.com/documentation/de-de/unreal-engine/online-subsystem-steam-interface-in-unreal-engine>

Steps를 복사 붙여넣기 하고 그냥 끄면 뒤에서 잘 안된다

조금만 더 내리면 Using session이라고 적혀 있는 부분도 있다. 그것도 같이 불여넣자!!!

우리가 셋팅한 것들로 파일들이 만들어져야하니 Binaries, intermediate, saved 파일을 삭제하자. (다시 생기는 애들이니 걱정말자, 다른 파일은 삭제하지말자... )

![](https://blog.kakaocdn.net/dna/bAmsnM/btsJFGJhZ5E/AAAAAAAAAAAAAAAAAAAAALdUGtGN2jvcwT4W4WxPPawXshmjMoCY9dihEtvinuh0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=hsVGYIHTX8w%2BtcAxysa6WMmT9oU%3D)

그리고 generate visual studio project files를 하고, 재시작을 하면 끝!

![](https://blog.kakaocdn.net/dna/8ORiy/btsJEiQbPGY/AAAAAAAAAAAAAAAAAAAAAAIO3_QEloEYGHoKvPs658myalCUeMlO5Nnn2E5UKVht/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=cPljprVe%2FNUZ6mA7A4ef3e3Tm%2F4%3D)

이제 스팀하고 잘 연동이 되었는지 테스트를 해봐야 된다.

함수에 대해서 일일이 설명하기에는 나가야될 진도가 빠듯하니 ( 개인적인 프로젝트 진도...)

함수는 각각 찾아보는 것을 권장한다. (매우 중요한것은 설명은 해보겠다.. ) 

원래 IOnlineSessionPtr로 선언을 했지만 그렇게 선언하면

![](https://blog.kakaocdn.net/dna/dOZWt3/btsJFryOJSR/AAAAAAAAAAAAAAAAAAAAAHI3_rg-bQKqBjLgpCHIKQ_BTeGvSUHAPnN1Ne_z0ryx/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Dff%2B%2FpsI2oI0oDzdzvPV9HJApqA%3D)

 이런 오류가 생긴다.

전방 선언을 안해서 생기는 일

IOnlineSessionPtr 은 TSharedPtr<class IOnlineSession, ESPMode::ThreadSafe>로 이루어져있다.

그러니 IOnlineSession 앞에 class를 붙여서 전방선언을 해서 오류를 우회하자

![](https://blog.kakaocdn.net/dna/LI5iA/btsJDQGBdhQ/AAAAAAAAAAAAAAAAAAAAACb4zMq7K1irjVj6ih-i_Gq3JtQqyniQQP2kcLHHEmkn/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=pxbuB%2FoApXgiSD35mSEpNFCw%2BOo%3D)
![](https://blog.kakaocdn.net/dna/cj6ydy/btsJDzkRtcq/AAAAAAAAAAAAAAAAAAAAADUKtCZbYwtaCA7Sx7CLcIa4bBj66_TP1rFRj57w1cR7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=NeRttAX740g4Y1ScUkjZzcdiKAo%3D)

결과적으로 NULL이 뜬다..

근데 getsubsystemName을 통해서 얻어온 NULL이다

null이 Tostring을 통해서 null로 출력될 수가 없기 떄문이다.

![](https://blog.kakaocdn.net/dna/bjJs2z/btsJFKx95W5/AAAAAAAAAAAAAAAAAAAAAEBPkGnfnRWOG8y5u7dokZiiiHcudJkgh_IpeKnAy3hV/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=ktBQKYfdWR66G9JtDB48RtF5q%2BI%3D)

packaging을 하고 exe파일을 실행시키면

![](https://blog.kakaocdn.net/dna/bi5tPw/btsJEktFegK/AAAAAAAAAAAAAAAAAAAAAHAj6I5bTLP2iTERUgqR3jpyEhnikilfzswHzKFm3cwJ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=GBlQB8ReIKtRaJz7KN5dvcm5UgE%3D)

steam과 잘 연동되었음을 알 수 있다!