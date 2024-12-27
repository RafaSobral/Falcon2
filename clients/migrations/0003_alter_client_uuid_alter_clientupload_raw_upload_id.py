# Generated by Django 5.1.4 on 2024-12-27 14:24

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_alter_client_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='clientupload',
            name='raw_upload_id',
            field=models.CharField(editable=False, max_length=18, null=True),
        ),
    ]