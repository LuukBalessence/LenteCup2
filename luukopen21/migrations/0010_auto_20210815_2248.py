# Generated by Django 3.1.7 on 2021-08-15 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luukopen21', '0009_golfprofiel_verradergame'),
    ]

    operations = [
        migrations.AddField(
            model_name='golfprofiel',
            name='immuniteitraad',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='golfprofiel',
            name='immuniteitverraad',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='golfprofiel',
            name='instemronde',
            field=models.BooleanField(default=True),
        ),
    ]
