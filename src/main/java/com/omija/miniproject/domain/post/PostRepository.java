package com.omija.miniproject.domain.post;

import com.omija.miniproject.domain.member.MemberGender;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface PostRepository extends JpaRepository<Post, String> {
    Optional<Post> findById(String s);

    @Query("SELECT DISTINCT p FROM Post p "+
    "JOIN p.memberPostLinks mpl "+
    "JOIN mpl.member m "+
    "WHERE m.gender = :gender")
    List<Post> findPostsByMemberGender(@Param("gender")MemberGender gender);

    @Query("SELECT p FROM Post p "+
    "JOIN p.memberPostLinks mpl "+
    "WHERE mpl.member.id = :memberId")
    List<Post> findPostsByMemberId(@Param("memberId")Long memberId);
}
