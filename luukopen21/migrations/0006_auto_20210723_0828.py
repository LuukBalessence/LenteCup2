# Generated by Django 3.1.7 on 2021-07-23 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luukopen21', '0005_auto_20210722_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='golfprofiel',
            name='buggy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='golfprofiel',
            name='huurset',
            field=models.BooleanField(default=False),
        ),
    ]
