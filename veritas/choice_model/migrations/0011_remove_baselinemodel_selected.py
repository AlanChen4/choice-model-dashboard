# Generated by Django 4.0.2 on 2022-06-15 01:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('choice_model', '0010_rename_bundle_id_modifiedsitesbundle_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baselinemodel',
            name='selected',
        ),
    ]
