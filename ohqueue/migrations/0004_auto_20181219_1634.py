# Generated by Django 2.1.4 on 2018-12-19 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_auto_20181218_2250'),
        ('ohqueue', '0003_auto_20181219_0355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ohqueue',
            name='questions',
        ),
        migrations.AddField(
            model_name='ohqueue',
            name='questions',
            field=models.ManyToManyField(null=True, to='questions.Question'),
        ),
    ]