# users/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from projects.serializers import CategorySerializer

User = get_user_model()


class AuthorListSerializer(serializers.ModelSerializer):
    specialization = CategorySerializer(many=True, read_only=True)
    project_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
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
        model = User
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
        model = User
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
        read_only_fields = ["id", "email", "username"]


class CustomRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ("email", "password", "password2")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
            }
        }

    def validate(self, attrs):
        if attrs.get("password") != attrs.pop("password2", None):
            raise serializers.ValidationError(
                {"password": "Паролі не співпадають."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
