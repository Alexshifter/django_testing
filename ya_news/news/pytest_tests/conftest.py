from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор комментария')


@pytest.fixture
def author_client(author):
    auth_client = Client()
    auth_client.force_login(author)
    return auth_client


@pytest.fixture
def news():
    news = News.objects.create(title='Заголовок', text='Текст')
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )
    return comment


@pytest.fixture
def all_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index),
        ) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def some_comments_under_news(author, news):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def users_login_url():
    return reverse('users:login')


@pytest.fixture
def users_logout_url():
    return reverse('users:logout')


@pytest.fixture
def users_signup_url():
    return reverse('users:signup')


@pytest.fixture
def comment_delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def comment_edit_url(comment):
    return reverse('news:edit', args=(comment.id,))
