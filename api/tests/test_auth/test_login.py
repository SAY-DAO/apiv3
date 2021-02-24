import pytest
from django.urls import reverse
from model_bakery import baker

from users.models import User

pytestmark = pytest.mark.django_db
endpoint = reverse('authentication:login')


def test_login_by_username(api_client, faker):
    raw_password = faker.password()
    user = baker.make(User, password=raw_password)
    user.set_password(raw_password)
    user.save()

    response = api_client().post(
        endpoint,
        data=dict(
            username=user.username,
            password=raw_password,
        )
    )

    assert response.status_code == 200
    assert response.data['access'] is not None
    assert response.data['refresh'] is not None


def test_login_by_username_slugify(api_client, faker):
    raw_password = faker.password()
    user = baker.make(User, password=raw_password)
    user.set_password(raw_password)
    user.save()

    response = api_client().post(
        endpoint,
        data=dict(
            username=user.username.upper(),
            password=raw_password,
        )
    )

    assert response.status_code == 200


def test_login_by_email(api_client, faker):
    raw_password = faker.password()
    user = baker.make(User, email=faker.email(), password=raw_password, is_email_verified=True)
    user.set_password(raw_password)
    user.save()

    response = api_client().post(
        endpoint,
        data=dict(
            username=user.email,
            password=raw_password,
        )
    )

    assert response.status_code == 200


def test_login_by_normalize_email(api_client, faker):
    raw_password = faker.password()
    user = baker.make(User, email=faker.email(), password=raw_password, is_email_verified=True)
    user.set_password(raw_password)
    user.save()

    response = api_client().post(
        endpoint,
        data=dict(
            username=user.email.replace('gmail', 'GmaIL'),
            password=raw_password,
        )
    )

    assert response.status_code == 200


def test_login_by_phone(api_client, faker):
    raw_password = faker.password()
    user = baker.make(User, phone=f'+{faker.msisdn()}', password=raw_password, is_phone_verified=True)
    user.set_password(raw_password)
    user.save()

    response = api_client().post(
        endpoint,
        data=dict(
            username=user.phone,
            password=raw_password,
        )
    )

    assert response.status_code == 200


def test_login_by_unverified_email(api_client, faker):
    raw_password = faker.password()
    user = baker.make(User, email=faker.email(), password=raw_password, is_email_verified=False)
    user.set_password(raw_password)
    user.save()

    response = api_client().post(
        endpoint,
        data=dict(
            username=user.email,
            password=raw_password,
        )
    )

    assert response.status_code == 400


def test_login_by_unverified_phone(api_client, faker):
    raw_password = faker.password()
    user = baker.make(User, phone=f'+{faker.msisdn()}', password=raw_password, is_phone_verified=False)
    user.set_password(raw_password)
    user.save()

    response = api_client().post(
        endpoint,
        data=dict(
            username=user.phone,
            password=raw_password,
        )
    )

    assert response.status_code == 400


def test_login_by_wrong_username(api_client, faker):
    raw_password = faker.password()
    user = baker.make(User, password=raw_password)
    user.set_password(raw_password)
    user.save()

    response = api_client().post(
        endpoint,
        data=dict(
            username=f'wrong-{user.username}',
            password=raw_password,
        )
    )

    assert response.status_code == 400


def test_login_wrong_password(api_client, faker):
    raw_password = faker.password()
    user = baker.make(User, email=faker.email(), password=raw_password)
    user.set_password(raw_password)
    user.save()

    response = api_client().post(
        endpoint,
        data=dict(
            username=user.username,
            password=f'!{raw_password}',
        )
    )

    assert response.status_code == 400
