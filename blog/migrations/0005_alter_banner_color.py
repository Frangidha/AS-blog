# Generated by Django 3.2.19 on 2023-11-26 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20231126_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='color',
            field=models.PositiveIntegerField(choices=[(1, 'On'), (2, 'Off')], default=1),
        ),
    ]
