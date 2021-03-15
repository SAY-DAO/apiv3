import pytest
from django.urls import reverse

from authentication import models

pytestmark = pytest.mark.django_db
endpoint = reverse('authentication:reset-password')


def test_request_reset_link(api_client):

    response = api_client().post(
        endpoint,
        data=dict(
            destination='test@test.com',
        )
    )

    assert response.status_code == 200
    assert response.data['is_verified'] is False

    otp_validation: models.OTPValidation = models.OTPValidation.objects.all()[0]
    assert otp_validation.destination == 'test@test.com'
    assert otp_validation.is_verified is False
