# Generated by Django 3.1.7 on 2021-06-28 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('euro2020', '0030_virtualmatch_homewonshootout'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='readurl',
            field=models.URLField(blank=True, max_length=300),
        ),
    ]