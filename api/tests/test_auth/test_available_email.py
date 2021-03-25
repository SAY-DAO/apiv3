import pytest
from django.urls import reverse
from model_bakery import baker

from users.models import User

pytestmark = pytest.mark.django_db
view_name = 'authentication:available_email'


def test_available_email(api_client, faker):
    email = faker.email()

    response = api_client().get(
        reverse(view_name, kwargs=dict(handle=email)),
    )
    assert response.status_code == 200

    user = baker.make(User, email=email)

    response = api_client().get(
        reverse(view_name, kwargs=dict(handle=user.email)),
    )
    assert response.status_code == 400
