"""Answers a coding assistant gave LIVE in the lab session (step 8, authorized by the teacher).

The assistant only received the content of blog/models.py and the text of the
eight questions; it did not see the repository, the expected answers or the
other answer files. They are kept exactly as the assistant wrote them:

    python manage.py duel --source ai_live
"""
from datetime import date

from django.db.models import Count, Q

from blog.models import Author, Comment, Post


def q1():
    # Artículos ya publicados
    return Post.objects.filter(published=True)


def q2():
    # Artículos sin categoría asignada
    return Post.objects.filter(category__isnull=True)


def q3():
    # Publicados entre el 1/03/2026 y el 31/05/2026, ambos incluidos
    return Post.objects.filter(
        published=True,
        published_at__range=(date(2026, 3, 1), date(2026, 5, 31)),
    )


def q4():
    # Artículos con más de dos comentarios
    return Post.objects.annotate(num_comments=Count("comments")).filter(num_comments__gt=2)


def q5():
    # Top 3 artículos publicados por número de comentarios, con n_comments y n_tags
    return (
        Post.objects.filter(published=True)
        .annotate(
            n_comments=Count("comments", distinct=True),
            n_tags=Count("tags", distinct=True),
        )
        .order_by("-n_comments", "pk")[:3]
    )


def q6():
    # Artículos de autores de Perú (publicados o no)
    return Post.objects.filter(
        Q(author__profile__country__iexact="Perú") | Q(author__profile__country__iexact="Peru")
    )


def q7():
    # Comentarios de artículos de la categoría «Tecnología»
    return Comment.objects.filter(post__category__name="Tecnología")


def q8():
    # Autores que nunca han publicado un artículo (sin posts o solo con borradores)
    return Author.objects.exclude(posts__published=True)
