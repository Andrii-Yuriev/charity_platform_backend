from rest_framework import serializers
from .models import Category, Project, ProjectImage
from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar", "display_name"]


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ["id", "image", "order"]


class ProjectListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "subtitle",
            "author",
            "category",
            "donation_type",
            "cover_image",
            "status",
            "end_date",
        ]

    def get_cover_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            request = self.context.get("request")
            return (
                request.build_absolute_uri(first_image.image.url)
                if request
                else first_image.image.url
            )
        return None


class ProjectDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "subtitle",
            "author",
            "category",
            "images",
            "description",
            "fundraising_goal",
            "target_amount",
            "donation_type",
            "price",
            "donation_percentage",
            "monobank_jar_url",
            "privatbank_konvert_url",
            "paypal_me_url",
            "other_payment_details",
            "status",
            "created_at",
            "end_date",
            "views_count",
        ]
