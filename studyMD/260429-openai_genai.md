# 의존성
## 원칙
1. 스프링 4.x.x를 쓰지말것.
2. 원칙 1을 반드시 고수할것.
은행권이나 안정적인 서버를 추구하는 회사들이 자바 1.8을 아직도 쓰는데에는 이유가 있다.
non-stable 버전을 절대 함부로 사용하지 말것

스냅샷 버전을 써야하기 때문에 기본 maven repository 뿐만이 아닌 스냅샷용 repository도 추가시켜줘야함
```gradle
repositories {
    mavenCentral()
    maven { url = 'https://repo.spring.io/milestone' }
    maven { url = 'https://repo.spring.io/snapshot' }
    maven {
        name = 'Central Portal Snapshots'
        url = 'https://central.sonatype.com/repository/maven-snapshots/'
    }
}
```

## BOM(Bill of Materials)
여러 라이브러리를 사용할때, 서로 버전이 꼬이지 않도록 미리 정의해둔 정보를 BOM이라고 한다!
직접 만든 라이브러리 비법 레시피같은거임 (테스트 완료하고 충돌 해결된 라이브러리 버전들 리스팅)
이걸 이용하면 build.gradle 에서 org.~~:library 하고 버전을 안적어도 됨

내부적으로는 그냥 특별한 형태의 POM.xml이라고 한다. dependency들만 적혀있음.

## dependency-management 플러그인
build.gradle 에 보면 자동으로 추가된 dependency-management라는 플러그인이 있을것!

아무래도 dependency-management 는 버전 후처리 레이어가 추가되어 속도도 느리고, 버전 강제, 충돌 추적등도 어려워서 기업들에서는 좀 뺀다고 한다.
안쓰는 경우에는 아래처럼 해주면 된다.
```gradle
dependencies {
    // https://docs.spring.io/spring-boot/gradle-plugin/managing-dependencies.html#managing-dependencies.gradle-bom-support
    implementation platform(org.springframework.boot.gradle.plugin.SpringBootPlugin.BOM_COORDINATES)
    annotationProcessor platform(org.springframework.boot.gradle.plugin.SpringBootPlugin.BOM_COORDINATES)
    implementation platform('org.springframework.ai:spring-ai-bom:2.0.0-SNAPSHOT')
}
```

# Spring-ai
일단 나는 스프링 4.x.x 라서 spring-ai 2.x.x를 사용!
```yaml
ai:
  google:
    genai:
      api-key: ${GEMINI_API_KEY}
      chat:
        options:
          model: gemini-3.1-flash-lite-preview
  openai:
    api-key: ${OPENAI_API_KEY}
    chat:
      options:
        model: gpt-5.4-mini
```
요래 해주면 Spring-ai가 알아서 API Key 가져다가 씀!

```java
@Configuration
public class LlmConfig {
    @Bean
    public ChatClient geminiChatClient(GoogleGenAiChatModel googleGenAiChatModel) {
        return ChatClient.create(googleGenAiChatModel);
    }
    @Bean
    public ChatClient openAiChatClient(OpenAiChatModel openAiChatModel) {
        return ChatClient.create(openAiChatModel);
    }
}
```
chatClient들을 Bean으로 등록! 공식 docs 방법 그대로 가져왔음




# 그 외 공부한것
## @Component, 그리고 @Bean
@Service, @Repository도 내부적으로 @Component를 달고 있음.
둘다 스프링에 빈을 등록하는건 맞긴함.

### @Component
* 스프링이 @ComponentScan을 때릴때 @Component를 발견하고 지가 직접 인스턴스를 만들어서 빈으로 등록함
* 얘는 **내가 직접 만든 클래스** 를 빈으로 등록함!
  * 그렇다보니 외부 라이브러리 클래스에는 @Component를 붙일수가 없다
### @Bean
* 애는 외부 클래스를 빈으로 등록할때 쓴다.
* 빈을 만드는 코드를 작성하면 **리턴값**을 스프링이 빈으로 등록해줌..!
* 내가 코드를 쓰는거니까, 생성과정에서 필요한걸 끼워넣을 수 있음(생성과정 제어 가능!)
* 참고로 @Configuration 은 Bean을 담는 그릇이라고 생각하면 된다.
  * @Configuration 자체도 @Component를 달고 있어서 스프링 빈으로 등록되지만, 애는 다른 빈을 만들어주는 공장 역할을 수행!
  * 또한 얘는 내부적으로 클래스를 프록시로 감싼다. 그래서 2Bean을 여러번 호출해도 항상 싱글톤 보장해줌

## 비동기
스프링에서 비동기는 세가지 정도 방식이 있다고 한다.
1. @Async 어노테이터. AppConfig에 @EnableAsync 하면 자동으로 됨. @Async 붙은 함수 딱 js의 promise처럼 사용 가능(별도 스레드)!
2. webflux. spring-web 대신 spring-webflux. 이건 fastapi 같은 이벤트 루프 형식의 비동기 지원. 대신 아키텍처 싹다 바꿔야됨
3. vitual thread. 이건 좀더 공부가 필요하다. 코루틴방식인데, 지가 알아서 블로킹을 인식한다던데..?

## RestTemplate, RestClient
안드로이드의 retrofit, 파이썬의 requests와 비슷하게 외부 요청하는 라이브러리!

## @Qualifier
인터페이스는 하나인데 구현체가 여러개라면, 스프링은 어떤 빈을 주입해야할지 헷갈려한다.
이때 주입하고 싶은 구현체를 @Qualifier로 알려주면 알아서 해당 빈을 주입해준다..!
