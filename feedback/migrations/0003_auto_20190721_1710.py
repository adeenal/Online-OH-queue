# Generated by Django 2.1.4 on 2019-07-21 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_auto_20190721_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='ta',
        ),
        migrations.AddField(
            model_name='feedback',
            name='ta_email',
            field=models.CharField(default='No Account', max_length=64),
        ),
    ]