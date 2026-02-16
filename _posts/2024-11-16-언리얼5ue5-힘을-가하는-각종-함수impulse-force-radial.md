---
title: "[언리얼5/UE5] 힘을 가하는 각종 함수(impulse, force, radial)"
date: 2024-11-16
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

**AddImpulse vs AddForce**

* **AddImpulse**는 프레임 속도(fps)와 관계없이 즉각적으로 힘 벡터를 적용한다. 이 함수는 총알 충격이나 폭발 같은 순간적인 효과를 표현할 때 유용하다.
* **AddForce**는 프레임 속도에 맞춰 힘을 조정하여 프레임마다 호출해야 한다. 지속적인 가속 효과를 표현할 때 사용되며, AddImpulse와 같은 효과를 내기 위해서는 프레임 수만큼 힘 벡터를 곱하거나 여러 프레임에 걸쳐 호출해야 한다.

**Vel Change vs Accel Change 파라미터**

* 이 두 파라미터는 객체의 질량을 무시하고 속도를 조정한다. Epic Games에서는 AddForce 함수의 용도가 매 프레임 호출하여 가속도를 변경하는 것이기 때문에 이를 Accel Change라고 명명했으나, 실제로는 속도 조정과 동일한 기능을 수행한다. "Ignore Mass" 같은 이름을 사용했다면 더 명확했을 것이다.

**Radial**

* Radial 함수는 특정 위치에서 힘이 발생하는 원점을 지정할 수 있다. 예를 들어, 폭발 지점에서 힘이 방사형으로 퍼져 나가는 효과를 줄 때 사용한다.

**Angular**

* Angular는 객체의 x, y, z 방향에 힘을 더하는 대신 pitch, yaw, roll 회전축에 힘을 추가하여 회전력을 적용한다. 다른 함수들과는 성격이 다르지만, 객체의 회전을 표현할 때 유용하다.

**LaunchCharacter**

* LaunchCharacter 함수는 물리 시뮬레이션(질량, 마찰)을 적용하지 않으며, 캐릭터 전용으로 사용할 수 있다. 이 함수는 캐릭터의 속도를 설정하거나 더하여 기본적인 힘 효과를 준다. xy와 z override 파라미터를 설정하면 기존 속도에 더하는 대신 해당 속도로 설정한다.

AddImpuse가 안될때...   
두번째 인자를 true로 해주면 된다. (속도변화에 관한 인자)

지금 FPS게임에 넉백을 넣으려고 하는데, LaunchCharacter가 적당한 것 같다.

AddImpuse를 하면 점프해서 발은 맞추면 몬스터가 위로 튄다...  
LaunchCharacter는 Z좌표를 고정시킬 수 있다!