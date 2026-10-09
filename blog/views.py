from django.shortcuts import render

from .queries import posts_for_front_page


def front_page(request):
    return render(request, "blog/front_page.html", {"posts": posts_for_front_page()})
