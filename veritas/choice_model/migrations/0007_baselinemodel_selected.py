# Generated by Django 4.0.2 on 2022-05-23 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choice_model', '0006_alter_baselinemodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='baselinemodel',
            name='selected',
            field=models.BooleanField(default=True),
        ),
    ]
