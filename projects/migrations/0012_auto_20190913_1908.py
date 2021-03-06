# Generated by Django 2.2.5 on 2019-09-13 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_project_applied'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coast',
            name='originator',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='coas_originator', to='projects.Originator'),
        ),
        migrations.AlterField(
            model_name='project',
            name='originator',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='project_originator', to='projects.Originator'),
        ),
        migrations.AlterField(
            model_name='project',
            name='region',
            field=models.IntegerField(choices=[('', 'wybierz subregion'), (1, 'jeleniogórski'), (2, 'legnicki'), (3, 'wałbrzyski'), (4, 'wrocławski'), (5, 'm. Wrocław')], verbose_name='Subregion'),
        ),
        migrations.AlterField(
            model_name='project',
            name='subject',
            field=models.IntegerField(choices=[('', 'wybierz obszar merytoryczny'), (1, 'sport'), (2, 'turystyka'), (3, 'kultura'), (4, 'wsparcie osób z niepełnosprawnościami'), (5, 'wsparcie społeczeństwa obywatelskiego'), (6, 'wsparcie seniorów'), (7, 'wsparcie rzemiosła')], verbose_name='Obszar merytoryczny'),
        ),
    ]
