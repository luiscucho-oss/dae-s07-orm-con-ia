from django.core.management.base import BaseCommand
from django.db import transaction

from blog import seed_data
from blog.models import Author, Category, Comment, Post, Profile, Tag


class Command(BaseCommand):
    help = "Carga los datos fijos del laboratorio (borra los del blog antes de cargar)."

    @transaction.atomic
    def handle(self, *args, **options):
        # Comments and posts go first; authors, categories and tags after them.
        for model in (Comment, Post, Profile, Author, Category, Tag):
            model.objects.all().delete()

        authors = {}
        for name, country in seed_data.AUTHORS:
            author = Author.objects.create(name=name)
            Profile.objects.create(author=author, country=country)
            authors[name] = author
        categories = {name: Category.objects.create(name=name) for name in seed_data.CATEGORIES}
        tags = {name: Tag.objects.create(name=name) for name in seed_data.TAGS}

        for item in seed_data.POSTS:
            post = Post.objects.create(
                title=item["title"],
                body=f"Cuerpo de «{item['title']}».",
                author=authors[item["author"]],
                category=categories.get(item["category"]),
                published=item["published"],
                published_at=item["date"],
            )
            post.tags.set([tags[name] for name in item["tags"]])
            for author_name, text in seed_data.comments_of(item):
                Comment.objects.create(post=post, author_name=author_name, text=text)

        if options["verbosity"] > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Listo: {Author.objects.count()} autores, {Post.objects.count()} artículos, "
                    f"{Comment.objects.count()} comentarios."
                )
            )
