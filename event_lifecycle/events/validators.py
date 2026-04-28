from pathlib import Path

from django.core.exceptions import ValidationError

MAX_RECEIPT_SIZE = 2 * 1024 * 1024
RECEIPT_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf'}
PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png'}


def _validate_size(file_obj):
    if file_obj.size >= MAX_RECEIPT_SIZE:
        raise ValidationError('File size must be less than 2MB.')


def validate_receipt(file_obj):
    _validate_size(file_obj)
    extension = Path(file_obj.name).suffix.lower()
    if extension not in RECEIPT_EXTENSIONS:
        raise ValidationError('Receipt must be a JPG, PNG, or PDF file.')


def validate_photo(file_obj):
    _validate_size(file_obj)
    extension = Path(file_obj.name).suffix.lower()
    if extension not in PHOTO_EXTENSIONS:
        raise ValidationError('Photo must be a JPG or PNG file.')
