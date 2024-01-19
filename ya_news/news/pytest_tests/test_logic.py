from news.models import Comment
import pytest
from pytest_django.asserts import assertRedirects, assertFormError
from news.forms import BAD_WORDS, WARNING
from http import HTTPStatus

DEF_NUM_OF_COMMENTS = 1


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
        client,
        news_detail_url,
        form_data):
    client.post(news_detail_url, data=form_data)
    assert Comment.objects.count() == DEF_NUM_OF_COMMENTS - 1


def test_user_can_create_comment(
        author_client,
        news_detail_url,
        form_data,
        news):
    response = author_client.post(news_detail_url, data=form_data)
    assertRedirects(response, f'{news_detail_url}#comments')
    assert Comment.objects.count() == DEF_NUM_OF_COMMENTS
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author_client.get(news_detail_url).context['user']


def test_user_cant_use_bad_words(author_client, form_data, news_detail_url):
    form_data['text'] += f', {BAD_WORDS[0]}. И еще текст.'
    response = author_client.post(news_detail_url, data=form_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
        author_client,
        comment_delete_url,
        news_detail_url):

    assert Comment.objects.count() == DEF_NUM_OF_COMMENTS
    response = author_client.delete(comment_delete_url)
    assertRedirects(response, news_detail_url + '#comments')
    assert Comment.objects.count() == DEF_NUM_OF_COMMENTS - 1


def test_user_cant_delete_comment_of_another_user(
        admin_client,
        comment_delete_url):
    response = admin_client.delete(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == DEF_NUM_OF_COMMENTS


def test_author_can_edit_comment(
        author_client,
        comment_edit_url,
        news_detail_url,
        form_data, comment):
    response = author_client.post(comment_edit_url, data=form_data)
    assertRedirects(response, news_detail_url + '#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_user_cant_edit_comment_of_another_user(
        admin_client,
        comment_edit_url,
        comment,
        form_data):
    default_comment_text = comment.text
    response = admin_client.post(comment_edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == default_comment_text
