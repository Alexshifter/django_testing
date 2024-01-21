from .conftest import DataForTestModules
from notes.forms import NoteForm


class TestContent(DataForTestModules):

    def test_notes_list_for_different_users(self):
        users_statuses = (
            (self.author_client, True),
            (self.usr_client, False),
        )
        for auth_client, status in users_statuses:
            with self.subTest(
                auth_client=auth_client,
                msg=(
                    'Убедитесь, что в список заметок одного пользователя '
                    'не попадают заметки другого пользователя. Убедитесь, '
                    'что отдельная заметка передается на страницу со списком '
                    'заметок в списке object_list в словаре context.'
                )
            ):
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
                msg=(
                    'Убедитесь, что на страницы создания и редактирования '
                    'заметки передаются  формы'
                )
            ):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
