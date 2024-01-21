from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.models import Note

User = get_user_model()

SUCCESS = HTTPStatus.OK
FAILURE = HTTPStatus.NOT_FOUND


class DataForTestModules(TestCase):

    NOTE_TEXT = 'Текст заметки, заданный через форму'
    NOTE_TITLE = 'Заголовок заметки, заданный через форму'
    NEW_NOTE_TEXT = 'Обновлённый текст заметки'
    NEW_NOTE_TITLE = 'Обновленный заголовок заметки'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.usr = User.objects.create(username='Другой пользователь')
        cls.author = User.objects.create(username='Автор')
        cls.notauthor = User.objects.create(username='Не автор')
        cls.note = Note.objects.create(
            title='Заголовок заметки',
            text='Текст заметки',
            author=cls.author,
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.usr_client = Client()
        cls.usr_client.force_login(cls.usr)
        cls.notauthor_client = Client()
        cls.notauthor_client.force_login(cls.notauthor)
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
        }
        cls.data_with_notunique_slug = {
            'slug': cls.note.slug,
            'text': cls.NOTE_TEXT,
            'title': cls.NOTE_TITLE,
        }

        cls.form_new_data = {
            'title': cls.NEW_NOTE_TITLE,
            'text': cls.NEW_NOTE_TEXT,
            'slug': slugify(cls.NEW_NOTE_TITLE),
        }
        cls.notes_home_url = reverse('notes:home')
        cls.notes_list_url = reverse('notes:list')
        cls.notes_detail_url = reverse('notes:detail', args=(cls.note.slug,))
        cls.notes_add_url = reverse('notes:add')
        cls.notes_edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.notes_delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.notes_success_url = reverse('notes:success')
        cls.login_url = reverse('users:login')
        cls.logout_url = reverse('users:logout')
        cls.signup_url = reverse('users:signup')
