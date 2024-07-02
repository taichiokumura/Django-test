# Generated by Django 5.0 on 2024-06-27 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_cardinformation_unique_id_imageposition_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardinformation',
            name='unique_id',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='imageposition',
            name='unique_id',
            field=models.CharField(max_length=50),
        ),
    ]