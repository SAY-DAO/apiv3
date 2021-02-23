from django.urls import reverse
import pytest
from authentication import models
from authentication.utils import generate_otp

pytestmark = pytest.mark.django_db
endpoint = reverse('authentication:verify_otp')


def test_verify_otp(api_client):
    email = 'test@test.com'

    otp_response = api_client().post(
        reverse('authentication:otp'),
        data=dict(
            destination=email,
        )
    )

    assert otp_response.status_code == 200

    otp_validation: models.OTPValidation = models.OTPValidation.objects.all()[0]

    response = api_client().post(
        endpoint,
        data=dict(
            destination=email,
            otp=generate_otp(otp_validation.secret),
        )
    )
    assert response.status_code == 200
    assert response.data['is_verified'] is True


def test_verify_wrong_otp(api_client):
    email = 'test@test.com'

    otp_response = api_client().post(
        reverse('authentication:otp'),
        data=dict(
            destination=email,
        )
    )

    assert otp_response.status_code == 200

    response = api_client().post(
        endpoint,
        data=dict(
            destination=email,
            otp=-1,
        )
    )
    assert response.status_code == 400

    otp_validation: models.OTPValidation = models.OTPValidation.objects.all()[0]
    assert otp_validation.is_verified is False
