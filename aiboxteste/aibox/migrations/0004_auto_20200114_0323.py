# Generated by Django 3.0.2 on 2020-01-14 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aibox', '0003_auto_20200114_0322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileupload',
            old_name='classifier',
            new_name='classificador',
        ),
    ]