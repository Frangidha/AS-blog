# Generated by Django 3.2.19 on 2023-11-04 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='contribution_and_originality',
            new_name='rating',
        ),
        migrations.RemoveField(
            model_name='review',
            name='discussion_and_interpretation',
        ),
        migrations.RemoveField(
            model_name='review',
            name='methodology_and_experimental_design',
        ),
        migrations.RemoveField(
            model_name='review',
            name='research_objective_and_importance',
        ),
        migrations.RemoveField(
            model_name='review',
            name='results_and_data_analysis',
        ),
        migrations.CreateModel(
            name='Technique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(default='test')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='techniques', to='blog.category')),
            ],
        ),
    ]