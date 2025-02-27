from django.urls import reverse

HOMEPAGE = 'news:home'
COMMENT_EDIT = 'news:edit'
COMMENT_DELETE = 'news:delete'
AUTHOR_COMMENT = 'Author typed some text'
HOMEPAGE_URL = reverse(HOMEPAGE)
NEWS_DETAIL = 'news:detail'
USERS_LOGIN = 'users:login'
USERS_LOGOUT = 'users:logout'
USERS_SIGNUP = 'users:signup'