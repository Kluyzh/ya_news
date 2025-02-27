from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client

from news.models import Comment, News

from .constants import AUTHOR_COMMENT


@pytest.fixture
def author(django_user_model):  
    return django_user_model.objects.create(username='author')


@pytest.fixture
def not_author(django_user_model):  
    return django_user_model.objects.create(username='not_author')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news_object():
    news = News.objects.create(
        title='Weather forecast',
        text='Today is a good day'
    )
    return news


@pytest.fixture
def comment_of_author(author, news_object):
    comment = Comment.objects.create(
        news=news_object,
        text=AUTHOR_COMMENT,
        author=author
    )
    return comment


@pytest.mark.django_db
@pytest.fixture
def bunch_of_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'News number {index}',
            text=f'Text of news number {index}',
            date=today - timedelta(days=index)
        ) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.mark.django_db
@pytest.fixture
def bunch_of_comments(author, news_object):
    today = datetime.today()
    all_comments = [
        Comment(
            author=author,
            news=news_object,
            text=f'Comment number {index}',
            created=today - timedelta(days=index)
        ) for index in range(10)
    ]
    Comment.objects.bulk_create(all_comments)


@pytest.fixture
def comment_data_form():
    return {'text': 'New comment'}
