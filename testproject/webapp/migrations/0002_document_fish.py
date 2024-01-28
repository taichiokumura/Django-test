# Generated by Django 5.0 on 2024-01-28 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='fish',
            field=models.CharField(blank=True, choices=[('1', 'メダカ'), ('2', 'キンブナ'), ('3', 'シマドジョウ'), ('4', 'タイリクバラタナゴ')], max_length=50, verbose_name='種類名'),
        ),
    ]
