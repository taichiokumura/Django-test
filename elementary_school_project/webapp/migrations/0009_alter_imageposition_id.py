# Generated by Django 5.0 on 2024-06-27 07:00

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_imageposition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageposition',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
