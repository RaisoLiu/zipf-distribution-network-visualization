# Generated by Django 3.1.1 on 2020-09-27 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djsite', '0004_data_in_addr_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data_in_addr',
            name='address',
        ),
        migrations.RemoveField(
            model_name='data_in_addr',
            name='path_of_article_list',
        ),
    ]
