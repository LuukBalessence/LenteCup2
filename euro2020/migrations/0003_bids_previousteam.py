# Generated by Django 3.1.7 on 2021-05-17 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('euro2020', '0002_country_nlname'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='previousteam',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidsprevious', to='euro2020.team'),
        ),
    ]
