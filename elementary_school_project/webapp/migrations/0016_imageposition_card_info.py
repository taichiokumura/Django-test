# Generated by Django 5.0 on 2024-06-27 10:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0015_alter_cardinformation_unique_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageposition',
            name='card_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.cardinformation'),
        ),
    ]
