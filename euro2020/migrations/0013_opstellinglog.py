# Generated by Django 3.1.7 on 2021-05-23 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('euro2020', '0012_auto_20210523_2156'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpstellingLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tijdopgesteld', models.DateTimeField()),
                ('opgesteldespeler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opstellinglog', to='euro2020.player')),
                ('phase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opstellinglog', to='euro2020.gamephase')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opstellinglog', to='euro2020.team')),
            ],
        ),
    ]
