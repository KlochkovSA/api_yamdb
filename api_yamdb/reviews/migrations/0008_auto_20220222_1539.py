# Generated by Django 2.2.16 on 2022-02-22 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20220218_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(verbose_name='Дата публикации'),
        ),
    ]
