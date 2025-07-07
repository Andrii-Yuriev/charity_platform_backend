from django.db import models


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
