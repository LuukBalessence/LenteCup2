# Generated by Django 3.1.7 on 2021-05-22 20:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('euro2020', '0008_opstelling'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='eliminated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='team',
            name='order',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Order'),
        ),
    ]
