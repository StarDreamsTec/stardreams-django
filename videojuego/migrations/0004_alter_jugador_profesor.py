# Generated by Django 3.2 on 2021-04-16 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videojuego', '0003_alter_profesor_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jugador',
            name='profesor',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
