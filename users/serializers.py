from rest_framework import serializers
from .models import CustomUser
from projects.serializers import CategorySerializer


class AuthorListSerializer(serializers.ModelSerializer):
    specialization = CategorySerializer(many=True, read_only=True)
    project_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "display_name",
            "avatar",
            "city",
            "specialization",
            "project_count",
        ]


class AuthorDetailSerializer(serializers.ModelSerializer):
    specialization = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "display_name",
            "avatar",
            "bio",
            "city",
            "specialization",
            "phone_number",
            "telegram_url",
            "instagram_url",
            "facebook_url",
            "date_joined",
        ]


class CurrentUserSerializer(serializers.ModelSerializer):
    specialization = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "avatar",
            "bio",
            "city",
            "specialization",
            "phone_number",
            "telegram_url",
            "instagram_url",
            "facebook_url",
        ]
        read_only_fields = ["id", "username", "email"]
