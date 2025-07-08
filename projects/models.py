from django.db import models
from django.conf import settings
from core.validators import validate_image_size, validate_image_extension


class Category(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Назва категорії"
    )
    slug = models.SlugField(
        max_length=100, unique=True, verbose_name="Слаг категорії"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["name"]


class Project(models.Model):
    class Status(models.TextChoices):
        MODERATION = "moderation", "На модерації"
        ACTIVE = "active", "Активний"
        ARCHIVED = "archived", "Архівний"
        DRAFT = "draft", "Чернетка"

    class DonationType(models.TextChoices):
        FULL_PRICE = "full_price", "100% з продажу"
        PERCENTAGE = "percentage", "Відсоток від продажу"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name="Автор",
    )
    title = models.CharField(max_length=255, verbose_name="Назва проєкту")
    subtitle = models.CharField(
        max_length=255, blank=True, verbose_name="Короткий опис"
    )
    description = models.TextField(verbose_name="Повний опис проєкту")
    fundraising_goal = models.TextField(
        verbose_name="Мета збору",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects",
        verbose_name="Категорія",
    )

    target_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Цільова сума, грн",
    )
    donation_type = models.CharField(
        max_length=20,
        choices=DonationType.choices,
        verbose_name="Тип збору",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Вкажіть, якщо тип збору '100% з продажу'",
        verbose_name="Ціна товару",
    )
    donation_percentage = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Вкажіть, якщо тип збору '% від продажів'",
        verbose_name="Відсоток на донат",
    )

    monobank_jar_url = models.URLField(
        max_length=255, blank=True, verbose_name="Посилання на МоноБанку"
    )
    privatbank_konvert_url = models.URLField(
        max_length=255,
        blank=True,
        verbose_name="Посилання на Конверт Приватбанку",
    )
    paypal_me_url = models.URLField(
        max_length=255, blank=True, verbose_name="Посилання на PayPal.Me"
    )
    other_payment_details = models.TextField(
        blank=True, verbose_name="Інші реквізити"
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.MODERATION,
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата створення"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата оновлення"
    )
    end_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата завершення збору"
    )
    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Кількість переглядів"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Проєкт"
        verbose_name_plural = "Проєкти"
        ordering = ["-created_at"]


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Проєкт",
    )
    image = models.ImageField(
        upload_to="project_gallery/",
        validators=[validate_image_size, validate_image_extension],
        verbose_name="Зображення",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self):
        return f"Зображення для {self.project.title}"

    class Meta:
        verbose_name = "Зображення проєкту"
        verbose_name_plural = "Зображення проєктів"
        ordering = ["order"]
