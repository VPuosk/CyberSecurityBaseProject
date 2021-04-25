# Generated by Django 3.1.7 on 2021-04-25 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=20)),
                ('text', models.CharField(max_length=200)),
                ('time', models.DateTimeField()),
            ],
        ),
    ]
