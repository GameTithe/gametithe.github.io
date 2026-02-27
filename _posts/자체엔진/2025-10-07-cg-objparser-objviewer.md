---
title: "3D 세계 만들기 - Obj Parsing, Obj Viewer"
date: 2025-10-07
toc: true
categories:
  - "자체엔진"
sub_category: ""
tags:
  - "DirectX"
---


<!-- 유튜브 링크: 

<iframe width="560" height="315"
  src="https://www.youtube.com/embed/링크"
  title="Jungle Smash"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  allowfullscreen>
</iframe>

-->

<iframe width="560" height="315"
  src="https://www.youtube.com/embed/yXMgXy2ISxs"
  title="Jungle Smash"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  allowfullscreen>
</iframe>

### **ObjPaser**

obj에는 대략 정보가 아래와 같이 작성되어있다.

**mtllib:** mtl 파일 이름

**v:** vertex position

**vt:** texture uv coord

**vn:** vertex normal

**f:** face ( v / vt/ vn )

Parser를 만드는 방법은 간단하다.

v가 보일 때 Position을 저장하는 array에 저장을 한다.

vt가 보일 때 Texture Coordinate을 저장하는 array에 저장을 한다.

vn이 보일 때 normal을 저장하는 array에 저장을 한다.

f를 만나면 index1 / index2/ index3을 만나게 될 텐데

이때 저장해둔 v,vt,vn에서 꺼내오면 된다.

