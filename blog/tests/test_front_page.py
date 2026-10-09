"""Part 2 of the lab: take this test from red to green.

`test_front_page_runs_two_queries` FAILS in the starter on purpose. The page is
correct; it is just expensive. Edit `blog/queries.py` until it passes.
"""
import importlib.util
import unittest
from unittest import mock

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

HAS_TEACHER = importlib.util.find_spec("teacher") is not None


class FrontPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_blog", verbosity=0)

    def test_front_page_shows_the_published_posts(self):
        response = self.client.get(reverse("front_page"))
        self.assertContains(response, "Introducción al ORM de Django")
        self.assertNotContains(response, "Borrador: migraciones")

    def test_front_page_runs_two_queries(self):
        # one for the posts (with their author), one for all their tags
        with self.assertNumQueries(2):
            self.client.get(reverse("front_page"))

    @unittest.skipUnless(HAS_TEACHER, "carpeta teacher/ ausente")
    def test_the_reference_solution_is_green(self):
        from teacher import solutions

        with mock.patch("blog.views.posts_for_front_page", solutions.posts_for_front_page):
            with self.assertNumQueries(2):
                self.client.get(reverse("front_page"))
