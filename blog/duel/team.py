"""YOUR answers. One function per question, no arguments.

Write the ORM query that answers each question and return it (a QuerySet or a
list). Do not write SQL and do not filter in Python what the database can
filter. Check yourself with:

    python manage.py duel                 # all of them
    python manage.py duel --question q4   # just one

Question 5 asks for two numbers per post: annotate them as `n_comments` and
`n_tags`.
"""
from datetime import date  # noqa: F401  (you will need it in question 3)

from django.db.models import Count, Q  # noqa: F401

from blog.models import Author, Category, Comment, Post, Profile, Tag  # noqa: F401


def q1():
    """Los artículos que ya están publicados."""
    return Post.objects.filter(published=True).order_by("published_at")


def q2():
    """Los artículos que no tienen categoría asignada."""
    return Post.objects.filter(category__isnull=True).order_by("title")


def q3():
    """Los artículos publicados entre el 1 de marzo y el 31 de mayo de 2026, ambos días incluidos."""
    # Chained filters on single-valued fields are ANDed in the same WHERE.
    # published_at is a DateField, so __range (BETWEEN) includes both ends.
    return (
        Post.objects.filter(published=True)
        .filter(published_at__range=(date(2026, 3, 1), date(2026, 5, 31)))
        .order_by("published_at")
    )


def q4():
    """Los artículos con más de dos comentarios."""
    return (
        Post.objects.annotate(n_comments=Count("comments"))
        .filter(n_comments__gt=2)
        .order_by("-n_comments", "title")
    )


def q5():
    """Los tres artículos publicados con más comentarios; de cada uno, cuántos comentarios
    (`n_comments`) y cuántas etiquetas (`n_tags`)."""
    # Two joins (comments and tags) multiply the rows: distinct=True keeps each count honest.
    return (
        Post.objects.filter(published=True)
        .annotate(
            n_comments=Count("comments", distinct=True),
            n_tags=Count("tags", distinct=True),
        )
        .order_by("-n_comments", "title")[:3]
    )


def q6():
    """Los artículos escritos por autores de Perú (publicados o no)."""
    # The country lives in the one-to-one Profile, not in Author.
    return Post.objects.filter(author__profile__country="Perú").order_by("author__name", "title")


def q7():
    """Los comentarios de los artículos de la categoría «Tecnología»."""
    return Comment.objects.filter(post__category__name="Tecnología").order_by(
        "post__title", "created_at"
    )


def q8():
    """Los autores que nunca han publicado un artículo."""
    # exclude() also keeps authors with drafts only, not just the ones with no posts at all.
    return Author.objects.exclude(posts__published=True).order_by("name")
