# Generated by Django 4.2.4 on 2023-10-25 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='process',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='time',
            field=models.IntegerField(),
        ),
    ]
