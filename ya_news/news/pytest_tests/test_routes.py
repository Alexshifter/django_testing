from http import HTTPStatus

from pytest_django.asserts import assertRedirects
import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('home_url'),
        pytest.lazy_fixture('news_detail_url'),
        pytest.lazy_fixture('users_login_url'),
        pytest.lazy_fixture('users_logout_url'),
        pytest.lazy_fixture('users_signup_url'),
    ),
)
def test_availability_pages_for_anonymous(client, url):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('comment_edit_url'),
        pytest.lazy_fixture('comment_delete_url'),

    )
)
@pytest.mark.parametrize(
    'parametrized_client, exp_status',
    (
        (
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture('admin_client'),
            HTTPStatus.NOT_FOUND),
    )
)
def test_availability_for_comment_edit_and_delete(
    url,
    parametrized_client,
    exp_status
):
    response = parametrized_client.get(url)
    assert response.status_code == exp_status


@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('comment_edit_url'),
        pytest.lazy_fixture('comment_delete_url'),
    )
)
def test_redirect_for_anonymous_client(client, url, users_login_url):
    redirect_url = f'{users_login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
