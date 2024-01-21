from .conftest import DataForTestModules, SUCCESS, FAILURE


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
            (self.notes_home_url, self.client, SUCCESS,),
            (self.login_url, self.client, SUCCESS,),
            (self.logout_url, self.client, SUCCESS,),
            (self.signup_url, self.client, SUCCESS,),
        )
        for url, some_client, exp_status in urls_with_clients:
            with self.subTest(url=url, some_client=some_client):
                response = some_client.get(url)
                self.assertEqual(response.status_code, exp_status)

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
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
