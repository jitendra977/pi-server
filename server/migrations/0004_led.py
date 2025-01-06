# Generated by Django 5.1.4 on 2025-01-06 00:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_alter_user_email_alter_user_phone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LED',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('gpio', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.user')),
            ],
        ),
    ]