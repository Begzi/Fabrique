# Generated by Django 4.1 on 2022-08-25 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0003_alter_timezone_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=12, unique=True, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='timezone',
            name='code',
            field=models.CharField(max_length=100, verbose_name='Часовой пояс'),
        ),
    ]