# Generated by Django 5.0 on 2024-06-27 09:02

import webapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0014_alter_cardinformation_unique_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardinformation',
            name='unique_id',
            field=models.CharField(default=webapp.models.generate_unique_id, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='imageposition',
            name='unique_id',
            field=models.CharField(default=webapp.models.generate_unique_id, max_length=50),
        ),
    ]