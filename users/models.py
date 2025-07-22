from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.validators import validate_image_size, validate_image_extension
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, Transpose


class CustomUserManager(BaseUserManager):
    """
    Custom user model with unique email
    identificator for authentification instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Email is required"))
        email = self.normalize_email(email)

        username = extra_fields.pop("username", None)

        if not username:
            username = email.split("@")[0]
            counter = 1
            temp_username = username
            while self.model.objects.filter(username=username).exists():
                temp_username = f"{username}{counter}"
                counter += 1
            username = temp_username

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(_("Email address"), unique=True)
    username = models.CharField(
        _("Username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        blank=True,
    )

    bio = models.TextField(blank=True, verbose_name="Про себе")
    avatar = ProcessedImageField(
        upload_to="avatars/",
        processors=[Transpose(), ResizeToFill(400, 400)],
        format="WEBP",
        options={"quality": 85},
        null=True,
        blank=True,
        verbose_name="Аватар",
        validators=[
            validate_image_size,
            validate_image_extension,
        ],
    )
    city = models.CharField(max_length=100, blank=True, verbose_name="Місто")
    specialization = models.ManyToManyField(
        "projects.Category",
        blank=True,
        related_name="specialists",
        verbose_name="Спеціалізація",
    )
    phone_number = models.CharField(
        max_length=20, blank=True, verbose_name="Номер телефону"
    )
    telegram_url = models.URLField(
        max_length=200, blank=True, verbose_name="Telegram"
    )
    instagram_url = models.URLField(
        max_length=200, blank=True, verbose_name="Instagram"
    )
    facebook_url = models.URLField(
        max_length=200, blank=True, verbose_name="Facebook"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.get_username()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Автори"
