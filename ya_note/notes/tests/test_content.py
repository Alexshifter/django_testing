# news/tests/test_content.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.usr = User.objects.create(username='Пользователь')
        cls.note = Note.objects.create(
            title='Заголовок заметки',
            text='Текст заметки',
            author=cls.author,
        )

    def test_notes_list_for_different_users(self):
        users_statuses = (
            (self.author, True),
            (self.usr, False),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            response = self.client.get(reverse('notes:list'))
            object_list = response.context['object_list']
            self.assertEqual(self.note in object_list, status)

    def test_pages_contains_form(self):
        names = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        self.client.force_login(self.author)
        for name, args in names:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
