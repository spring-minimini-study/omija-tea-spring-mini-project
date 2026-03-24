package com.omija.miniproject.domain.memberpostlink;

import com.omija.miniproject.common.entity.CreatedAt;
import com.omija.miniproject.domain.member.Member;
import com.omija.miniproject.domain.post.Post;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.*;

@Entity
@Table(
        name = "member_post_link",
        indexes = {
                @Index(name = "ix_userpostlink_post_id", columnList = "post_id"),
                @Index(name = "ix_userpostlink_member_id", columnList = "member_id")
        }
)
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class MemberPostLink extends CreatedAt {
    @EmbeddedId //복합키 클래스를 PK로 쓰겠다는것.
    private MemberPostLinkId id = new MemberPostLinkId();

    @ManyToOne(fetch = FetchType.LAZY)
    @MapsId("memberId")
    @JoinColumn(name = "member_id")
    @OnDelete(action = OnDeleteAction.CASCADE)
    private Member member;

    @ManyToOne(fetch = FetchType.LAZY)
    @MapsId("postId")
    @JoinColumn(name = "post_id")
    @OnDelete(action = OnDeleteAction.CASCADE)
    private Post post;

    private String memo;

    public static MemberPostLink of(Member member, Post post) {
        MemberPostLink link = new MemberPostLink();
        link.member = member;
        link.post = post;
        return link;
    }

    public static MemberPostLink of(Member member, Post post, String memo) {
        MemberPostLink link = of(member, post);
        link.memo = memo;
        return link;
    }

}