# Generated by Django 2.1.4 on 2019-01-04 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ohqueue', '0009_auto_20190103_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ohqueue',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
