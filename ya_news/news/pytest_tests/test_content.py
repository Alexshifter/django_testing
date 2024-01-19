from django.conf import settings
import pytest


@pytest.mark.django_db
def test_news_order(all_news, client, home_url):
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_news_count(all_news, client, home_url):
    response = client.get(home_url)
    news_count = len(response.context['object_list'])
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_comments_order(
    client,
    some_comments_under_news,
    news,
    news_detail_url,
):
    response = client.get(news_detail_url)
    assert 'news' in response.context
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
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
    news_detail_url
):
    response = parametrized_client.get(news_detail_url)
    assert ('form' in response.context) is comment_form_access_status
