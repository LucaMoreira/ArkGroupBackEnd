# Generated by Django 4.2.5 on 2023-09-30 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudpharma', '0002_alter_medcine_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medcine',
            name='actual_amount',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='medcine',
            name='end_date',
            field=models.DateField(null=True),
        ),
    ]
