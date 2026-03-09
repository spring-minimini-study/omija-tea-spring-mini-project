package com.omija.miniproject.domain.member;

import lombok.*;

import java.util.List;

public class MemberDto {
    @Getter
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CreateMemberRequest {
        private String userId;
        private String name;

        public Member toEntity() {
            return Member.builder().userId(this.userId).name(this.name).build();
        }
    }

    @Getter
    @AllArgsConstructor
    public static class MemberInfo {
        private String userId;
        private String name;

        public MemberInfo(Member member) {
            this.userId = member.getUserId();
            this.name = member.getName();
        }
    }

    @Getter
    @AllArgsConstructor
    public static class AdminMemberInfo {
        private Long id;
        private String userId;
        private String name;

        public AdminMemberInfo(Member member) {
            this.id = member.getId();
            this.userId = member.getUserId();
            this.name = member.getName();
        }
    }

    @Getter
    @AllArgsConstructor
    public static class AdminListResponse {
        private List<AdminMemberInfo> memberList;
    }
}
