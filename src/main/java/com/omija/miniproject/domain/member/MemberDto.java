package com.omija.miniproject.domain.member;

import lombok.*;

import java.util.List;

public class MemberDto {
    @Getter
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CreateMemberRequest {
        private String memberId;
        private String name;

        public Member toEntity() {
            return Member.builder().memberId(this.memberId).name(this.name).build();
        }
    }

    @Getter
    @AllArgsConstructor
    public static class MemberInfo {
        private String memberId;
        private String name;

        public MemberInfo(Member member) {
            this.memberId = member.getMemberId();
            this.name = member.getName();
        }
    }

    @Getter
    @AllArgsConstructor
    public static class AdminMemberInfo {
        private Long id;
        private String memberId;
        private String name;

        public AdminMemberInfo(Member member) {
            this.id = member.getId();
            this.memberId = member.getMemberId();
            this.name = member.getName();
        }
    }

    @Getter
    @AllArgsConstructor
    public static class AdminListResponse {
        private List<AdminMemberInfo> memberList;
    }
}
