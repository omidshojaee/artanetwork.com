# Generated by Django 5.1.4 on 2025-01-13 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='subject',
            field=models.CharField(default='', max_length=100, verbose_name='contact subject'),
            preserve_default=False,
        ),
    ]
