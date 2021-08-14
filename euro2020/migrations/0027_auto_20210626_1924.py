# Generated by Django 3.1.7 on 2021-06-26 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('euro2020', '0026_bids_ontslaan'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='shootout',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='match',
            name='verlenging',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='virtualmatch',
            name='shootout',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='virtualmatch',
            name='verlenging',
            field=models.BooleanField(default=False),
        ),
    ]