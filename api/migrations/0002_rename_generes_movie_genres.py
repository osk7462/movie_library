# Generated by Django 3.2 on 2021-05-03 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='generes',
            new_name='genres',
        ),
    ]
