# Generated by Django 2.1.7 on 2019-08-01 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20190801_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='teams',
            field=models.ManyToManyField(related_name='contributors', to='data.Team'),
        ),
    ]