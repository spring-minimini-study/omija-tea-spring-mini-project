package com.omija.miniproject;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@OpenAPIDefinition(
        info = @Info(
                title = "omija-tea Spring Mini project API",
                description = "스터디에서 진행하는 spring mini project의 API 명세 입니다",
                contact = @Contact(name = "정남준", email = "playjnj123@gmail.com")
        )
)
@SpringBootApplication
public class MiniProjectApplication {

    public static void main(String[] args) {
        SpringApplication.run(MiniProjectApplication.class, args);
    }

}
