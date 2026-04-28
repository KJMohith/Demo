import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_photo, validate_receipt


class Event(models.Model):
    title = models.CharField(max_length=150)
    event_date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event_date', 'title']

    def __str__(self):
        return self.title


class Participant(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    transaction_id = models.CharField(max_length=100, unique=True)
    receipt = models.FileField(upload_to='receipts/', validators=[validate_receipt])
    photo = models.ImageField(upload_to='receipts/', validators=[validate_photo])
    transaction_photo_data = models.BinaryField(blank=True, null=True, editable=False)
    transaction_verified = models.BooleanField(default=True)
    attendance = models.BooleanField(default=False)
    feedback_given = models.BooleanField(default=False)
    feedback_text = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    certificate_hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.transaction_id})'

    def save(self, *args, **kwargs):
        if self.photo and hasattr(self.photo, 'read'):
            self.photo.seek(0)
            self.transaction_photo_data = self.photo.read()
            self.photo.seek(0)
        super().save(*args, **kwargs)

    def is_eligible(self):
        return self.attendance and self.feedback_given
