# Generated by Django 5.1.4 on 2025-01-15 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_brand_promotion'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='available',
            field=models.CharField(choices=[('available', 'Available'), ('unavailable', 'Unavailable')], default='available', max_length=11, verbose_name='availability'),
        ),
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.TextField(default='', help_text='Write a short description for this product.', verbose_name='short description'),
            preserve_default=False,
        ),
    ]
