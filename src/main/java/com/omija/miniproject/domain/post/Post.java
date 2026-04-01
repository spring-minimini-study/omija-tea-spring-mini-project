package com.omija.miniproject.domain.post;

import com.omija.miniproject.common.entity.CreatedAt;
import com.omija.miniproject.domain.memberpostlink.MemberPostLink;
import jakarta.persistence.*;
import lombok.*;

import java.util.*;

@Entity
@Table(name = "post")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Post extends CreatedAt {
    @Id
    private String id;

    @Column(nullable = false)
    private String description;

    @OneToMany(
            mappedBy = "post",
            cascade = CascadeType.ALL,
            orphanRemoval = true
    )
    private List<MemberPostLink> memberPostLinks = new ArrayList<>();

    public int getUserLinkCount() {
        return memberPostLinks.size();
    }
}
