import pytest
from django.urls import reverse
from model_bakery import baker

from users.models import User

pytestmark = pytest.mark.django_db
endpoint = reverse('authentication:reset-password')


def test_reset_password(api_client, faker):
    user = baker.make(User, email=faker.email())

    response = api_client().post(
        endpoint,
        data=dict(
            destination=user.email,
        )
    )

    assert response.status_code == 200
