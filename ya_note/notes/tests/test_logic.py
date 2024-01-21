from http import HTTPStatus

from pytils.translit import slugify

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class DataForTestModules(TestCase):

    NOTE_TEXT = 'Текст заметки, заданный через форму'
    NOTE_TITLE = 'Заголовок заметки, заданный через форму'
    NEW_NOTE_TEXT = 'Обновлённый текст заметки'
    NEW_NOTE_TITLE = 'Обновленный заголовок заметки'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.notauthor = User.objects.create(username='Не автор')
        cls.note = Note.objects.create(
            title='Заголовок заметки',
            text='Текст заметки',
            author=cls.author,
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
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
        cls.notes_add_url = reverse('notes:add')
        cls.notes_success_url = reverse('notes:success')


class TestNoteCreation(DataForTestModules):

    def test_anonymous_user_cant_create_note(self):
        def_notes_count = Note.objects.count()
        self.client.post(self.notes_add_url, data=self.form_data)
        self.assertEqual(Note.objects.count(), def_notes_count)

    def test_user_can_create_note(self):
        def_notes_count = Note.objects.count()
        response = self.author_client.post(
            self.notes_add_url,
            data=self.form_data,
        )
        self.assertRedirects(response, self.notes_success_url)
        self.assertEqual(Note.objects.count(), def_notes_count + 1)
        note = Note.objects.last()
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.title, self.NOTE_TITLE)
        self.assertEqual(note.slug, slugify(self.NOTE_TITLE))
        self.assertEqual(note.author, self.author)

    def test_user_cant_use_notunique_slug(self):
        def_notes_count = Note.objects.count()
        response = self.author_client.post(
            self.notes_add_url,
            data=self.data_with_notunique_slug,
        )
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=self.data_with_notunique_slug['slug'] + WARNING,
        )
        self.assertEqual(Note.objects.count(), def_notes_count)


class TestNoteEditDelete(DataForTestModules):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {'title': cls.NEW_NOTE_TITLE,
                         'text': cls.NEW_NOTE_TEXT,
                         'slug': slugify(cls.NEW_NOTE_TITLE),
                         }
        cls.notes_edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.notes_delete_url = reverse('notes:delete', args=(cls.note.slug,))

    def test_author_can_delete_note(self):
        def_notes_count = Note.objects.count()
        response = self.author_client.delete(self.notes_delete_url)
        self.assertRedirects(response, self.notes_success_url)
        self.assertEqual(Note.objects.count(), def_notes_count - 1)

    def test_user_cant_delete_note_of_another_user(self):
        def_notes_count = Note.objects.count()
        response = self.notauthor_client.delete(self.notes_delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), def_notes_count)

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            self.notes_edit_url,
            data=self.form_data,
        )
        self.assertRedirects(response, self.notes_success_url)
        self.note.refresh_from_db()
        note_values_setup_values = (
            (self.note.title, self.NEW_NOTE_TITLE,),
            (self.note.text, self.NEW_NOTE_TEXT,),
            (self.note.slug, slugify(self.NEW_NOTE_TITLE),),
            (self.note.author, self.author),
        )
        for value, setup_value in note_values_setup_values:
            with self.subTest(value=value, setup_value=setup_value):
                self.assertEqual(value, setup_value)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.notauthor_client.post(
            self.notes_edit_url,
            data=self.form_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        note_values_setup_values = (
            (note_from_db.title, self.note.title,),
            (note_from_db.text, self.note.text,),
            (note_from_db.author, self.note.author,),
        )
        for value, setup_value in note_values_setup_values:
            with self.subTest(value=value, setup_value=setup_value):
                self.assertEqual(value, setup_value)
