# Generated by Django 2.0.4 on 2018-06-02 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20180602_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='first_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='device',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
    ]
