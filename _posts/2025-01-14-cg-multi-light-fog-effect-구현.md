---
title: "[CG] Multi Light + Fog Effect 구현"
date: 2025-01-14
toc: true
categories:
  - "Tistory"
tags:
  - "tistory"
---

<https://tithingbygame.tistory.com/138>

[[실습저장소] Multi Light + Fog Effect

tithingbygame.tistory.com](https://tithingbygame.tistory.com/138)

1. Multi Light

Multi Light는 생각보다 간단합니다.

그냥 데이터를 2개 보내주고, Shader에서 for문으로 2번 그려주면 됩니다.

데이터 보내는 코드

```
		// 첫 번째 조명 정보 설정
		lights[0].lightPos = lightPosition;
		lights[0].padding = 0.0f; // 패딩은 사용하지 않지만 정렬을 위해 필요
		lights[0].lightColor = glm::vec4(1.0f, 0.0f, 0.0f, 1.0f); // 빨간 조명

		// 두 번째 조명 정보 설정
		lights[1].lightPos = lightPosition + vec3(-1.0f, 0.0f, -1.0f);
		lights[1].padding = 0.0f; // 패딩은 사용하지 않지만 정렬을 위해 필요
		
		lights[1].lightColor = glm::vec4(0.0f, 0.0f, 1.0f, 1.0f); // 파란 조명
		GLint lightPosLoc = glGetUniformLocation(shaderProgram.ID, "lights[0].lightPos");
		GLint lightColorLoc = glGetUniformLocation(shaderProgram.ID, "lights[0].lightColor");

		// 첫 번째 조명 데이터
		glUniform3fv(lightPosLoc, 1, glm::value_ptr(lights[0].lightPos));
		glUniform4fv(lightColorLoc, 1, glm::value_ptr(lights[0].lightColor));

		// 두 번째 조명 데이터
		lightPosLoc = glGetUniformLocation(shaderProgram.ID, "lights[1].lightPos");
		lightColorLoc = glGetUniformLocation(shaderProgram.ID, "lights[1].lightColor");
		
		glUniform3fv(lightPosLoc, 1, glm::value_ptr(lights[1].lightPos));
		glUniform4fv(lightColorLoc, 1, glm::value_ptr(lights[1].lightColor));
	
		FogInfo fogInfo;
		fogInfo.maxDist = 3.0f;
		fogInfo.minDist = 1.0f;
		fogInfo.color = vec3(1,1,1);
		fogInfo.padding = vec3(0, 0, 0);

		GLuint fogMaxDist = glGetUniformLocation(shaderProgram.ID,"Fog.maxDist");
		GLuint fogMinDist = glGetUniformLocation(shaderProgram.ID,"Fog.minDist");
		GLuint fogPaddingDist = glGetUniformLocation(shaderProgram.ID,"Fog.padding");
		GLuint fogColorDist = glGetUniformLocation(shaderProgram.ID,"Fog.color");
		glUniform1f(fogMaxDist, fogInfo.maxDist);
		glUniform1f(fogMinDist, fogInfo.minDist);
		glUniform3fv(fogPaddingDist, 1, glm::value_ptr(fogInfo.padding));
		glUniform3fv(fogColorDist, 1, glm::value_ptr(fogInfo.color));
```

그리는 코드

fragment Shader

```
vec4 spotLight() 
{
	vec4 Color = vec4(0.0f, 0.0f, 0.0f, 0.0f);
	
	for(int i = 0; i < 2; i++)
	{	
	//ambient
	float ambient = 0.2f;
	
	//diffuse 
	float outerCone = 0.90f;
	float innerCone = 0.95f;

	vec3 n_normal = normalize(normal);

	vec3 lightDir = normalize(lights[i].lightPos - curPos);
	float diffuse = max( dot( lightDir, n_normal) , 0.0f);

	//specular
	float specularLight = 0.5f;
	vec3 viewDir = normalize(camPos - curPos);
	vec3 reflectDir = reflect(-lightDir, n_normal);

	float specularPow = pow(max(dot(viewDir, reflectDir), 0.0f), 16);
	float specular = specularLight * specularPow;

	float angle = dot(vec3(0.0f, -1.0f, 0.0f), -lightDir);
	float inten = clamp((angle - outerCone) / (innerCone - outerCone), 0.0f, 1.0f);

	//return texture(tex0, texCord) * lights[i].lightColor * (diffuse + ambient + specular);
	//return texture(tex0, texCord) * (  ambient + diffuse *inten + specular * inten) * lights[i].lightColor;
	Color +=  (ambient + diffuse *inten + specular * inten) * lights[i].lightColor;
 }
 return Color;
}
```

2. Fog Effect

기본적인 Fog 효과는 아래의 공식을 사용하면 됩니다.

dmax는 안개효과의 최대치가 적용되는 (물체가 안보이는) 거리,

dmin은  안개효과가 적용되지 않는(물체가 온전히 보이는) 거리,

z는 물체와 카메라의 거리입니다.

![](https://blog.kakaocdn.net/dna/SrnIm/btsLLTadocV/AAAAAAAAAAAAAAAAAAAAANvP-v45peiRmsk0HqB09FVHkRFjoz19cbGb6y53mZc3/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1772290799&allow_ip=&allow_referer=&signature=rXyms9M4toJ8C3TB7pEZvJodwF0%3D)

```
	float dist = length(camPos - curPos);
	float fogFactor  = (Fog.maxDist - dist) / (Fog.maxDist - Fog.minDist);
	fogFactor = clamp(fogFactor, 0.0f, 1.0f);
	
	vec4 shadeColor = spotLight();
	vec3 color = mix( Fog.color, shadeColor.xyz, fogFactor );
	FragColor = vec4(color, fogFactor);
```

지수함수를 사용하면 더 사실적으로 나타낼 수 있다고 합니다. 거의 차이는 없지만 밀도가 느껴지기는 합니다.

```
	float density = 0.5f;
	float dist = length(camPos - curPos);
	float fogFactor = exp(-pow(density * dist,2));
	
	vec4 shadeColor = spotLight();
	vec3 finalColor = mix(Fog.color, shadeColor.xyz, fogFactor);
	FragColor = vec4(finalColor, 1.0f);
```