package com.omija.miniproject.domain.post;

import com.omija.miniproject.domain.memberpostlink.MemberPostLink;
import jakarta.persistence.*;
import lombok.*;

import java.util.*;

@Entity
@Table(name = "post")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Post {
    @Id
    private String id;

    @Column(nullable = false)
    private String description;

    @OneToMany(
            mappedBy = "post",
            cascade = CascadeType.ALL,
            orphanRemoval = true
    )
    private List<MemberPostLink> userPostLinks = new ArrayList<>();

    public int getUserLinkCount() {
        return userPostLinks.size();
    }
}
