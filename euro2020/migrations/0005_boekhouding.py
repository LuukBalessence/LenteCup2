# Generated by Django 3.1.7 on 2021-05-20 19:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('euro2020', '0004_league_draw'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boekhouding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boekingsopmerking', models.CharField(max_length=200, verbose_name='boekingsopmerking')),
                ('aantalbetcoins', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(48000)])),
                ('team', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='boekhouding', to='euro2020.team')),
            ],
        ),
    ]
