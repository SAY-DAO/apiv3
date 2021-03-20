import pytest
from django.urls import reverse
from model_bakery import baker

from authentication.models import ResetPassword
from users.models import User

pytestmark = pytest.mark.django_db
endpoint = reverse('authentication:confirm-reset-password')


def test_confirm_reset_password(api_client, faker):
    user = baker.make(User, email=faker.email())
    reset_password = baker.make(ResetPassword, user=user, token='asdzxc')
    new_password = '123456'

    response = api_client().post(
        endpoint,
        data=dict(
            password=new_password,
            token=reset_password.token,
        )
    )
    assert response.status_code == 200

    user = User.objects.filter(email=user.email).get()
    assert user.check_password(new_password) is True

    # Check against duplicate usage
    response = api_client().post(
        endpoint,
        data=dict(
            password=new_password,
            token=reset_password.token,
        )
    )
    assert response.status_code == 400
