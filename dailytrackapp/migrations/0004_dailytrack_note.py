# Generated by Django 3.2.7 on 2021-12-18 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dailytrackapp', '0003_auto_20210407_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailytrack',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
