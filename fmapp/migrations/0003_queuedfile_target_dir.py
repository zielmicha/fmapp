# Generated by Django 2.0.8 on 2018-08-21 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fmapp', '0002_queuedfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='queuedfile',
            name='target_dir',
            field=models.CharField(default='/', max_length=200),
        ),
    ]