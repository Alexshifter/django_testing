from http import HTTPStatus

import pytest
from django.contrib.auth import get_user
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

NEW_COMMENT_TEXT = 'Текст комментария, отправленный через форму'


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
        client,
        news_detail_url):
    def_num_of_comments = Comment.objects.count()
    client.post(news_detail_url, data={'text': NEW_COMMENT_TEXT})
    assert Comment.objects.count() == def_num_of_comments


def test_user_can_create_comment(
        author_client,
        news_detail_url,
        news):
    def_num_comments = Comment.objects.count()
    response = author_client.post(news_detail_url,
                                  data={'text': NEW_COMMENT_TEXT})
    assertRedirects(response, f'{news_detail_url}#comments')
    assert Comment.objects.count() == def_num_comments + 1
    comment = Comment.objects.last()
    assert comment.text == NEW_COMMENT_TEXT
    assert comment.news == news
    assert comment.author == get_user(author_client)


def test_user_cant_use_bad_words(author_client, news_detail_url):
    def_num_comments = Comment.objects.count()
    response = author_client.post(
        news_detail_url,
        data={'text': f'{NEW_COMMENT_TEXT}, {BAD_WORDS[0]}!'}
    )
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == def_num_comments


def test_author_can_delete_comment(
        author_client,
        comment_delete_url,
        news_detail_url):
    def_num_of_comments = Comment.objects.count()
    response = author_client.delete(comment_delete_url)
    assertRedirects(response, news_detail_url + '#comments')
    assert Comment.objects.count() == def_num_of_comments - 1


def test_user_cant_delete_comment_of_another_user(
        admin_client,
        comment_delete_url):
    def_num_of_comments = Comment.objects.count()
    response = admin_client.delete(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == def_num_of_comments


def test_author_can_edit_comment(
        author_client,
        comment_edit_url,
        news_detail_url,
        comment,
        news,
):
    response = author_client.post(
        comment_edit_url,
        data={'text': NEW_COMMENT_TEXT}
    )
    assertRedirects(response, news_detail_url + '#comments')
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT
    assert comment.author == get_user(author_client)
    assert comment.news == news


def test_user_cant_edit_comment_of_another_user(
        admin_client,
        comment_edit_url,
        comment):
    response = admin_client.post(
        comment_edit_url,
        data={'text': NEW_COMMENT_TEXT}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text
    assert comment.author == comment_from_db.author
    assert comment.news == comment_from_db.news
