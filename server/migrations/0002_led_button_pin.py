# Generated by Django 5.1.4 on 2025-01-06 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='led',
            name='button_pin',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
