"""The eight questions of the duel and the expected answer of each one.

`expected` is computed from `seed_data` with plain Python (no ORM). A question
also says how to turn what an answer returns into something comparable
(`normalize`) and how many queries a good answer may cost (`budget`).
"""
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from typing import Any

from blog import seed_data

POSTS = seed_data.POSTS
COUNTRY_OF = dict(seed_data.AUTHORS)


@dataclass(frozen=True)
class Question:
    key: str
    text: str  # the question as the teacher dictates it
    contract: str  # what the answer function must return
    expected: Any
    normalize: Callable[[Any], Any]
    budget: int = 1  # a good answer needs this many queries at most


def _titles(posts):
    return sorted(post.title for post in posts)


def _expected_top_three():
    published = [p for p in POSTS if p["published"]]
    ranked = sorted(published, key=lambda p: -p["comments"])[:3]
    return [(p["title"], p["comments"], len(p["tags"])) for p in ranked]


def _expected_authors_without_published():
    published_by = {p["author"] for p in POSTS if p["published"]}
    return sorted(name for name, _ in seed_data.AUTHORS if name not in published_by)


QUESTIONS = [
    Question(
        key="q1",
        text="Los artículos que ya están publicados.",
        contract="un QuerySet (o lista) de Post",
        expected=sorted(p["title"] for p in POSTS if p["published"]),
        normalize=_titles,
    ),
    Question(
        key="q2",
        text="Los artículos que no tienen categoría asignada.",
        contract="un QuerySet (o lista) de Post",
        expected=sorted(p["title"] for p in POSTS if p["category"] is None),
        normalize=_titles,
    ),
    Question(
        key="q3",
        text="Los artículos publicados entre el 1 de marzo y el 31 de mayo de 2026, "
             "ambos días incluidos.",
        contract="un QuerySet (o lista) de Post",
        expected=sorted(
            p["title"] for p in POSTS
            if p["date"] is not None and date(2026, 3, 1) <= p["date"] <= date(2026, 5, 31)
        ),
        normalize=_titles,
    ),
    Question(
        key="q4",
        text="Los artículos con más de dos comentarios.",
        contract="un QuerySet (o lista) de Post",
        expected=sorted(p["title"] for p in POSTS if p["comments"] > 2),
        normalize=_titles,
    ),
    Question(
        key="q5",
        text="Los tres artículos publicados con más comentarios, y de cada uno cuántos "
             "comentarios y cuántas etiquetas tiene.",
        contract="un QuerySet de Post ordenado, anotado con `n_comments` y `n_tags`",
        expected=_expected_top_three(),
        normalize=lambda posts: [(p.title, p.n_comments, p.n_tags) for p in list(posts)[:3]],
    ),
    Question(
        key="q6",
        text="Los artículos escritos por autores de Perú (publicados o no).",
        contract="un QuerySet (o lista) de Post",
        expected=sorted(p["title"] for p in POSTS if COUNTRY_OF[p["author"]] == "Perú"),
        normalize=_titles,
    ),
    Question(
        key="q7",
        text="Los comentarios de los artículos de la categoría «Tecnología».",
        contract="un QuerySet (o lista) de Comment",
        expected=sorted(
            text
            for p in POSTS if p["category"] == "Tecnología"
            for _author, text in seed_data.comments_of(p)
        ),
        normalize=lambda comments: sorted(c.text for c in comments),
    ),
    Question(
        key="q8",
        text="Los autores que nunca han publicado un artículo.",
        contract="un QuerySet (o lista) de Author",
        expected=_expected_authors_without_published(),
        normalize=lambda authors: sorted(a.name for a in authors),
    ),
]

BY_KEY = {question.key: question for question in QUESTIONS}
