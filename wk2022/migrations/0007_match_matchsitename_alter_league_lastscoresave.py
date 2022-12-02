# Generated by Django 4.1.3 on 2022-11-23 20:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wk2022', '0006_alter_league_lastscoresave_alter_player_sitename'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='matchsitename',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='matchsite name'),
        ),
        migrations.AlterField(
            model_name='league',
            name='lastscoresave',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 23, 21, 25, 56, 628240), verbose_name='Laatst opgeslagen Scoremake'),
        ),
    ]