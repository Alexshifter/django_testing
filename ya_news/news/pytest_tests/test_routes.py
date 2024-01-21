from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

SUCCESS = HTTPStatus.OK
FAILURE = HTTPStatus.NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, parametrize_client, exp_status',
    (
        (lf('home_url'), lf('client'), SUCCESS),
        (lf('users_login_url'), lf('client'), SUCCESS),
        (lf('users_logout_url'), lf('client'), SUCCESS),
        (lf('users_signup_url'), lf('client'), SUCCESS),
        (lf('news_detail_url'), lf('client'), SUCCESS),
        (lf('comment_edit_url'), lf('author_client'), SUCCESS),
        (lf('comment_edit_url'), lf('admin_client'), FAILURE),
        (lf('comment_delete_url'), lf('author_client'), SUCCESS),
        (lf('comment_delete_url'), lf('admin_client'), FAILURE),
    ),
)
def test_availability_diff_pages_for_diff_users(
    url,
    parametrize_client,
    exp_status,
):
    response = parametrize_client.get(url)
    assert response.status_code == exp_status


@pytest.mark.parametrize(
    'url',
    (
        lf('comment_edit_url'),
        lf('comment_delete_url'),
    )
)
def test_redirect_for_anonymous_client(client, url, users_login_url):
    redirect_url = f'{users_login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
