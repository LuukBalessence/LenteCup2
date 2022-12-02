# Generated by Django 4.1.3 on 2022-11-23 20:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wk2022', '0004_auto_20221005_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='lastscoresave',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 23, 21, 13, 34, 925041), verbose_name='Laatst opgeslagen Scoremake'),
        ),
        migrations.AddField(
            model_name='player',
            name='sitename',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Last name'),
        ),
    ]