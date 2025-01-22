# Generated by Django 5.1.4 on 2025-01-04 05:45

import django.db.models.deletion
import mptt.fields
import taggit.managers
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='brand name')),
                ('slug', models.SlugField(help_text='English letters and numbers only. Replace space with "-".', max_length=100, unique=True, verbose_name='brand slug')),
            ],
            options={
                'verbose_name': 'brand',
                'verbose_name_plural': 'brands',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='category name')),
                ('slug', models.SlugField(help_text='English letters and numbers only. Replace space with "-".', max_length=100, unique=True, verbose_name='category slug')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, help_text='Optional. Select a parent category if this category is a subcategory.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.category', verbose_name='parent category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='product name')),
                ('slug', models.SlugField(help_text='English letters and numbers only. Replace space with "-".', max_length=255, unique=True, verbose_name='product slug')),
                ('image', models.ImageField(blank=True, help_text='Upload a product image.', null=True, upload_to='products/', verbose_name='product image')),
                ('description', tinymce.models.HTMLField(help_text='Write a description for this product.', verbose_name='product description')),
                ('price', models.IntegerField(help_text='Enter the price of this product in Tomans.', verbose_name='product price')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.brand', verbose_name='product brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category', verbose_name='product category')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='product tags')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='e.g. Length, Weight, Color, etc.', max_length=255, verbose_name='specification title')),
                ('value', models.CharField(help_text='e.g. 10 cm, 20 kg, Red, etc.', max_length=255, verbose_name='specification value')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='products.product')),
            ],
            options={
                'verbose_name': 'specification',
                'verbose_name_plural': 'specifications',
            },
        ),
    ]