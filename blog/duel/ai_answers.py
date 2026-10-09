"""Answers a coding assistant gave to the same eight questions.

They are kept exactly as the assistant wrote them: not corrected, not
commented. Run them through the duel and decide for yourself which ones you
would accept:

    python manage.py duel --source ai
"""
from datetime import date

from django.db.models import Count

from blog.models import Author, Comment, Post


def q1():
    return Post.objects.filter(published=True)


def q2():
    return Post.objects.filter(category__isnull=True)


def q3():
    return Post.objects.filter(
        published_at__gt=date(2026, 3, 1),
        published_at__lt=date(2026, 5, 31),
    )


def q4():
    return [post for post in Post.objects.all() if post.comments.count() > 2]


def q5():
    return (
        Post.objects.filter(published=True)
        .annotate(n_comments=Count("comments"), n_tags=Count("tags"))
        .order_by("-n_comments")[:3]
    )


def q6():
    return Post.objects.filter(author__country="Perú")


def q7():
    return Comment.objects.filter(post__category__name="Tecnología")


def q8():
    return Author.objects.filter(posts__published=False)
