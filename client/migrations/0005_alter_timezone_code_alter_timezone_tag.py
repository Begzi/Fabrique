# Generated by Django 4.1 on 2022-08-25 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_alter_timezone_code_alter_timezone_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timezone',
            name='code',
            field=models.CharField(max_length=10, verbose_name='Часовой пояс'),
        ),
        migrations.AlterField(
            model_name='timezone',
            name='tag',
            field=models.CharField(max_length=5, verbose_name='Обозначение'),
        ),
    ]