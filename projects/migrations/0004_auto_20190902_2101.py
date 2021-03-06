# Generated by Django 2.2.5 on 2019-09-02 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20190902_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='originator',
            name='email',
            field=models.EmailField(max_length=64, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='originator',
            name='first_name',
            field=models.CharField(max_length=64, verbose_name='Imię'),
        ),
        migrations.AlterField(
            model_name='originator',
            name='last_name',
            field=models.CharField(max_length=64, verbose_name='Nazwisko'),
        ),
        migrations.AlterField(
            model_name='originator',
            name='pesel',
            field=models.IntegerField(verbose_name='PESEL'),
        ),
        migrations.AlterField(
            model_name='originator',
            name='phone',
            field=models.IntegerField(verbose_name='Numer telefonu'),
        ),
        migrations.AlterField(
            model_name='originator',
            name='post_code',
            field=models.CharField(max_length=6, verbose_name='Kod pocztowy'),
        ),
    ]
