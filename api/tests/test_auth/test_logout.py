import pytest
from django.conf import settings
from django.urls import reverse
from model_bakery import baker

from authentication.utils import get_tokens_for_user
from users.models import User

pytestmark = pytest.mark.django_db
endpoint = reverse('authentication:logout')


def test_logout(api_client, faker):
    user = baker.make(User)
    tokens = get_tokens_for_user(user)
    HTTP_HEADERS = {
        settings.AUTH_HEADER_NAME: tokens['access'],
    }

    response = api_client().post(
        endpoint,
        **HTTP_HEADERS,
    )
    assert response.status_code == 200

    # making a private call using blacklisted token
    response = api_client().post(
        endpoint,
        **HTTP_HEADERS,
    )
    assert response.status_code == 401
