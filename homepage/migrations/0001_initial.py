# Generated by Django 5.1.4 on 2024-12-18 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='slide title')),
                ('subtitle', models.CharField(max_length=255, verbose_name='slide subtitle')),
                ('image', models.ImageField(blank=True, null=True, upload_to='slider/', verbose_name='slide image')),
            ],
            options={
                'verbose_name': 'slider',
                'verbose_name_plural': 'sliders',
            },
        ),
    ]
