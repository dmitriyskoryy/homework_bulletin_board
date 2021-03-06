# Generated by Django 4.0.3 on 2022-05-09 15:04

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_alter_adt_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(height_field=100, upload_to='photo/%Y/%m/%d/', verbose_name='Фото', width_field=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='adt',
            name='photo',
        ),
        migrations.AlterField(
            model_name='adt',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Контент'),
        ),
        migrations.AlterField(
            model_name='adt',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Заголовок объявления'),
        ),
    ]
