# Generated by Django 5.0.2 on 2024-02-24 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StyleSculptapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='detail',
            field=models.CharField(default=0, max_length=300),
            preserve_default=False,
        ),
    ]