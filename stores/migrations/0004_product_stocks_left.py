# Generated by Django 3.2.6 on 2021-08-08 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0003_delete_productimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stocks_left',
            field=models.IntegerField(default=1),
        ),
    ]
