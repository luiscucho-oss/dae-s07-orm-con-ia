"""Queries behind the views. Part 2 of the lab happens in this file."""
from blog.models import Post


def posts_for_front_page():
    # The template walks `post.author` and `post.tags` once per post. Without
    # help that is 1 + 2N queries (the N+1 problem):
    # - select_related("author") brings the author in the same query (SQL JOIN),
    #   which works for ForeignKey / OneToOne.
    # - prefetch_related("tags") brings the tags of ALL the posts in a second
    #   query (WHERE post_id IN (...)) and matches them in Python; it is the
    #   tool for ManyToMany and reverse relations.
    # Result: 2 queries no matter how many posts there are.
    return (
        Post.objects.filter(published=True)
        .select_related("author")
        .prefetch_related("tags")
        .order_by("-published_at")
    )
