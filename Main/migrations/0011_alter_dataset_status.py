# Generated by Django 3.2.4 on 2021-06-12 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0010_auto_20210610_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='status',
            field=models.CharField(choices=[('P', 'Processing'), ('R', 'Ready'), ('I', 'In queue'), ('F', 'Failed')], max_length=2, null=True),
        ),
    ]