# Generated by Django 3.2 on 2021-04-16 03:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videojuego', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jugador',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='genero',
            field=models.IntegerField(choices=[(1, 'Mujer'), (2, 'Hombre'), (3, 'Otro')], default=3, null=True),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
