# Generated by Django 4.1 on 2022-08-25 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0005_remove_message_client_remove_message_notice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='filters',
            field=models.ManyToManyField(to='notice.filter'),
        ),
        migrations.DeleteModel(
            name='Notice_Filter',
        ),
    ]