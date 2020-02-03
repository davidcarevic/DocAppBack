# Generated by Django 3.0.2 on 2020-02-03 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='comments',
            options={'verbose_name_plural': 'Comments'},
        ),
        migrations.AlterModelOptions(
            name='elements',
            options={'verbose_name_plural': 'Elements'},
        ),
        migrations.AlterModelOptions(
            name='items',
            options={'verbose_name_plural': 'Items'},
        ),
        migrations.AlterModelOptions(
            name='projects',
            options={'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterModelOptions(
            name='roles',
            options={'verbose_name_plural': 'Roles'},
        ),
        migrations.AlterModelOptions(
            name='sections',
            options={'verbose_name_plural': 'Sections'},
        ),
        migrations.AlterModelOptions(
            name='teammembers',
            options={'verbose_name_plural': 'Team Members'},
        ),
        migrations.AlterModelOptions(
            name='teamprojects',
            options={'verbose_name_plural': 'Team Projects'},
        ),
        migrations.AlterModelOptions(
            name='teams',
            options={'verbose_name_plural': 'Teams'},
        ),
        migrations.AlterField(
            model_name='teammembers',
            name='role',
            field=models.ForeignKey(db_column='role_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Roles'),
        ),
        migrations.AlterField(
            model_name='teammembers',
            name='team',
            field=models.ForeignKey(db_column='team_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Teams'),
        ),
        migrations.AlterField(
            model_name='teamprojects',
            name='team',
            field=models.ForeignKey(db_column='team_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Teams'),
        ),
    ]
