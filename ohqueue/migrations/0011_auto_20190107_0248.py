# Generated by Django 2.1.4 on 2019-01-07 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ohqueue', '0010_auto_20190104_2005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ohqueue',
            options={'verbose_name': 'Office Hours Queue', 'verbose_name_plural': 'Office Hours Queues'},
        ),
        migrations.AlterField(
            model_name='ohqueue',
            name='friday_times',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ohqueue',
            name='last_answer_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='ohqueue',
            name='monday_times',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ohqueue',
            name='saturday_times',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ohqueue',
            name='sunday_times',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ohqueue',
            name='thursday_times',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ohqueue',
            name='tuesday_times',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ohqueue',
            name='wednesday_times',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
