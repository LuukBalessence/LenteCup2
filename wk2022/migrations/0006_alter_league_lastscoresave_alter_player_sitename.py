# Generated by Django 4.1.3 on 2022-11-23 20:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wk2022', '0005_league_lastscoresave_player_sitename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='lastscoresave',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 23, 21, 15, 5, 688782), verbose_name='Laatst opgeslagen Scoremake'),
        ),
        migrations.AlterField(
            model_name='player',
            name='sitename',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='website name'),
        ),
    ]
