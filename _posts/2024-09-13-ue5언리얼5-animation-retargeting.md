---
title: "[UE5/언리얼5] Animation Retargeting"
date: 2024-09-13
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

(미래에 저의 기억을 되살리기 위한 글로 많은 생략이 있을 수 있습니다)

애니메이션 retargeting을 위해서는 가지고 있는 모델의 rig 정보와 유사하게 만들어줘야지 retargeting할 수 있습니다.

![](https://blog.kakaocdn.net/dna/CzCNV/btsJxEFWFsj/AAAAAAAAAAAAAAAAAAAAAPNegMo54PaEOhwPw8-lvLnCO7g-a1GXb-pQ6TjtHbUa/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=%2FC43KlaTY8nOYZx6oS%2FuCaae5sI%3D)

pelvis 를 Retarget Root로 설정을 해줍니다.

애니매이션을 가져오고 싶은 에셋의

관절들을 비슷하게 카피해줍니다.

![](https://blog.kakaocdn.net/dna/L6RDm/btsJxj9Sqd5/AAAAAAAAAAAAAAAAAAAAAAC4t9A4oNHIlMCU388UDZBPf38orelybWrA4M5vSLVR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=5h%2FN05J5EfhFAvjs6TbMY6PO1Lo%3D)

카피가 되었다면 IK\_Retarget을 만들어주고

![](https://blog.kakaocdn.net/dna/YXH4U/btsJxnR1kyj/AAAAAAAAAAAAAAAAAAAAAHzVdyEaaHM7RWemMHrmMsZ5b_i20ufVHVPU9Et3BVqN/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=TuPhjGC4xT6AqtID8HuWUHs2kT8%3D)

안에서 Source 와 Target을 정해준다면   
이렇게 Animation Retargeting이 가능합니다.

![](https://blog.kakaocdn.net/dna/eg3fse/btsJy0Bcztq/AAAAAAAAAAAAAAAAAAAAALT8YD3icxomuqh1Wb0EciRe94iSBiwafz3OCnRaWNJR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=PLAJ03KU8%2BGkN%2BW9zgNfuGL4FEQ%3D)