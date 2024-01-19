# Generated by Django 3.2.19 on 2023-11-04 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20231104_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='technique',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='posts_using_technique', to='blog.technique'),
        ),
    ]