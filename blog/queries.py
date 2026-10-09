"""Queries behind the views. Part 2 of the lab happens in this file."""
from blog.models import Post


def posts_for_front_page():
    # TODO(team): this works, but the template walks `post.author` and
    # `post.tags` once per post, so the number of queries grows with the number
    # of posts (the N+1 problem). Fix it here so the test in
    # blog/tests/test_front_page.py goes from red to green.
    return Post.objects.filter(published=True).order_by("-published_at")
