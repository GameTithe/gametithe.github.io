---
title: "[실습저장소] IK(Inverse Kinematics)"
date: 2024-11-02
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

### 1. Forward Kinematics (순방향 운동학)

**Forward Kinematics**는 각 관절의 **각도를 알고 있을 때, 끝점의 위치를 계산하는 방식이다**.

로봇이나 캐릭터의 뼈대를 구성하는 모든 관절의 **회전각**과 **링크의 길이**를 통해 손끝이나 발끝 같은 **end-effector(끝점)의 위치**를 찾는다.



![](https://blog.kakaocdn.net/dna/1C2ZD/btsKuj1Co1J/AAAAAAAAAAAAAAAAAAAAAF7aY_Dq3Nj30d1Qf3MFFSm2SrCcnCLDsO1NH0gfMIeF/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=8NihK4KkAg96DMqTEmB8j5xl8Sw%3D)

이렇게 각도를 추가해주면서 구현했다.

### 2. Inverse Kinematics (역방향 운동학)

**Inverse Kinematics**는 **end-effector(끝점)**의**위치가 주어졌을 때, 각 관절의 각도를 계산하는 방식**입니다. 이 방법은 손끝이나 발끝이 특정 위치에 도달하도록 **각 관절의 회전 각도를 역산**하는 데 사용된다.



아래의 링크에서 잘 설명해준다.   
따라서 코딩하면 구할 수 있다.

개인적으로 헷갈렸던 부분은 joint의 좌표를 구하는 것였다.

joint를 만들어줄 때 사용한 변환행렬을 그대로 이용해주면 된다.

![](https://blog.kakaocdn.net/dna/sKlWU/btsKuUtCFQW/AAAAAAAAAAAAAAAAAAAAAD-4P1diNMO7b7R2xw0m4TbLXqtBehjjMMDx2o57ft3E/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=VLMfQj86hDkif9RqAO%2FarmE3CfI%3D)

<https://www.gamedeveloper.com/programming/3-simple-steps-to-implement-inverse-kinematics>