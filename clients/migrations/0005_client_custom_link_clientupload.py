# Generated by Django 5.1.4 on 2024-12-16 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_client_end_date_alter_client_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='custom_link',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='ClientUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploads', to='clients.client')),
            ],
        ),
    ]
