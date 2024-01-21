from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class DataForTestModules(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.usr = User.objects.create(username='Пользователь')
        cls.note = Note.objects.create(
            title='Заголовок заметки',
            text='Текст заметки',
            author=cls.author,
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.usr_client = Client()
        cls.usr_client.force_login(cls.usr)
        cls.notes_list_url = reverse('notes:list')
        cls.notes_add_url = reverse('notes:add')
        cls.notes_edit_url = reverse('notes:edit', args=(cls.note.slug,))


class TestContent(DataForTestModules):

    def test_notes_list_for_different_users(self):
        users_statuses = (
            (self.author_client, True),
            (self.usr_client, False),
        )
        for auth_client, status in users_statuses:
            with self.subTest(
                auth_client=auth_client,
                msg='Убедитесь, что в список заметок одного пользователя'
                    ' не попадают заметки другого пользователя.\n Убедитесь,'
                    ' что отдельная заметка передается на страницу со списком'
                    ' заметок в списке object_list в словаре context'):
                response = auth_client.get(self.notes_list_url)
                all_notes = response.context['object_list']
                self.assertEqual(self.note in all_notes, status)

    def test_pages_contains_form(self):
        urls = (
            self.notes_add_url,
            self.notes_edit_url,
        )
        for url in urls:
            with self.subTest(
                url=urls,
                msg='Убедитесь, что на страницы создания и редактирования'
                    ' заметки передаются  формы'):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
