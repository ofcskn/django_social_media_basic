# Generated by Django 4.1 on 2022-09-29 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollower',
            name='to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to', to=settings.AUTH_USER_MODEL),
        ),
    ]