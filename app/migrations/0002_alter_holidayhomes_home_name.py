# Generated by Django 4.2 on 2023-04-08 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holidayhomes',
            name='home_name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]