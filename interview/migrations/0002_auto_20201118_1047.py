# Generated by Django 3.0.2 on 2020-11-18 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidate',
            options={'permissions': [('export', 'Can export candidate list'), ('notify', 'notify interviewer for candidate review')], 'verbose_name': '应聘者', 'verbose_name_plural': '应聘者'},
        ),
    ]
