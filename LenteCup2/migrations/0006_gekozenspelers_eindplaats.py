# Generated by Django 3.1.7 on 2021-04-05 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LenteCup2', '0005_speler_land'),
    ]

    operations = [
        migrations.AddField(
            model_name='gekozenspelers',
            name='eindplaats',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]