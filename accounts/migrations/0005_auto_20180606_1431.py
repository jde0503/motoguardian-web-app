# Generated by Django 2.0.4 on 2018-06-06 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180606_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='lat',
            field=models.DecimalField(decimal_places=10, max_digits=20),
        ),
        migrations.AlterField(
            model_name='trip',
            name='lng',
            field=models.DecimalField(decimal_places=10, max_digits=20),
        ),
    ]
