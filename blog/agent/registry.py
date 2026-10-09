"""A closed list of actions: the only things a language model may ask for.

The model never gets a shell, an `eval` or a raw ORM. It emits an *intent*
(`{"action": ..., "args": {...}}`) and `execute` decides. Three rules:

1. Only actions in `ACTIONS` exist. Anything else is denied, not interpreted.
2. Reads (R0) run, and what they return is wrapped as `untrusted_data`: a
   comment that says "ignore your instructions" is a string, not an order.
3. Destructive writes (R2) never run on the model's say-so. `execute` returns a
   plan with a hash; only the same plan, approved by a human who passes that
   hash back, is applied.
"""
import hashlib
import json
from dataclasses import dataclass
from typing import Any, Callable

from django.db import transaction
from django.db.models import Count

from blog.models import Comment, Post


@dataclass(frozen=True)
class Action:
    name: str
    risk: str  # "R0" reads, "R2" destructive
    params: dict[str, type]
    description: str
    run: Callable[..., Any]
    plan: Callable[..., dict] | None = None  # only R2 actions have one


# --- R0: reads ---------------------------------------------------------------


def _posts_by_category(category: str):
    posts = Post.objects.filter(category__name=category).values("id", "title")
    return list(posts)


def _comments_of_post(post_id: int):
    return list(Comment.objects.filter(post_id=post_id).values("author_name", "text"))


def _posts_per_author():
    rows = Post.objects.values("author__name").annotate(total=Count("id")).order_by("-total")
    return [{"author": row["author__name"], "total": row["total"]} for row in rows]


# --- R2: destructive ---------------------------------------------------------


def _plan_delete_comments(post_id: int) -> dict:
    ids = list(Comment.objects.filter(post_id=post_id).order_by("id").values_list("id", flat=True))
    return {"affected_comment_ids": ids}


def _delete_comments(post_id: int):
    with transaction.atomic():
        deleted, _ = Comment.objects.filter(post_id=post_id).delete()
    return {"deleted": deleted}


ACTIONS: dict[str, Action] = {
    action.name: action
    for action in (
        Action("posts_by_category", "R0", {"category": str},
               "Lista los artículos de una categoría.", _posts_by_category),
        Action("comments_of_post", "R0", {"post_id": int},
               "Lista los comentarios de un artículo.", _comments_of_post),
        Action("posts_per_author", "R0", {},
               "Cuenta los artículos de cada autor.", _posts_per_author),
        Action("delete_comments_of_post", "R2", {"post_id": int},
               "Borra todos los comentarios de un artículo.", _delete_comments,
               plan=_plan_delete_comments),
    )
}


# --- the gate ----------------------------------------------------------------


def _denied(reason: str) -> dict:
    return {"status": "denied", "reason": reason}


def _valid_args(action: Action, args: Any) -> str | None:
    """None if the arguments fit the action exactly; otherwise why they do not."""
    if not isinstance(args, dict):
        return "args must be an object"
    if set(args) != set(action.params):
        return f"expected arguments {sorted(action.params)}, got {sorted(args)}"
    for name, kind in action.params.items():
        value = args[name]
        # bool is an int in Python; `True` is not a valid post_id
        if not isinstance(value, kind) or isinstance(value, bool):
            return f"argument {name!r} must be {kind.__name__}"
    return None


def plan_hash(action: Action, args: dict, details: dict) -> str:
    canonical = json.dumps(
        {"action": action.name, "args": args, "details": details}, sort_keys=True
    )
    return hashlib.sha256(canonical.encode()).hexdigest()[:12]


def execute(intent: Any, approval: str | None = None) -> dict:
    """Decide what to do with an intent. `approval` comes from a human, never from the model."""
    if not isinstance(intent, dict):
        return _denied("the intent must be an object")
    action = ACTIONS.get(intent.get("action"))
    if action is None:
        return _denied(f"unknown action {intent.get('action')!r}")
    args = intent.get("args", {})
    problem = _valid_args(action, args)
    if problem:
        return _denied(problem)

    if action.risk == "R0":
        return {"status": "ok", "untrusted_data": action.run(**args)}

    # R2: build the plan from the CURRENT state. If anything changed since the
    # human looked at it, the hash changes and the old approval stops working.
    details = action.plan(**args)
    digest = plan_hash(action, args, details)
    plan = {"action": action.name, "args": args, "details": details, "plan_hash": digest}
    if approval != digest:
        return {"status": "approval_required", "plan": plan}
    return {"status": "applied", "plan": plan, "result": action.run(**args)}


def tools_for_prompt() -> str:
    """The catalogue shown to the model: names, arguments and what each does."""
    lines = []
    for action in ACTIONS.values():
        params = ", ".join(f"{name}: {kind.__name__}" for name, kind in action.params.items())
        lines.append(f"- {action.name}({params}) [{action.risk}] {action.description}")
    return "\n".join(lines)
