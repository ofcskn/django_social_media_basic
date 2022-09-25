# Generated by Django 4.1 on 2022-09-25 09:59

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_image_rename_function'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(blank=True, upload_to=core.models.PathAndRename('posts/')),
        ),
    ]
