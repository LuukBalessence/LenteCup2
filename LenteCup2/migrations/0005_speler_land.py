# Generated by Django 3.1.7 on 2021-04-05 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LenteCup2', '0004_auto_20210405_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='speler',
            name='land',
            field=models.CharField(default='nederland', max_length=40),
            preserve_default=False,
        ),
    ]
