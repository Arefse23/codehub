# Generated by Django 4.1.7 on 2023-03-19 07:16

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_category_icon_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]