import pytest
from django.conf import settings

from .constants import HOMEPAGE_URL, NEWS_DETAIL
from .functions import get_url


@pytest.mark.usefixtures('bunch_of_news')
@pytest.mark.django_db
def test_num_of_news_on_main(client):
    response = client.get(HOMEPAGE_URL)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.usefixtures('bunch_of_news')
@pytest.mark.django_db
def test_order_of_news(client):
    response = client.get(HOMEPAGE_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.usefixtures('bunch_of_comments')
def test_oder_of_comments(client, news_object):
    response = client.get(get_url(NEWS_DETAIL, news_object.pk))
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps, reverse=True)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user, is_there_form',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('author_client'), True)
    )
)
def test_comment_form_for_different_users(user, is_there_form, news_object):
    response = user.get(get_url(NEWS_DETAIL, news_object.pk))
    assert ('form' in response.context) == is_there_form
