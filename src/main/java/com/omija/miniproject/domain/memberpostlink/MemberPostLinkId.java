package com.omija.miniproject.domain.memberpostlink;

import jakarta.persistence.*;

import java.util.*;

@Embeddable
public class MemberPostLinkId {
    @Column(name = "member_id")
    private Integer memberId;

    @Column(name = "post_id")
    private String postId;

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        MemberPostLinkId that = (MemberPostLinkId) o;
        return Objects.equals(memberId, that.memberId) && Objects.equals(postId, that.postId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(memberId, postId);
    }
}
