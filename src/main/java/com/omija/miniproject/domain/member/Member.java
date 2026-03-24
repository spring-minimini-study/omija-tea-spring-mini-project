package com.omija.miniproject.domain.member;

import com.omija.miniproject.common.entity.CreatedAt;
import com.omija.miniproject.domain.memberpostlink.MemberPostLink;
import com.omija.miniproject.domain.post.Post;
import jakarta.persistence.*;
import lombok.*;

import java.util.ArrayList;
import java.util.List;

@Entity
@Getter
@Table(name = "member")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Member extends CreatedAt {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique=true, nullable=false)
    private String memberId;

    @Column(nullable=false)
    private String name;

    @OneToMany(
            mappedBy = "member",
            cascade = CascadeType.ALL,
            orphanRemoval = true
    )
    private List<MemberPostLink> memberPostLinks = new ArrayList<>();

    public void addPost(Post post){
        boolean alreadyLinked = memberPostLinks.stream().anyMatch(link -> link.getPost().equals(post));
        if(!alreadyLinked){
            MemberPostLink link = MemberPostLink.of(this, post);
            memberPostLinks.add(link);
        }
    }

    public void removePost(Post post){
        memberPostLinks.removeIf(link -> link.getPost().equals(post));
    }

    public boolean isBookmarked(Post post){
        return memberPostLinks.stream().anyMatch(link -> link.getPost().equals(post));
    }

    @Builder
    public Member(String memberId, String name){
        this.memberId = memberId;
        this.name = name;
    }
}
