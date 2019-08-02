# Generated by Django 2.1.7 on 2019-08-02 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_inactiveissue'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnassignedIssuesActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hoster', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=500)),
                ('repository', models.CharField(max_length=100)),
                ('number', models.SmallIntegerField()),
                ('url', models.URLField()),
            ],
        ),
    ]
