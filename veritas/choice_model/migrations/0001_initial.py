# Generated by Django 4.0.2 on 2022-05-09 22:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('acres', models.FloatField()),
                ('trails', models.IntegerField()),
                ('trail_miles', models.FloatField()),
                ('picnic_area', models.IntegerField()),
                ('sports_facilities', models.IntegerField()),
                ('swimming_facilities', models.IntegerField()),
                ('boat_launch', models.IntegerField()),
                ('waterbody', models.IntegerField()),
                ('bathrooms', models.IntegerField()),
                ('playgrounds', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ModifiedSitesBundle',
            fields=[
                ('bundle_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=100)),
                ('history_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ModifiedSite',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('name', models.CharField(max_length=100)),
                ('acres', models.FloatField()),
                ('trails', models.IntegerField()),
                ('trail_miles', models.FloatField()),
                ('picnic_area', models.IntegerField(choices=[(0, 'No'), (1, 'Yes')])),
                ('sports_facilities', models.IntegerField(choices=[(0, 'No'), (1, 'Yes')])),
                ('swimming_facilities', models.IntegerField(choices=[(0, 'No'), (1, 'Yes')])),
                ('boat_launch', models.IntegerField(choices=[(0, 'No'), (1, 'Yes')])),
                ('waterbody', models.IntegerField(choices=[(0, 'No'), (1, 'Yes')])),
                ('bathrooms', models.IntegerField()),
                ('playgrounds', models.IntegerField(choices=[(0, 'No'), (1, 'Yes')])),
                ('bundle_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='choice_model.modifiedsitesbundle')),
            ],
        ),
    ]
