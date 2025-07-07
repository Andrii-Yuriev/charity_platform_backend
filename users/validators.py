from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_image_size(file):
    """
    Validate the size of the uploaded image file.
    Raises ValidationError if the file size exceeds 2 MB.
    """
    max_size_mb = 2
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(
            _(f"Розмір файлу не може перевищувати {max_size_mb} МБ."),
        )


def validate_image_extension(file):
    """
    Validate the file extension of the uploaded image.
    Raises ValidationError if the file is not a valid image type.
    """
    valid_extensions = [
        "jpg",
        "jpeg",
        "png",
    ]
    extension = file.name.split(".")[-1].lower()
    if extension not in valid_extensions:
        raise ValidationError(
            _("Неприпустимий формат файлу. Дозволені формати: jpg, jpeg, png.")
        )
