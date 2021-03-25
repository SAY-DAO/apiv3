import pytest
from django.urls import reverse
from model_bakery import baker

from users.models import User

pytestmark = pytest.mark.django_db
view_name = 'authentication:available_username'


def test_available_username(api_client, faker):
    username = 'abcd'

    response = api_client().get(
        reverse(view_name, kwargs=dict(handle=username)),
    )
    assert response.status_code == 200

    user = baker.make(User, username=username)

    response = api_client().get(
        reverse(view_name, kwargs=dict(handle=user.username)),
    )
    assert response.status_code == 400
