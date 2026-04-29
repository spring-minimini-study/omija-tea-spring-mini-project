package com.omija.miniproject.domain.test;

import com.omija.miniproject.domain.llm.OpenAiClient;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Tag(name = "Test", description = "테스트 API")
@RestController
@RequiredArgsConstructor
@RequestMapping("/test")
public class TestController {
    private final OpenAiClient openAiClient;

    @Operation(
            summary = "질문!",
            description = "asdf"
    )
    @PostMapping
    public ResponseEntity<String> chat(@RequestBody String message) {
        String res = openAiClient.generateChat(message);
        return ResponseEntity.ok(res);
    }
}
