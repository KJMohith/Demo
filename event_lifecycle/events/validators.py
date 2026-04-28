from pathlib import Path

from django.core.exceptions import ValidationError

MAX_RECEIPT_SIZE = 2 * 1024 * 1024
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf'}


def validate_receipt(file_obj):
    if file_obj.size >= MAX_RECEIPT_SIZE:
        raise ValidationError('Receipt size must be less than 2MB.')

    extension = Path(file_obj.name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValidationError('Receipt must be a JPG, PNG, or PDF file.')
