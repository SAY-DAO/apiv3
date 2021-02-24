import pytest
from django.urls import reverse

from authentication import models

pytestmark = pytest.mark.django_db
endpoint = reverse('authentication:otp')


def test_email(api_client):

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


def test_phone(api_client):

    response = api_client().post(
        endpoint,
        data=dict(
            destination='+98123456789',
        )
    )

    assert response.status_code == 200
    assert response.data['is_verified'] is False
    otp_validation: models.OTPValidation = models.OTPValidation.objects.all()[0]
    assert otp_validation.destination == '+98123456789'
    assert otp_validation.is_verified is False


def test_retry(api_client):
    response = api_client().post(
        endpoint,
        data=dict(
            destination='test@test.com',
        )
    )

    assert response.status_code == 200
    assert response.data['send_counter'] == 1

    response = api_client().post(
        endpoint,
        data=dict(
            destination='test@test.com',
        )
    )
    assert response.status_code == 200
    assert response.data['send_counter'] == 2


@pytest.mark.parametrize(
    'destination',
    [
        'test',
        '@test',
        'test@'
        '9812345667',
        '99999999999999999999',
        '99',
    ],
)
def test_wrong_destination(api_client, destination):
    response = api_client().post(
        endpoint,
        data=dict(
            destination=destination,
        )
    )
    assert response.status_code == 400


@pytest.mark.parametrize(
    'destination',
    [
        'test@GmAil.COM',
        't.est@gmail.COM',
        'test+test@gmail.COM',
    ],
)
def test_normalize_email(api_client, destination):
    response = api_client().post(
        endpoint,
        data=dict(
            destination=destination,
        )
    )
    assert response.status_code == 200
    assert response.data['destination'] == 'test@gmail.com'
