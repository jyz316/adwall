# Generated by Django 2.2.4 on 2019-08-26 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name='date published'),
        ),
    ]
