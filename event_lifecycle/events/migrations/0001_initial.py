# Generated manually for offline setup
import uuid

from django.db import migrations, models
import django.core.validators
import events.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('receipt', models.FileField(upload_to='receipts/', validators=[events.validators.validate_receipt])),
                ('transaction_verified', models.BooleanField(default=False)),
                ('attendance', models.BooleanField(default=False)),
                ('feedback_given', models.BooleanField(default=False)),
                ('feedback_text', models.TextField(blank=True)),
                ('rating', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('certificate_hash', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
    ]
