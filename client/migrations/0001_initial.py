# Generated by Django 4.1 on 2022-08-25 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimeZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, verbose_name='Часовой пояс')),
                ('tag', models.CharField(max_length=100, verbose_name='Обозначение')),
                ('title', models.CharField(max_length=100, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Часовой пояс',
                'verbose_name_plural': 'Часовой пояса',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=12, unique=True, verbose_name='Номер телефона')),
                ('code', models.CharField(max_length=5, verbose_name='Код мобильного оператора')),
                ('tag', models.CharField(max_length=100, verbose_name='Тэг')),
                ('time_zone', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients', to='client.timezone')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
    ]
