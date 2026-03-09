package com.omija.miniproject.domain.member;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class MemberService {
    private final MemberRepository memberRepository;

    @Transactional
    public MemberDto.MemberInfo createMember(MemberDto.CreateMemberRequest request) {
        Member member = request.toEntity();
        Member dbMember = memberRepository.save(member);
        return new MemberDto.MemberInfo(dbMember);
    }

    public MemberDto.MemberInfo getMemberInfoByUserId(String userId) {
        Member member = memberRepository.findByUserId(userId).orElseThrow(() -> new IllegalArgumentException("user not exist"));
        return new MemberDto.MemberInfo(member);
    }

    public MemberDto.AdminListResponse getAllMemberForAdmin() {
        List<MemberDto.AdminMemberInfo> MemberInfos = memberRepository.findAll().stream().map(MemberDto.AdminMemberInfo::new).collect(Collectors.toList());
        return new MemberDto.AdminListResponse(MemberInfos);
    }
}
