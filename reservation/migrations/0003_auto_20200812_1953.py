# Generated by Django 3.1 on 2020-08-12 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_auto_20200811_1512'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservation',
            options={'ordering': ('-created',), 'verbose_name': 'رزرو', 'verbose_name_plural': 'رزرو شده\u200cها'},
        ),
    ]
