---
title: "[RDM Plugin] QA4: 자연스러운 파편 생성 및 최적화"
date: 2026-02-09
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

총알이 많이 충돌되었을 때,  프레임 드랍이 심하다는 이슈가 들어왔다.

지금은 연결이 완전히 끊겨야지 파편을 생성해서 탈락시킨다. ( 한 줄 정도의 사이즈로도 연결되어있어서는 안된다. )

하지만 실제 게임에서 그렇게 디테일하게 판정하면, mesh를 무너뜨리기 쉽지않다.

 그러므로 임의로 서버가 판단해서 파괴하는 로직을 넣으면 좋을 것 같다.

아래와 같이 vertex가 많이 생성되는 구멍을 파내는 아이디어로 시작했다.

![](https://blog.kakaocdn.net/dna/xzh6V/dJMb99SIPgj/AAAAAAAAAAAAAAAAAAAAAEiHEp0aFcnAm9CBcRKV7SfvkLggCWIoY2gd2KSJLKaS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=dCT1JQMe5eZUGWNG%2BvXLQFm%2BWQQ%3D)![](https://blog.kakaocdn.net/dna/vJmYL/dJMcacWch83/AAAAAAAAAAAAAAAAAAAAAHHDarvJ1pr4zV_ich6EWv7dHcwI3maWA3hG6OwJWuo0/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=SDWLPZrkjp7egkxwXTRdn9iDDI0%3D)

충돌이 많이되는경우 vertex가 기하급수적으로 증가한다.

![](https://blog.kakaocdn.net/dna/ZSSag/dJMcaaxklKy/AAAAAAAAAAAAAAAAAAAAAF0aWokeJw9NzBK44-hnv22axGavorrzbzCLLmO7BWsN/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=WxrwF%2B4w1mlc0CVo8ZZ91b0aLfQ%3D)

지금 Supcercell 안에 cell의 destroyed ratio를 계산해서

임계치를 넘으면 supercell이 무너지도록 만들었다. (supercell 단위로 BFS가 최적화 되어있기 때문에)

결과적으로 vertex가 절반이상이 줄게되었다.

삼각형은 1/3 정도로 줄었다.

![](https://blog.kakaocdn.net/dna/5zBnp/dJMcah4hVkz/AAAAAAAAAAAAAAAAAAAAADsIPsNm1jDqsxZR_FvOvLMOZNDYtyEP5-lJnsXoFQPp/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nKJFavhw15OsLwNMXStxlwT3QGE%3D)
![](https://blog.kakaocdn.net/dna/dMdv4V/dJMcagqK3hO/AAAAAAAAAAAAAAAAAAAAAP7wJ2SQ93v_ZuFmpaybsdhnT-fJ9oGawP-sISq12_OK/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=n2q3LXU85yTIyQziA6n%2Bqze9qyU%3D)



### 네트워크 동기화

모양은 determinstic한 알고리즘이여서 거의 비슷하게 생성된다.

![](https://blog.kakaocdn.net/dna/cvkOqR/dJMb99SJ4NH/AAAAAAAAAAAAAAAAAAAAAA9TPncQ5PoqVElIVRyl4-p1qMmtHax7PvPmdrL8IhlF/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=2T0SS31%2Fsn07rNvmV6FhIontZBg%3D)

Transform 동기화는 안되고 있음

![](https://blog.kakaocdn.net/dna/bbJc0E/dJMcaia40R2/AAAAAAAAAAAAAAAAAAAAAFhfZjI7HDCH_I6MHdJE4zpU1w5jHmnd86FyTzTEN3qB/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=bTfiUM9mzzumKGePBFhVM1XTpu8%3D)

Transform 동기화는

Server에서 Debris Actor를 만들고 replicate를 하고,

각각의 클라이언트에서 만든 Mesh를 입히면, 자연스럽게 동기화가 된다. (Mesh가 동기화 되는건 앞에서 확인했다.)