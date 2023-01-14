from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from faker import Faker

from .models import Post, Tag


class ObjectHelpers:
    def set_up(self):
        self.faker = Faker()

    def __init__(self):
        self.objects = []

    def create_super_user(self):
        self.superuser = User.objects.create_superuser(
            username=self.faker.name(),
            email=self.faker.email(),
            password=self.faker.password(),
        )
        self.objects.append(self.superuser)
        return self.superuser

    def create_regular_user(self):
        regular_user = User.objects.create_user(
            username=self.faker.name(),
            email=self.faker.email(),
            password=self.faker.password(),
        )
        self.objects.append(regular_user)
        return regular_user

    def create_tag(self):
        tag = Tag.objects.create(name=self.faker.paragraph(nb_sentences=1))
        self.objects.append(tag)
        return tag

    def create_post(self, author=None):
        if not author:
            author = self.create_regular_user()

        post = Post.objects.create(
            title=self.faker.paragraph(nb_sentences=1),
            author=author,
            body=self.faker.paragraph(nb_sentences=6),
        )

        tags = [self.create_tag() for _ in range(3)]
        post.tags.set(tags)

        self.objects.append(post)
        return post


class ObjectHelpersTestCase(TestCase):
    def setUp(self):
        self.helpers = ObjectHelpers()
        self.helpers.set_up()

    def test_create_superuser(self):
        # Create a superuser using the helper class
        superuser = self.helpers.create_super_user()

        # Verify that the superuser was created and has the 'is_superuser' flag set to True
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_create_regular_user(self):
        # Create a regular user using the helper class
        regular_user = self.helpers.create_regular_user()

        # Verify that the regular user was created and does not have the 'is_superuser' flag set to True
        self.assertFalse(regular_user.is_superuser)
        self.assertFalse(regular_user.is_staff)

    def test_create_tag(self):
        # Create a tag using the helper class
        tag = self.helpers.create_tag()

        # Verify that the tag was created
        self.assertTrue(Tag.objects.filter(pk=tag.pk).exists())

    def test_create_post(self):
        # Create a post using the helper class
        post = self.helpers.create_post()

        # Verify that the post was created
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())

    def test_assign_tags_to_post(self):
        # Create a post using the helper class
        post = self.helpers.create_post()

        # Verify that the tags were assigned to the post
        self.assertEqual(post.tags.count(), 3)


class PostTestCase(TestCase):
    def setUp(self):
        self.helpers = ObjectHelpers()
        self.helpers.set_up()

    def test_str_method(self):
        # Create a regular user using the helper class
        user = self.helpers.create_regular_user()

        # Create a post using the helper class
        post = self.helpers.create_post(author=user)

        # Verify that the __str__ method returns the expected output
        self.assertEqual(str(post), f"{post.title} | {user.username}")

    def test_get_absolute_url(self):
        # Create a post using the helper class
        post = self.helpers.create_post()

        # Verify that the get_absolute_url method returns the expected URL
        self.assertEqual(post.get_absolute_url(), f"/article/{post.slug}")

    def test_save_method(self):
        # Create a post with no slug
        post = Post.objects.create(
            title=self.helpers.faker.paragraph(nb_sentences=1),
            author=self.helpers.create_regular_user(),
            body=self.helpers.faker.paragraph(nb_sentences=6),
        )

        # Verify that the save method generated a slug
        self.assertTrue(post.slug)

    def test_like_count(self):
        # Create a post using the helper class
        post = self.helpers.create_post()

        # Verify that the like_count method returns 0 when no likes have been added
        self.assertEqual(post.like_count(), 0)

        # Create a regular user using the helper class
        user = self.helpers.create_regular_user()

        # Like the post
        post.likes.add(user)

        # Verify that the like_count method returns 1 when one like has been added
        self.assertEqual(post.like_count(), 1)

    def tearDown(self):
        for obj in self.helpers.objects:
            obj.delete()


class TagTestCase(TestCase):
    def setUp(self):
        self.helpers = ObjectHelpers()
        self.helpers.set_up()

    def tearDown(self):
        for obj in self.helpers.objects:
            obj.delete()

    def test_str_method(self):
        # Create a tag using the helper class
        tag = self.helpers.create_tag()

        # Verify that the __str__ method returns the expected output
        self.assertEqual(str(tag), tag.name)

    def test_get_absolute_url(self):
        # Create a tag using the helper class
        tag = self.helpers.create_tag()

        # Verify that the get_absolute_url method returns the expected output
        self.assertEqual(tag.get_absolute_url(), reverse_lazy("article-list"))
