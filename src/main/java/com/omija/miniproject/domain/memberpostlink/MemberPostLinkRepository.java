package com.omija.miniproject.domain.memberpostlink;

import com.omija.miniproject.domain.post.Post;
import org.springframework.data.jpa.repository.*;
import org.springframework.data.repository.query.Param;

import java.util.*;

public interface MemberPostLinkRepository extends JpaRepository<MemberPostLink, MemberPostLinkId> {
    @Query("SELECT l.post FROM MemberPostLink l " +
            "WHERE l.member.id = :memberId")
    List<Post> findAllPostsByMemberId(@Param("memberId") Long memberId);
}
