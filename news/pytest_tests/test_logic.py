from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

from .constants import (AUTHOR_COMMENT, COMMENT_DELETE, COMMENT_EDIT,
                        NEWS_DETAIL)
from .functions import get_url


@pytest.mark.django_db
def test_anonymous_cant_comment(
    client, news_object, comment_data_form
):
    client.post(get_url(NEWS_DETAIL, news_object.pk), comment_data_form)
    assert 0 == Comment.objects.count()


@pytest.mark.django_db
def test_auth_user_can_comment(
    author, author_client, news_object, comment_data_form
):
    url = get_url(NEWS_DETAIL, news_object.pk)
    response = author_client.post(url, comment_data_form)
    assert Comment.objects.count() == 1
    assertRedirects(response, f'{url}#comments')
    comment = Comment.objects.get()
    assert comment.author == author
    assert comment.text == comment_data_form['text']


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client, news_object):
    url = get_url(NEWS_DETAIL, news_object.pk)
    bad_words_data = {'text': f'Some text, {BAD_WORDS[0]}, end'}
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_author_can_edit_own_comments(
    author_client, comment_of_author, comment_data_form
):
    edit_url = get_url(COMMENT_EDIT, comment_of_author.pk)
    expected_redirect = (
        get_url(NEWS_DETAIL, comment_of_author.news.pk) + '#comments'
    )
    response = author_client.post(
        edit_url,
        comment_data_form
    )
    assertRedirects(response, expected_redirect)
    comment_of_author.refresh_from_db()
    assert comment_of_author.text == comment_data_form['text']


@pytest.mark.django_db
def test_author_can_delete_own_comment(author_client, comment_of_author):
    expected_redirect = (
        get_url(NEWS_DETAIL, comment_of_author.news.pk) + '#comments'
    )
    response = author_client.post(
        get_url(COMMENT_DELETE, comment_of_author.pk)
    )
    assertRedirects(response, expected_redirect)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_not_author_cant_edit_comments(
    not_author_client, comment_of_author, comment_data_form
):
    edit_url = get_url(COMMENT_EDIT, comment_of_author.pk)
    response = not_author_client.post(
        edit_url,
        comment_data_form
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_of_author.refresh_from_db()
    assert comment_of_author.text == AUTHOR_COMMENT


@pytest.mark.django_db
def test_not_author_cant_delete_comments(not_author_client, comment_of_author):
    response = not_author_client.post(
        reverse(COMMENT_DELETE, args=(comment_of_author.pk,))
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