( vn이 없을 때도 있는데, 그때는 index1 // index2로 되어있으니 따로 처리하는 코드를 추가해주자)

아래의 코드는 직접 구현한 코드이다.

수도코드 느낌으로 보자

```
    auto flushSubset = [&]()
        {
            if (Faces.empty()) return;
			
            //Mesh Data로 생성
            MeshesData.push_back(MakeMeshSubset(Positions, Normals, TexCoords, Faces, NameOfSubset));
            SubsetMatKeys.push_back(NameOfSubset);
            Faces.clear();
        };
        
    while (std::getline(File, Line))
    {
        std::istringstream Tokenizer(Line);

        FString Prefix;
        Tokenizer >> Prefix;
        if (Prefix == "usemtl")
        {
        	// usemtl을 만났을 때 submesh처리 
            flushSubset();
            Tokenizer >> NameOfSubset;
        }
        else if (Prefix == "o" || Prefix == "g")
        { 
        	//o, g는 따로 처리 안했음
        }
        else if (Prefix == "mtllib")
        { 
        	//mtl파일 이름 저장
            std::getline(Tokenizer, MTLLibName);
            while (!MTLLibName.empty() && (MTLLibName.front() == ' ' || MTLLibName.front() == '\t')) MTLLibName.erase(MTLLibName.begin());


        }

        if (Prefix == "v") // position
        {
            FPosition Position;
            Tokenizer >> Position.x >> Position.y >> Position.z;
			
            //0,0,0으로 조정 및 scale 조정
            Position = (Position - CenterPos);
            Position = Position * Scale;

            Positions.push_back(Position);
        }
        else if (Prefix == "vn") // normal
        {
            FNormal Normal;
            Tokenizer >> Normal.x >> Normal.y >> Normal.z;
            Normals.push_back(Normal);
        }
        else if (Prefix == "vt") // uv
        {
            FTexCoord TexCoord;
            Tokenizer >> TexCoord.u >> TexCoord.v;
            TexCoords.push_back(TexCoord);
        }
        else if (Prefix == "f") // face
        {
            FString FaceBuffer; 

            FFace FirstVertex;
            FFace ThirdVertex;
            for (int i = 0; i < 3; i++)
            {
                Tokenizer >> FaceBuffer;
                FFace Face = ParseFaceBuffer(FaceBuffer);
                Faces.push_back(Face);

                switch (i)
                {
                case 0:
                    FirstVertex = Face;
                    break;
                case 2:
                    ThirdVertex = Face;
                    break;
                }
            }

        }
    }

    flushSubset();
    File.close();
```

이렇게만 obj 파싱은 해줘도 잘 될 것이다.

(아직 mtl 파일을 읽지 않아서, 랜덤색을 가지고있는 것이다.)

![](https://blog.kakaocdn.net/dna/bFvyTt/btsQISJt0rS/AAAAAAAAAAAAAAAAAAAAACBsKz11ZR2Lq8D3Om_l7jLR5ZO9s3YEc5XeaCJcB_el/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=tDzD3T6x7GKCkJGwObm%2BxE97V3Y%3D)![](https://blog.kakaocdn.net/dna/cHTQLY/btsQIM3Ooli/AAAAAAAAAAAAAAAAAAAAADsGzLTMIZcgc5FqTCO-j8rXply68v6YGd9fuE9-SOGG/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=qRir9WNiP3bC3ID6sL998%2FQn4v0%3D)

하지만 작은(?) 문제가 있다. 만약 f에서 조합하는 vertex가 3개가 아니라 4개 5개인 polygon이면??

아래와 같이 obj파일을 파싱하는데 문제가 생길 것이다.

![](https://blog.kakaocdn.net/dna/bIQpfJ/btsQH87P7pH/AAAAAAAAAAAAAAAAAAAAAJ0ky4jAzCjS_aObSTW3puL37XqUwWJWCXGbGgsLBdaz/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=321L4DmhDJXPbuwstvcYrCg7dGw%3D)

그럴 경우 아래의 그림 처럼 쪼개주면된다.

![](https://blog.kakaocdn.net/dna/cbtYYL/btsQHZCYzU9/AAAAAAAAAAAAAAAAAAAAACHH9ZWJtqGwZ_GnbUZ1w5DrmX3At9JxK8QfqUqfg8uO/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=EEsBZI5hJr88zvqT5mz7Thlgj48%3D)

구현방법은 간단하다.

1. 첫번째 vertex는 고정

2. 삼각형을 만들 때 사용한 3번째 정점을 다음 삼각형의 두번째 정점으로 사용

```
 else if (Prefix == "f") // face
 {
     FString FaceBuffer; 

     FFace FirstVertex;
     FFace ThirdVertex;
     for (int i = 0; i < 3; i++)
     {
         Tokenizer >> FaceBuffer;
         FFace Face = ParseFaceBuffer(FaceBuffer);
         Faces.push_back(Face);

         switch (i)
         {
         case 0:
             FirstVertex = Face;
             break;
         case 2:
             ThirdVertex = Face;
             break;
         }
     }

     // 들어오는 face의 veretx 수가 삼각형이 아닐 때 삼각형화 시켜주는 코드
     while (Tokenizer >> FaceBuffer)
     { 
         Faces.push_back(FirstVertex);
         Faces.push_back(ThirdVertex);

         Tokenizer >> FaceBuffer;
         FFace Face = ParseFaceBuffer(FaceBuffer); 
         Faces.push_back(Face);

         
         ThirdVertex = Face;
     } 
  	}
```

위의 코드를 추가하면 어떤 polygon도 아래와 같이 잘 파싱이될 것이다.

![](https://blog.kakaocdn.net/dna/G9V8J/btsQJbQpiBw/AAAAAAAAAAAAAAAAAAAAAA3h5vtXtcml-uPdFmjY-ToOEaMSC-qEAkhRgkZxr0pM/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=qEhJFF96MqLBUdsR%2BmZtvzkqinw%3D)

### 

### Material

이제 material을 받아와야한다.

obj파일을 읽다보면, usemtl 어쩌구가 등장하는데

이의미는

어쩌구라는 material을 사용할 mesh들입니다 라는 것이다.

mtl파일에 들어가보면

```
newmtl 어쩌구
   Ka 1.000 1.000 1.000
   Kd 1.000 1.000 1.000
   Ks 0.000 0.000 0.000
   d 1.0
   illum 2
   # 앰비언트 텍스처 맵
   map_Ka lemur.tga
```

이렇게 정보있을 텐데, 이름으로 매핑된다고 생각하면된다.

mtl에 적혀있는 정보는 아래와 같다.

```
Ka: ambient color

Kd: diffuse color

Ks: Specular color

Ns: Specular exponent

# 앰비언트 텍스처 맵
   map_Ka lemur.tga
   map_Ks 등등
```

위와 같이 naming convention이 정해져있기에 그에 따라서 파싱을 하고,

pixel shader에서 map이 있으면 texturing을 map이 없으면 상수로 색을 칠해주면 된다.

renderdox으로 보면 texture가 잘 들어오는 것을 확인할 수 있다.

![](https://blog.kakaocdn.net/dna/KsyDP/btsQIDN2Rfn/AAAAAAAAAAAAAAAAAAAAACe_N2TZVXYonKtC4c93Qa_l8elvgTpH7BQdNWPM0kNQ/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=DqhnAxXlExy62xsycyau%2B6xlcN0%3D)![](https://blog.kakaocdn.net/dna/95x0o/btsQIDgdZZu/AAAAAAAAAAAAAAAAAAAAAFqGXYN2yacZsjRHtIFM-k49DGYMjLXfH73--oBHJtwS/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Ysm6g42vo9zlLfWGNDnITNDBjkg%3D)

mtl을 파싱 하고 나면 아래와 같이 이쁜 차를 볼 수 있다.

![](https://blog.kakaocdn.net/dna/k7anA/btsQIHIoYCC/AAAAAAAAAAAAAAAAAAAAAM74jYdImk1xWLkqqnbrJZrvq5fN5ehxkL-8L01Iue9Z/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=grZFnohXYh4b5YSD00YvN15smbk%3D)

지금은 grid, axis, object가 모두 동일한 vertex, pixel shader를 사용하고 있기에 이를 나눠주는 작업도 해주었다.

 

![](https://blog.kakaocdn.net/dna/uchyU/btsQHQ6TEtO/AAAAAAAAAAAAAAAAAAAAAHF35xfRVOyjuE0QGt5NCVt0vebtWq2aNkdmkF3JLopR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=lOhGoLw9OCMUSNyXrIIcdHHcC3k%3D)![](https://blog.kakaocdn.net/dna/IvyWM/btsQIIU0Ddz/AAAAAAAAAAAAAAAAAAAAAMs-3Nr_ORFggdjouiZJg6g3ZQTUgApgi1V9WI8Rnq2C/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=WEfYftMNkjJ1iPjnJ8I76HUFb08%3D)

.

위에서 Mesh와 Material을 파싱했는데, 이것들을 아래의 구조로 저장을 하면, mesh의 material을 변경시킬 수 있다.

![](https://blog.kakaocdn.net/dna/D7x9g/btsQL9SQ2aq/AAAAAAAAAAAAAAAAAAAAAPdLQRSedW7L6g9iAwOCEhgSHY6_Uhad-dnaWJ7KHgrR/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=vhQ25rAlyiLVeOO5B6LLMuqAEJ0%3D)



멋이게 꾸민... 모습..!

![](https://blog.kakaocdn.net/dna/4JYIg/btsQ2jILcIL/AAAAAAAAAAAAAAAAAAAAAKBZiAZ_sio-YEdteinPcRqI0gXUAMeV6riBSzS2fI1y/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=9j9S2srK40qc%2F6Z84SgH%2Bs%2Fjn6I%3D)

### **2. Obj Viewer**

ObjViewerDebug의 exe파일에서는 UI를 빼고 draw하도록 설정했다.

![](https://blog.kakaocdn.net/dna/0SpzV/btsQH8l8j8v/AAAAAAAAAAAAAAAAAAAAAGTpssYnoE4_TIwDzQgDCxdKMAjE1DMurnyFjiMN2ZD8/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Vi%2B%2F7189V5k8L9GiKH%2FXtuTRTNc%3D)
![](https://blog.kakaocdn.net/dna/paxLA/btsQIQ6z3Sn/AAAAAAAAAAAAAAAAAAAAAKAA47sdPiHSJPfaJGk6Mrp2nvJxsARLfkPWqyjlk3dw/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=3Z7go6zQ39N6bz3DOl%2BMZqv%2Fyu4%3D)

obj 파일을 클릭할 때, ObjViewerDebug.exe파일로 실행되도록 설정해주었다.

이때 경로도 얻어올 수 있으니, obj파일을 잘 불러올 수 있을 것이다.

```
    int argc = 0;
    LPWSTR* argv = CommandLineToArgvW(GetCommandLineW(), &argc);
    std::wstring objStringPath;
    if (argv && argc >= 2)
    {
        objStringPath = argv[1];
    }
```



### **Troblue Shooting**

1. 경로 인식

앞에 띄어쓰기 하나 있다고, 경로를 인식을 못하고 투정을 부린다..푸하하

![](https://blog.kakaocdn.net/dna/m2QBB/btsQJwGznbj/AAAAAAAAAAAAAAAAAAAAAPSpwHddYEQ16BI0y3yOOT8Q9juOJTayIiNKv0yFBYGg/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=Ju02dLJ%2B5c9jAe1VdM3ps7YaXt4%3D)

OBJ파일이 저장될 때 mtl에 적혀있는 material에 대한 Path가 상대경로로 저장될 때, 절대 경로로 저장 될 때가 있다.

심지어 상대경로가 obj제작자의 상대경로라서 사실상 의미없는 경로가 될 수 도 있다.

이를 해결하기 위해서 지정된 경로에서 파일명 + 확장자(.png or .dds)만 가져오고, 나의 상대 경로에 붙이는 작업을 수행했다.