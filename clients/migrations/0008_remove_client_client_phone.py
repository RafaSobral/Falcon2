# Generated by Django 5.1.4 on 2024-12-20 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_client_drive_folder_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='client_phone',
        ),
    ]