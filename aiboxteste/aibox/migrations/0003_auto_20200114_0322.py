# Generated by Django 3.0.2 on 2020-01-14 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aibox', '0002_auto_20200114_0320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileupload',
            old_name='file',
            new_name='arquivo',
        ),
    ]
