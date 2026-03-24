package com.omija.miniproject.domain.member;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.*;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;

@Tag(name = "Member", description = "유저 관리 API")
@RestController
@RequiredArgsConstructor
@RequestMapping("/member")
class MemberController {
    private final MemberService memberService;

    @Operation(
            summary = "유저 생성",
            description = "유저 정보로 유저 생성"
    )
    @PostMapping
    public ResponseEntity<MemberDto.MemberInfo> createMember(@RequestBody MemberDto.CreateMemberRequest request) {
        MemberDto.MemberInfo member = memberService.createMember(request);

        return ResponseEntity.status(HttpStatus.CREATED).body(member);
    }

    @Operation(
            summary = "단일 유저 조회",
            description = "유저 ID로 단일 유저 조회"
    )
    @GetMapping("/{memberId}")
    public ResponseEntity<MemberDto.MemberInfo> getMember(@PathVariable String memberId) {
        MemberDto.MemberInfo member = memberService.getMemberInfoByMemberId(memberId);

        return ResponseEntity.ok(member);
    }

    @Operation(
            summary = "admin 유저 조회",
            description = "전체 유저 목록 반환"
    )
    @GetMapping("/admin")
    public ResponseEntity<MemberDto.AdminListResponse> getMemberList() {
        MemberDto.AdminListResponse members = memberService.getAllMemberForAdmin();
        return ResponseEntity.ok(members);
    }
}
