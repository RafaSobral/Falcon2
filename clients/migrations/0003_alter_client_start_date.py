# Generated by Django 5.1.4 on 2024-12-16 17:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_alter_client_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
