# Generated by Django 5.0 on 2024-02-14 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CardInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(default='SOME STRING', upload_to='result_images/')),
                ('cutout_images', models.ImageField(default='SOME STRING', upload_to='result_images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('fish', models.CharField(blank=True, choices=[('1', 'メダカ'), ('2', 'キンブナ'), ('3', 'シマドジョウ'), ('4', 'タイリクバラタナゴ')], max_length=50, verbose_name='種類名')),
                ('explanation', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]