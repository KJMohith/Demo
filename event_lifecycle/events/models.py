import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_receipt


class Participant(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    transaction_id = models.CharField(max_length=100, unique=True)
    receipt = models.FileField(upload_to='receipts/', validators=[validate_receipt])
    transaction_verified = models.BooleanField(default=False)
    attendance = models.BooleanField(default=False)
    feedback_given = models.BooleanField(default=False)
    feedback_text = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    certificate_hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f'{self.name} ({self.transaction_id})'

    def is_eligible(self):
        return self.transaction_verified and self.attendance and self.feedback_given
