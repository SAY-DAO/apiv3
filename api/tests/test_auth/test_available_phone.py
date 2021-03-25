import pytest
from django.urls import reverse
from model_bakery import baker

from users.models import User

pytestmark = pytest.mark.django_db
view_name = 'authentication:available_phone'


def test_available_phone(api_client, faker):
    phone = '+5512398'
    response = api_client().get(
        reverse(view_name, kwargs=dict(handle=phone)),
    )
    assert response.status_code == 200

    user = baker.make(User, phone=phone)

    response = api_client().get(
        reverse(view_name, kwargs=dict(handle=user.phone)),
    )
    assert response.status_code == 400
