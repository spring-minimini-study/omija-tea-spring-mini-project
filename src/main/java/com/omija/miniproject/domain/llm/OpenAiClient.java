package com.omija.miniproject.domain.llm;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

@Component
public class OpenAiClient {
    private final ChatClient chatClient;

    public OpenAiClient(@Qualifier("openAiChatClient") ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    public String generateChat(String prompt) {
        return chatClient.prompt()
                .system("너는 고양이야. 모든 질문에 고양이어로 대답해. 고양이는 인간 말 못해.")
                .user(prompt)
                .call()
                .content();
    }
}
