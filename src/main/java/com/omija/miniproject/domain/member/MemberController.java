package com.omija.miniproject.domain.member;

import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.*;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Tag(name= "Member", description="유저 관리 API")
@RestController
@RequiredArgsConstructor
@RequestMapping("/member")
class MemberController {
    private final MemberService memberService;

    @PostMapping
    public ResponseEntity<MemberDto.MemberInfo> createMember(@RequestBody MemberDto.CreateMemberRequest request) {
        MemberDto.MemberInfo member = memberService.createMember(request);

        return ResponseEntity.status(HttpStatus.CREATED).body(member);
    }

    @GetMapping("/{userId}")
    public ResponseEntity<MemberDto.MemberInfo> getMember(@PathVariable String userId) {
        MemberDto.MemberInfo member = memberService.getMemberInfoByUserId(userId);

        return ResponseEntity.ok(member);
    }

    @GetMapping("/admin")
    public ResponseEntity<MemberDto.AdminListResponse> getMemberList() {
        MemberDto.AdminListResponse members = memberService.getAllMemberForAdmin();
        return ResponseEntity.ok(members);
    }
}
