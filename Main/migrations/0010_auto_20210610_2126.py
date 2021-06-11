# Generated by Django 3.2.4 on 2021-06-10 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0009_dataset_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataset',
            options={'verbose_name': 'Датасет', 'verbose_name_plural': 'Датасеты'},
        ),
        migrations.AlterField(
            model_name='dataset',
            name='status',
            field=models.CharField(choices=[('P', 'Processing'), ('R', 'Ready'), ('I', 'In queue')], max_length=2, null=True),
        ),
    ]
