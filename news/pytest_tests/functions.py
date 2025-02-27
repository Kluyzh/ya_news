from django.urls import reverse


def get_url(page, page_var):
    return reverse(page, args=(page_var,))
