import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_order(all_news, client, home_url):
    response = client.get(home_url)
    all_news_instances = response.context['object_list']
    all_dates = [news.date for news in all_news_instances]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_news_count(all_news, client, home_url):
    response = client.get(home_url)
    news_count = response.context['object_list'].count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_comments_order(
    client,
    some_comments_under_news,
    news,
    news_detail_url,
):
    response = client.get(news_detail_url)
    assert 'news' in response.context
    all_comments = news.comment_set.all()
    all_dates_comments = [comment.created for comment in all_comments]
    all_dates_comments_sorted = sorted(all_dates_comments)
    assert all_dates_comments == all_dates_comments_sorted


@pytest.mark.parametrize(
    'parametrized_client, comment_form_access_status',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),

    )
)
def test_different_client_has_form(
    news,
    parametrized_client,
    comment_form_access_status,
    news_detail_url,
):
    response = parametrized_client.get(news_detail_url)
    assert ('form' in response.context) is comment_form_access_status
    if comment_form_access_status:
        assert isinstance(response.context['form'], CommentForm)
