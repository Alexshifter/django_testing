# news/tests/test_routes.py
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.usr = User.objects.create(username='Пользователь')
        cls.note = Note.objects.create(
            title='Заголовок заметки',
            text='Текст заметки',
            author=cls.author,
        )

    def test_home_page(self):
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability(self):
        names = (
            'notes:home',
            'users:login',
            'users:logout',
            'users:signup',
        )
        for name in names:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_diff_pages_for_auth_user(self):
        names = (
            'notes:list',
            'notes:add',
            'notes:success',
        )
        self.client.force_login(self.author)
        for name in names:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_notes_edit_and_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.usr, HTTPStatus.NOT_FOUND),
        )
        names = ('notes:edit', 'notes:delete', 'notes:detail')
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in names:
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        names = (
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:add', None),
            ('notes:success', None),
            ('notes:list', None),
            ('notes:detail', (self.note.slug,)),
        )
        for name, args in names:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
