# Generated by Django 4.1.7 on 2023-07-31 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wvi', '0010_kader_kelurahan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameters',
            name='deadline_due_date_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='parameters',
            name='target_child',
            field=models.IntegerField(default=0),
        ),
    ]