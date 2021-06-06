# Generated by Django 3.1.7 on 2021-06-06 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('euro2020', '0016_auto_20210605_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(choices=[('G1', 'GroepsRonde 1'), ('G2', 'GroepsRonde 2'), ('G3', 'GroepsRonde 3'), ('Q6', 'Achtste Finales'), ('Q8', 'Kwart Finales'), ('Q4', 'Halve Finales'), ('Q2', 'Grande Finale')], max_length=2, verbose_name='Stage')),
                ('start', models.DateTimeField(verbose_name='Gestart')),
                ('end', models.DateTimeField(verbose_name='Afgelopen')),
                ('has_started', models.BooleanField(default=False, verbose_name='Gestart')),
                ('has_ended', models.BooleanField(default=False, verbose_name='Afgelopen')),
                ('away', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awayteam_matches', to='euro2020.team')),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hometeam_matches', to='euro2020.team')),
            ],
            options={
                'verbose_name': 'Virtuele Wedstrijd',
                'verbose_name_plural': 'Wedstrijden',
                'ordering': ['start', 'id'],
            },
        ),
    ]