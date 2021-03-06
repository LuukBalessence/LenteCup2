# Generated by Django 3.1.7 on 2021-04-02 20:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.CharField(max_length=21)),
                ('weeknummer', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(53)])),
                ('maxpoints', models.PositiveSmallIntegerField(default=4)),
                ('openforscoring', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Scores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(40)])),
                ('qualifying', models.BooleanField(null=True)),
                ('baan', models.CharField(blank=True, max_length=40)),
                ('lus', models.CharField(blank=True, max_length=40)),
                ('finalscore', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='scores', to=settings.AUTH_USER_MODEL)),
                ('week', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='LenteCup2.week')),
            ],
        ),
    ]
