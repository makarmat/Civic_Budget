# Generated by Django 2.2.5 on 2019-09-02 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Originator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('pesel', models.IntegerField(max_length=11)),
                ('phone', models.IntegerField(max_length=9)),
                ('email', models.CharField(max_length=64)),
                ('post_code', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('start_date', models.DateField()),
                ('finish_date', models.DateField()),
                ('region', models.IntegerField(choices=[(1, 'jeleniogórski'), (2, 'legnicki'), (3, 'wałbrzyski'), (4, 'wrocławski'), (5, 'm. Wrocław')])),
                ('subject', models.IntegerField(choices=[(1, 'sport'), (2, 'turystyka'), (3, 'kultura'), (4, 'wsparcie osób z niepełnosprawnościami'), (5, 'wsparcie społeczeństwa obywatelskiego'), (6, 'wsparcie seniorów'), (7, 'wsparcie rzemiosła')])),
                ('description_short', models.TextField(max_length=1000)),
                ('description_long', models.TextField(max_length=2000)),
            ],
        ),
    ]
