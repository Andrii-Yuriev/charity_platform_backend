import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Project, Category

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def user_factory(**kwargs):
        return User.objects.create_user(**kwargs)

    return user_factory


@pytest.fixture
def create_category(db):
    return Category.objects.create(name="Test Category", slug="test-category")


@pytest.fixture
def create_project(db, create_user, create_category):
    user = create_user(email="author@test.com", password="password123")
    return Project.objects.create(
        author=user,
        category=create_category,
        title="Test Project",
        description="Test Description",
        fundraising_goal="Test Goal",
        donation_type="full_price",
        price="100.00",
    )


@pytest.mark.django_db
def test_project_update_by_owner(api_client, create_project):
    project = create_project
    owner = project.author
    api_client.force_authenticate(user=owner)

    updated_data = {"title": "Updated Title"}
    response = api_client.patch(
        f"/api/v1/projects/{project.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    project.refresh_from_db()
    assert project.title == "Updated Title"


@pytest.mark.django_db
def test_project_update_by_another_user_forbidden(
    api_client, create_project, create_user
):
    project = create_project
    another_user = create_user(email="another@test.com", password="password123")
    api_client.force_authenticate(user=another_user)

    updated_data = {"title": "Forbidden Update"}
    response = api_client.patch(
        f"/api/v1/projects/{project.id}/", updated_data, format="json"
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_project_delete_by_owner(api_client, create_project):
    project = create_project
    owner = project.author
    api_client.force_authenticate(user=owner)

    response = api_client.delete(f"/api/v1/projects/{project.id}/")

    assert response.status_code == 204
    assert not Project.objects.filter(id=project.id).exists()


@pytest.mark.django_db
def test_project_delete_by_another_user_forbidden(
    api_client, create_project, create_user
):
    project = create_project
    another_user = create_user(email="another@test.com", password="password123")
    api_client.force_authenticate(user=another_user)

    response = api_client.delete(f"/api/v1/projects/{project.id}/")

    assert response.status_code == 403
    assert Project.objects.filter(id=project.id).exists()


@pytest.mark.django_db
def test_upload_image_to_project_by_owner(api_client, create_project):
    project = create_project
    owner = project.author
    api_client.force_authenticate(user=owner)

    image_content = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
    image = SimpleUploadedFile(
        "test_image.jpeg", image_content, content_type="image/jpeg"
    )

    response = api_client.post(
        f"/api/v1/projects/{project.id}/upload-image/",
        {"image": image},
        format="multipart",
    )

    assert response.status_code == 201
    project.refresh_from_db()
    assert project.images.count() == 1
    assert project.images.first().image.name.endswith(".webp")
