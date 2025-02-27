from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from .constants import (COMMENT_DELETE, COMMENT_EDIT, HOMEPAGE, NEWS_DETAIL,
                        USERS_LOGIN, USERS_LOGOUT, USERS_SIGNUP)
from .functions import get_url


@pytest.mark.django_db
@pytest.mark.parametrize(
    'page, arg',
    (
        (HOMEPAGE, False),
        (NEWS_DETAIL, True),
        (USERS_LOGIN, False),
        (USERS_LOGOUT, False),
        (USERS_SIGNUP, False)
    )
)
def test_page_availability_for_anonymous_user(client, page, arg, news_object):
    if arg:
        url = get_url(page, news_object.pk)
    else:
        url = reverse(page)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'page',
    (COMMENT_EDIT, COMMENT_DELETE)
)
def test_page_availability_for_author_of_the_comment(
    author_client, comment_of_author, page
):
    response = author_client.get(get_url(page, comment_of_author.pk))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'page',
    (COMMENT_EDIT, COMMENT_DELETE)
)
def test_redirection_of_anonymous(page, client, comment_of_author):
    url = get_url(page, comment_of_author.pk)
    response = client.get(url)
    login_url = reverse(USERS_LOGIN)
    expected_redirect = f'{login_url}?next={url}'
    assertRedirects(response, expected_redirect)


@pytest.mark.parametrize(
    'page',
    (COMMENT_EDIT, COMMENT_DELETE)
)
def test_not_author_cant_edit_and_delete_comment(
    not_author_client, comment_of_author, page
):
    response = not_author_client.get(get_url(page, comment_of_author.pk))
    assert response.status_code == HTTPStatus.NOT_FOUND
