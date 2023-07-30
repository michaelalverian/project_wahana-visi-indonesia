# Generated by Django 4.1.7 on 2023-04-27 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wvi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='gender',
            field=models.CharField(max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='child',
            name='age',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='child',
            name='community',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='child',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='child',
            name='name',
            field=models.TextField(null=True),
        ),
    ]
