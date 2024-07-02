# Generated by Django 5.0 on 2024-06-27 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_remove_cardinformation_unique_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardinformation',
            name='unique_id',
            field=models.CharField(blank=True, default='', max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='imageposition',
            name='unique_id',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
