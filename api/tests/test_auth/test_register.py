import pytest
from django.urls import reverse
from model_bakery import baker

from authentication.models import OTPValidation
from users.models import User

pytestmark = pytest.mark.django_db
endpoint = reverse('authentication:register-list')


def test_register(api_client, faker):
    otp_validation = baker.make(OTPValidation, destination=faker.email(), is_verified=True)

    response = api_client().post(
        endpoint,
        data=dict(
            username=faker.user_name(),
            password=faker.password(),
            email=otp_validation.destination,
        )
    )

    assert response.status_code == 201


def test_register_unverified_email(api_client, faker):
    otp_validation = baker.make(OTPValidation, destination=faker.email(), is_verified=False)

    response = api_client().post(
        endpoint,
        data=dict(
            username=faker.user_name(),
            password=faker.password(),
            email=otp_validation.destination,
        )
    )

    assert response.status_code == 400

    response = api_client().post(
        endpoint,
        data=dict(
            username=faker.user_name(),
            password=faker.password(),
            email=faker.email(),
        )
    )

    assert response.status_code == 400


def test_register_unverified_phone(api_client, faker):
    otp_validation = baker.make(OTPValidation, destination=f'+{faker.msisdn()}', is_verified=False)

    response = api_client().post(
        endpoint,
        data=dict(
            username=faker.user_name(),
            password=faker.password(),
            phone=otp_validation.destination,
        )
    )

    assert response.status_code == 400

    response = api_client().post(
        endpoint,
        data=dict(
            username=faker.user_name(),
            password=faker.password(),
            phone=f'+{faker.msisdn()}',
        )
    )

    assert response.status_code == 400


def test_register_without_phone_and_email(api_client, faker):
    response = api_client().post(
        endpoint,
        data=dict(
            username=faker.user_name(),
            password=faker.password(),
        )
    )
    assert response.status_code == 400


def test_register_email_exists(api_client, faker):
    otp_validation = baker.make(OTPValidation, destination=faker.email(), is_verified=True)
    user = baker.make(User, email=otp_validation.destination)

    # Try to register with same email and different username
    response = api_client().post(
        endpoint,
        data=dict(
            username=faker.user_name(),
            password=faker.password(),
            email=otp_validation.destination,
        )
    )
    assert response.status_code == 400


def test_register_phone_exists(api_client, faker):
    otp_validation = baker.make(OTPValidation, destination=f'+{faker.msisdn()}', is_verified=True)
    user = baker.make(User, phone=otp_validation.destination)

    # Try to register with same phone and different username
    response = api_client().post(
        endpoint,
        data=dict(
            username=faker.user_name(),
            password=faker.password(),
            phone=otp_validation.destination,
        )
    )
    assert response.status_code == 400


def test_register_username_exists(api_client, faker):
    otp_validation = baker.make(OTPValidation, destination=faker.email(), is_verified=True)
    user = baker.make(User)

    response = api_client().post(
        endpoint,
        data=dict(
            username=user.username,
            password=faker.password(),
            email=otp_validation.destination,
        )
    )
    assert response.status_code == 400

