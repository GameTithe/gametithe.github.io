---
title: "[RDM Plugin] QA3: Mesh Island error"
date: 2026-02-09
toc: true
categories:
  - "UE5_Plugins"
tags:
  - "UE5_Plugin"
---

disconnected까지 잘 처리하고 있는데도,

공중에 파편이 남아있는 버그가 있다는 제보..!

debug 모드를 켜보니

boolean subtract ( 구멍 뚫기)는 총알의 방향으로 뚫는데, grid cell은 충돌된 물체의 normal의 반대방향으로 구멍을 뚫고 있었다.

![](https://blog.kakaocdn.net/dna/7koXz/dJMcagjY7wl/AAAAAAAAAAAAAAAAAAAAAGtxARmEMLmcGrt_HmPiuPq8sKp6UvwjGRpxMukFUqOD/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=yqtP%2BI%2FJmFVWfxTvtQ1nFyCxeD4%3D)![](https://blog.kakaocdn.net/dna/bGGKmv/dJMcabQvpgt/AAAAAAAAAAAAAAAAAAAAAPjkWJtu4zc9rC4nrLdyPEZa0rhM-qBYZLAOvyT0ecY6/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=nJFST3rSPb2kCcCJ5Xc4Y16YPH0%3D)

수정해주니 방향이 잘 맞는다.

![](https://blog.kakaocdn.net/dna/5LT4j/dJMcaioyEB0/AAAAAAAAAAAAAAAAAAAAAKZc8ZeLwFAGK47aI9SghFlGMYgP8vS02SFwDBEm1bwE/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=CbpltBwjDglIM5cxBJRjmb9XULI%3D)

하지만.. 여전히 땅에 안떨어지고 하늘에 떠있음..

![](https://blog.kakaocdn.net/dna/bumpci/dJMcahwq5Jo/AAAAAAAAAAAAAAAAAAAAAN-bF7I4RoWNE8XdE1Xbp2WKyA_xqe1s-w8KdYG-w5YG/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=NzJqLL%2B6%2BtP%2FHDa6B7thLY9RlvU%3D)

disconnected를 할 때 BFS를 돌고, BFS는 supercell로 최적화를 했다. (이 부분은 나중에 cell구조를 정리할 때 다뤄보겠음)

Supercell부분이 의심스러워석 supercell로 다시 확인을 해보았다.

![](https://blog.kakaocdn.net/dna/t4Qag/dJMcagRPsz4/AAAAAAAAAAAAAAAAAAAAAHi2d0xgoiZUAJjNJKAxeLIhS1ZjwQHaEYg6uQvtxYxi/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=5PuuspWq2KbkCYiqDFakvxG46mI%3D)

위의 그림과 같이 만들어졌는데, 아래의 그림처럼 손상되지 않은 mesh의 supercell이 바깥쪽으로 빙 돌면서 anchor까지 연결되어서 disconnected 판정이 안되고 있었다. (disconnected 판정을 앵커~파편까지 bfs를 통해서 연결되어있는 지 확인한다.)

![](https://blog.kakaocdn.net/dna/b54OJm/dJMcafZFx1K/AAAAAAAAAAAAAAAAAAAAAC0luXrPGoxCdB9M9GlQjlrHqiX555YztfI5Z1Zmyzuw/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=DhODWm7ZgIjBWKXUIt5zaaBVz8g%3D)![](https://blog.kakaocdn.net/dna/lUHhK/dJMcafL9YvJ/AAAAAAAAAAAAAAAAAAAAAEG_SxHckQtlU-J24oS1M_D9M8_9WDwLlgRy40CSSBVT/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=huKZDAu3fKqjcoEM4GLZ0WS8wHw%3D)

그래서 Supcell을 전부채우지 못하면 supcell을 생성하지 않도록 변경했다.

아래 이미지를 보면 외각으로 생성되는 supercell없어진 것을 볼 수 있다.

![](https://blog.kakaocdn.net/dna/SP7Sz/dJMcaiPALXN/AAAAAAAAAAAAAAAAAAAAACueFilZeqj4rW0-uVAz64nFuBA4Q5XUZcLZLAlFCpRT/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=rleqx%2F7tPMHsHqYVq43N6hdKfMA%3D)