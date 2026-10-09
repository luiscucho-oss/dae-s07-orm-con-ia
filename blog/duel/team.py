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
    raise NotImplementedError


def q2():
    """Los artículos que no tienen categoría asignada."""
    raise NotImplementedError


def q3():
    """Los artículos publicados entre el 1 de marzo y el 31 de mayo de 2026, ambos días incluidos."""
    raise NotImplementedError


def q4():
    """Los artículos con más de dos comentarios."""
    raise NotImplementedError


def q5():
    """Los tres artículos publicados con más comentarios; de cada uno, cuántos comentarios
    (`n_comments`) y cuántas etiquetas (`n_tags`)."""
    raise NotImplementedError


def q6():
    """Los artículos escritos por autores de Perú (publicados o no)."""
    raise NotImplementedError


def q7():
    """Los comentarios de los artículos de la categoría «Tecnología»."""
    raise NotImplementedError


def q8():
    """Los autores que nunca han publicado un artículo."""
    raise NotImplementedError
