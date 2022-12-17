# Generated by Django 4.1.3 on 2022-12-17 08:11

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wk2022', '0007_match_matchsitename_alter_league_lastscoresave'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='playerbid',
            field=models.PositiveSmallIntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20000)]),
        ),
        migrations.AlterField(
            model_name='league',
            name='lastscoresave',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 17, 9, 11, 13, 77139), verbose_name='Laatst opgeslagen Scoremake'),
        ),
    ]