from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note


User = get_user_model()


class TestNoteCreation(TestCase):

    NOTE_TEXT = 'Текст заметки'
    NOTE_TITLE = 'Заголовок заметки'
    DEF_NUM_OF_NOTES = 1
    NOTE_SLUG = slugify(NOTE_TITLE)

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('notes:add')
        cls.user1 = User.objects.create(username='Пользователь 1')
        cls.user2 = User.objects.create(username='Пользователь 2')
        cls.note = Note.objects.create(
            title='Заголовок заметки 1',
            text=cls.NOTE_TEXT,
            author=cls.user1,
        )
        cls.auth_client1 = Client()
        cls.auth_client1.force_login(cls.user1)
        cls.auth_client2 = Client()
        cls.auth_client2.force_login(cls.user2)
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
        }

        cls.data_with_notunique_slug = {
            'slug': cls.note.slug,
            'text': cls.NOTE_TEXT,
            'title': cls.NOTE_TITLE,
        }

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.url, data=self.form_data)
        notes_count_after_post = Note.objects.count()
        self.assertEqual(self.DEF_NUM_OF_NOTES, notes_count_after_post)

    def test_user_can_create_note(self):
        response = self.auth_client1.post(self.url, data=self.form_data)
        url_success = reverse('notes:success',)
        self.assertRedirects(response, url_success)
        self.assertEqual(Note.objects.count(), self.DEF_NUM_OF_NOTES + 1)
        note = Note.objects.all().order_by('-id')[0]
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.title, self.NOTE_TITLE)
        self.assertEqual(note.slug, self.NOTE_SLUG)
        self.assertEqual(note.author, self.user1)

    def test_user_cant_use_notunique_slug(self):
        response = self.auth_client2.post(
            self.url,
            data=self.data_with_notunique_slug,
        )
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=self.data_with_notunique_slug['slug'] + WARNING,
        )
        note_count = Note.objects.count()
        self.assertEqual(note_count, self.DEF_NUM_OF_NOTES)


class TestNoteEditDelete(TestCase):

    NOTE_TEXT = 'Текст заметки'
    NOTE_TITLE = 'Заголовок заметки'
    NEW_NOTE_TEXT = 'Обновлённый текст заметки'
    NEW_NOTE_TITLE = 'Обновленный заголовок заметки'
    NEW_NOTE_SLUG = slugify('Обновленный слаг заметки')
    DEF_NUM_OF_NOTES = 1

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.note = Note.objects.create(
            title='Заголовок заметки',
            text='Текст заметки',
            author=cls.author,
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.notauthor = User.objects.create(username='Не автор заметки')
        cls.notauthor_client = Client()
        cls.notauthor_client.force_login(cls.notauthor)
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.success_url = reverse('notes:success')
        cls.form_data = {'title': cls.NEW_NOTE_TITLE,
                         'text': cls.NEW_NOTE_TEXT,
                         'slug': cls.NEW_NOTE_SLUG,
                         }

    def test_author_can_delete_note(self):
        self.assertEqual(Note.objects.count(), self.DEF_NUM_OF_NOTES)
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.success_url)
        self.assertEqual(Note.objects.count(), self.DEF_NUM_OF_NOTES - 1)

    def test_user_cant_delete_note_of_another_user(self):
        response = self.notauthor_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), self.DEF_NUM_OF_NOTES)

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            self.edit_url,
            data=self.form_data,
        )
        self.assertRedirects(response, self.success_url)
        self.note.refresh_from_db()
        note_values_const_values = (
            (self.note.title, self.NEW_NOTE_TITLE,),
            (self.note.text, self.NEW_NOTE_TEXT,),
            (self.note.slug, self.NEW_NOTE_SLUG,),
        )
        for value, const_value in note_values_const_values:
            with self.subTest(value=value):
                self.assertEqual(value, const_value)
                self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)
                self.assertEqual(self.note.title, self.NEW_NOTE_TITLE)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.notauthor_client.post(
            self.edit_url,
            data=self.form_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        note_values_const_values = (
            (self.note.title, self.NOTE_TITLE,),
            (self.note.text, self.NOTE_TEXT,),
        )
        for value, const_value in note_values_const_values:
            with self.subTest(value=value):
                self.assertEqual(value, const_value)
                self.assertEqual(self.note.title, self.NOTE_TITLE)
                self.assertEqual(self.note.text, self.NOTE_TEXT)
                self.assertNotEqual(self.note.slug, self.NEW_NOTE_SLUG)
