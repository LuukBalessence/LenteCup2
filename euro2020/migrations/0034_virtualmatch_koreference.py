# Generated by Django 3.1.7 on 2021-07-06 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('euro2020', '0033_match_koreference'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualmatch',
            name='koreference',
            field=models.CharField(default='', max_length=4),
        ),
    ]
