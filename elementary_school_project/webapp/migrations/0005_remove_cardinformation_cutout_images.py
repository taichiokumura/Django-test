# Generated by Django 5.0 on 2024-05-22 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_cardinformation_living_thing_consideration_images_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardinformation',
            name='cutout_images',
        ),
    ]
