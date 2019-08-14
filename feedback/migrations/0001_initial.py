# Generated by Django 2.1.4 on 2019-07-29 00:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('helpful_scale', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('was_helpful', models.BooleanField(default=False)),
                ('comments', models.CharField(blank=True, max_length=280)),
                ('feedback_time', models.DateTimeField(auto_now_add=True)),
                ('ta_email', models.CharField(default='No Account', max_length=64)),
            ],
        ),
    ]
