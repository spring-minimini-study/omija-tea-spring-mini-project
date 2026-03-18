## 스프링 라이브러리 추가 할때 주의할점
* org.springframework.boot 가 앞에 붙어있는 애들은 spring boot 버전에 맞춰서 알아서 버전을 가져옴(dependency management)
* 그런데 springdoc 같은 외부 라이브러리들은 스프링이 버전관리를 안해줌. 버전 꼭 붙여야됨!

# Swagger (springdoc)
### 설치방법
`implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:3.0.2'`
- 주의사항 : 딱 한주 전에!!! spring 4.0 서포트가 추가되었음! 3.0.2 사용하면 된다.
### 공부한거
- @Tag 사용해서 Controller 단위로 태깅 가능
    - @Tag(name = "Member", description = "회원관리용 API")
- @Operation 이용해서 엔드포인트별 설명 붙이기 가능
    - @Operation(summary = "회원가입", description = "새로운 유저 등록!")
- DTO에도 어노테이션 다는것이 가능하다! pydantic Field처럼!
    - @Schema(description = "사용자 id", example = "omija")이런식으루

[image](./attachment/img1_swagger.png)

- 기본 url 은 /swagger-ui/index.html/이다.