# Generated by Django 3.2 on 2021-04-17 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videojuego', '0006_auto_20210416_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesor',
            name='token',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]