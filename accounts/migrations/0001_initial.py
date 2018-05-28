# Generated by Django 2.0.5 on 2018-05-28 15:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Leads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('email_address', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Leads',
            },
        ),
    ]
