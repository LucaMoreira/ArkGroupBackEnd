# Generated by Django 4.2.6 on 2023-10-31 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudpharma', '0004_alter_choice_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice',
            field=models.CharField(choices=[('1', 'Domingo'), ('2', 'Segunda'), ('3', 'Terca'), ('4', 'Quarta'), ('5', 'Quinta'), ('6', 'Sexta'), ('7', 'Sabado')], max_length=50, unique=True),
        ),
    ]