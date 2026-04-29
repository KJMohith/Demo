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
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='participants', null=True
    )
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
    marks = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    certificate_hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.event} ({self.transaction_id})'

    def save(self, *args, **kwargs):
        # FIX: Only read the photo file when it is a fresh upload (an InMemoryUploadedFile
        # or TemporaryUploadedFile), not on every partial save (e.g. update_fields=['marks']).
        # Previously this ran unconditionally, wasting IO and risking errors on partial saves.
        update_fields = kwargs.get('update_fields')
        photo_is_new_upload = (
            self.photo
            and hasattr(self.photo, 'file')
            and hasattr(self.photo.file, 'read')
            # FieldFile wraps an existing file on disk; InMemoryUploadedFile has content_type
            and hasattr(self.photo, 'content_type')
        )
        if photo_is_new_upload and (update_fields is None or 'photo' in update_fields):
            self.photo.seek(0)
            self.transaction_photo_data = self.photo.read()
            self.photo.seek(0)
        super().save(*args, **kwargs)

    def is_eligible(self):
        """Participant can download a certificate when all three conditions are met."""
        return bool(self.attendance and self.feedback_given and self.marks is not None)