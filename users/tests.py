import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
import os


@pytest.fixture
def create_user(
    db,
):
    def user_factory(**kwargs):
        return User.objects.create_user(**kwargs)

    return user_factory


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def registration_data():
    return {
        "email": "test@example.com",
        "password": "some_strong_password_123",
        "password2": "some_strong_password_123",
    }


@pytest.mark.django_db
def test_successful_registration(api_client, registration_data):
    response = api_client.post(
        "/api/v1/auth/registration/", registration_data, format="json"
    )

    assert response.status_code == 201
    assert User.objects.count() == 1

    new_user = User.objects.first()
    assert new_user.email == registration_data["email"]

    response_data = response.json()
    assert "access" in response_data
    assert "refresh" in response_data


@pytest.mark.django_db
def test_registration_passwords_mismatch(api_client):
    data = {
        "email": "test@example.com",
        "password": "password123",
        "password2": "password456",
    }

    response = api_client.post(
        "/api/v1/auth/registration/", data, format="json"
    )

    assert response.status_code == 400
    assert User.objects.count() == 0
    assert "password" in response.json()


@pytest.mark.django_db
def test_registration_duplicate_email(api_client, registration_data):
    User.objects.create_user(
        email=registration_data["email"], password=registration_data["password"]
    )

    assert User.objects.count() == 1

    response = api_client.post(
        "/api/v1/auth/registration/", registration_data, format="json"
    )

    assert response.status_code == 400
    assert User.objects.count() == 1
    assert "email" in response.json()


@pytest.mark.django_db
def test_avatar_upload_authenticated_user(api_client, create_user):

    user = create_user(email="user@test.com", password="password123")
    api_client.force_authenticate(user=user)

    avatar_content = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
    avatar = SimpleUploadedFile(
        "test_avatar.jpg", avatar_content, content_type="image/jpg"
    )

    response = api_client.put(
        "/api/v1/auth/user/avatar/", {"avatar": avatar}, format="multipart"
    )

    assert response.status_code == 200

    user.refresh_from_db()
    assert user.avatar is not None
    assert user.avatar.name.endswith(".webp")


@pytest.mark.django_db
def test_avatar_upload_unauthenticated_user(api_client):
    avatar_content = b"test content"
    avatar = SimpleUploadedFile("test.txt", avatar_content)

    response = api_client.put(
        "/api/v1/auth/user/avatar/", {"avatar": avatar}, format="multipart"
    )

    assert response.status_code == 401
