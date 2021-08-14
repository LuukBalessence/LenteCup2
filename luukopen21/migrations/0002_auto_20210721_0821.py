# Generated by Django 3.1.7 on 2021-07-21 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('luukopen21', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaanProfiel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=60)),
                ('plaats', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='GolfBaanProfiel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=60)),
                ('aantalholes', models.PositiveIntegerField(default=9)),
                ('sr', models.DecimalField(blank=True, decimal_places=1, max_digits=3)),
                ('cr', models.DecimalField(blank=True, decimal_places=1, max_digits=3)),
                ('par', models.DecimalField(blank=True, decimal_places=1, max_digits=3)),
                ('baan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='golfbaan', to='luukopen21.baanprofiel')),
            ],
        ),
        migrations.CreateModel(
            name='TeeKleur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kleur', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='golfprofiel',
            name='ziener',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='golfprofiel',
            name='verraders',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Holes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hole_nr', models.PositiveIntegerField()),
                ('par', models.PositiveIntegerField()),
                ('strokeindex', models.PositiveIntegerField()),
                ('afstand', models.PositiveIntegerField(blank=True)),
                ('golfbaan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holes', to='luukopen21.golfbaanprofiel')),
            ],
        ),
        migrations.AddField(
            model_name='golfbaanprofiel',
            name='teekleur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='golfbaan', to='luukopen21.teekleur'),
        ),
    ]