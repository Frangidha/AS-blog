# Generated by Django 3.2.19 on 2024-01-07 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_banner_color'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'ordering': ('title',), 'verbose_name_plural': 'Banners'},
        ),
    ]
