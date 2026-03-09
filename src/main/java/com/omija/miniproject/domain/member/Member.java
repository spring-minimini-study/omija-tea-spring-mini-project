package com.omija.miniproject.domain.member;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Member {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique=true, nullable=false)
    private String userId;

    @Column(nullable=false)
    private String name;

    @Builder
    public Member(String userId, String name){
        this.userId = userId;
        this.name = name;
    }
}
