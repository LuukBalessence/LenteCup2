# Generated by Django 3.1.7 on 2021-05-17 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('euro2020', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='nlname',
            field=models.CharField(default='', max_length=30, verbose_name='NL naam'),
        ),
    ]
