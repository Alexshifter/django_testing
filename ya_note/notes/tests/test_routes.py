from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

SUCCESS = HTTPStatus.OK
FAILURE = HTTPStatus.NOT_FOUND


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
        cls.anonym_client = Client()
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.usr_client = Client()
        cls.usr_client.force_login(cls.usr)
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


class TestRoutes(DataForTestModules):

    def test_availability_diff_pages_for_diff_users(self):
        urls_with_clients = (
            (self.notes_list_url, self.author_client, SUCCESS,),
            (self.notes_add_url, self.author_client, SUCCESS,),
            (self.notes_detail_url, self.author_client, SUCCESS,),
            (self.notes_edit_url, self.author_client, SUCCESS,),
            (self.notes_delete_url, self.author_client, SUCCESS,),
            (self.notes_success_url, self.author_client, SUCCESS,),
            (self.notes_detail_url, self.usr_client, FAILURE,),
            (self.notes_edit_url, self.usr_client, FAILURE,),
            (self.notes_delete_url, self.usr_client, FAILURE,),
        )
        for url, some_client, exp_status in urls_with_clients:
            with self.subTest(url=url, some_client=some_client):
                response = some_client.get(url)
                self.assertEqual(response.status_code, exp_status)

    def test_availability_diff_pages_for_anonymous(self):
        urls = (
            self.notes_home_url,
            self.login_url,
            self.logout_url,
            self.signup_url,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.anonym_client.get(url)
                self.assertEqual(response.status_code, SUCCESS)

    def test_redirect_for_anonymous_client(self):
        urls = (
            self.notes_list_url,
            self.notes_add_url,
            self.notes_detail_url,
            self.notes_edit_url,
            self.notes_delete_url,
            self.notes_success_url,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{self.login_url}?next={url}'
                response = self.anonym_client.get(url)
                self.assertRedirects(response, redirect_url)
