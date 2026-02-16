---
title: "[UE5/언리얼5] 블루프린트(BluePrint)튜토리얼 - while, for, for-break #7"
date: 2022-12-30
toc: true
categories:
  - "Tistory"
tags:
  - "언리얼5 #UE5 #언리얼일지 #사칙연산 #0출력 #언리얼변수 #언리얼공부 #언리얼독학 # 언리얼입문 #while #for #for-break"
---

## **while**

## **for**

## **for-break**

**대표적으로 3개가 있다.**

## 

## **while문**

![](https://blog.kakaocdn.net/dna/ETYfa/btrUL74JeiW/AAAAAAAAAAAAAAAAAAAAAK6D1q63zQccToK2LxpcrFzbx1uL5cvY5GqMoRVUBR-H/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=xNOESQ5wg4IVCsjeZNcGq5E4ro8%3D)

Loop Body  : while을 순회할 때 실행시킬 내용

Completed  : 완료되었을 때 실행시킬 내용

Condition    : while문 조건

## **Condition 이 True일 때 순회**

## **False일 때 순회**

## 

## **이렇게 실행한다면 while문이 무한루프를 돌기 때문에 오류가 난다.**

![](https://blog.kakaocdn.net/dna/egnn2O/btrUMJP5kG6/AAAAAAAAAAAAAAAAAAAAAAFTbx4Em4d54LVr3fP-HfaDEUXGUsmYk0DLgCSQFcJk/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=fzXd9Q6kYZThj6ey8OmCOYEZVAk%3D)
![](https://blog.kakaocdn.net/dna/nrXij/btrUIlCEnrp/AAAAAAAAAAAAAAAAAAAAAAGjsXraTubF3CwOYuOd6_AAqBIwhfOeS4Djna17NSiE/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=KsdGPki2rnVEdMUxjSH1qYnIQeA%3D)

**총알이 없을 때까지 발사한다는 알고리즘를 짜보자.(0일 때 스탑)**

답.

![](https://blog.kakaocdn.net/dna/d9Js0b/btrUE5tRvof/AAAAAAAAAAAAAAAAAAAAAHYn8uGUdg4C9BB2tVsiM8WPrEeW2G7YC8am7qiD3B7j/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=2TTrxFL1w4MehDwRqnOuCYmyoM0%3D)

## 

출력이 이렇게 되면 잘 짠겁니다~

![](https://blog.kakaocdn.net/dna/XYOCe/btrUKmA6XQG/AAAAAAAAAAAAAAAAAAAAADkUn3bmMuw0dgls3iE5QacBzeP5j-_fQeXLoWXe52zc/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=BdRrqfYk85J8JjYlUzRh5WxNlCk%3D)

## 

## 우클릭 -> for (flow control 산하에 있는 것)

## **for**

![](https://blog.kakaocdn.net/dna/mGyKB/btrUJkjbKct/AAAAAAAAAAAAAAAAAAAAABkobMOfu6QOLw0ahcC5yjxry7XHyWCcZs81aL8DqwRc/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=1wPI2SZ0FEkcIfB%2Bwiw4r7Ne2qE%3D)

## **FirstIndex가 LastIndex에 도착하면 종료된다.**

## **FirstIndex가 루프 1번 돌 때마다 1씩 증가한다.**

**Loop Body와 Completed는 똑같다.**

**Index : index, firstIndex, LastIndex를 비교하면서 For문을 반복한다.**

## **for-break**

**for-break는 특정 조건을** **break 걸어두고**

**그 조건을 만족하면 break하는 반복문이다.**

**뭔가 while문과 for문을 합친 느낌? 이다**

**예제를 풀어보면서 느낌을 알아가자**

**랜덤한 숫자 를 break조건으로 걸고 break될 때 출력해보자**

**(힌트 : 랜덤한 숫자를 골라주는 함수는 오른쪽 클릭->random 검색)**

(주의 : for-break의 lastIndex가 n이라고 할 떄, for문은 index가 n-1까지 순회한다.

            random함수의 Max가 n이면 0 ~ n 에서 랜덤으로 숫자를 반환한다.)

답

![](https://blog.kakaocdn.net/dna/bjTxb7/btrUL8ihlWJ/AAAAAAAAAAAAAAAAAAAAAJ2qLBgm5MWBJ3c647KsCCHOXoZmkyk68hJu_jEV4cHe/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=a%2BqqAj37yBGdQZCQ4jHGEbf5wHs%3D)

결과

![](https://blog.kakaocdn.net/dna/cZQx2a/btrUKYNJLZI/AAAAAAAAAAAAAAAAAAAAAHot_s7TCR8QL4QB-CI-belqhoBKfVc1SWEADMOrSHd7/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=UE14cATYPIJvlcaf636n%2FHZlikE%3D)
![](https://blog.kakaocdn.net/dna/p6Zn9/btrUKmVo74a/AAAAAAAAAAAAAAAAAAAAABYBxJ05LJ3uHspf7GqLjolaZ0GLSECIXMk7rNZpO7c3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=P%2BGmSlhwnc%2BmqbrYrLyH%2FtjPaB4%3D)

**지금까지 배운 것을 바탕으로 마지막 예제를 풀어보자**

**1. 2단~4단까지 곱셈을 출력하자.**

![](https://blog.kakaocdn.net/dna/YoabX/btrUGHM0n6p/AAAAAAAAAAAAAAAAAAAAAE9K1wivGXuDpOr50qmdbLccwjacfq4eJjBFe9iel4f4/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Ky4FNr47n71cgD5exJ3drrI1MSc%3D)

**이렇게 출력하면 된다.**

## **답. for문만 쓰면 더 간단하게 할 수 있지만, 연습을 위해서 while문을 포함했다.**

![](https://blog.kakaocdn.net/dna/PsstT/btrUGIkXdPy/AAAAAAAAAAAAAAAAAAAAADUvcPsb4-4l3U1PIJYnkkey0-Iskku-U9pg_6K6BQCH/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=yJWHezSHONWBFMjixH8uSEfhXDw%3D)
![](https://blog.kakaocdn.net/dna/4cek5/btrUNUXVMOx/AAAAAAAAAAAAAAAAAAAAADFZ8FS3KEz5qlmaOEvbqEvWGtykiTTT0JJj1iJW18fP/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=eUN6kUsPP3gj4Jazs0ORLpQENh8%3D)