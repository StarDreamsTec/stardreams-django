from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
import random, string
from django.contrib.auth.models import User
import django.db.models.signals as signals

# Create your models here.


class Genero(models.IntegerChoices):
    MUJER = 1, _('Mujer')
    HOMBRE = 2, _('Hombre')
    OTRO = 3, _('Otro')


class Rama(models.IntegerChoices):
    CIENCIA = 1, _('Ciencia')
    TEC = 2, _('Tecnología')
    ING = 3, _('Ingeniería')
    MAT = 4, _('Matemáticas')


class Profesor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        default="",
        null=False
    )
    genero = models.IntegerField(choices=Genero.choices, default=Genero.OTRO, null=True)
    edad = models.PositiveIntegerField()
    gradoEscolar = models.PositiveIntegerField()
    token = models.CharField(max_length=10,
                           blank=True,
                            null=True,
                           editable=False)

    def save(self, *args, **kwargs):
        t = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        while Profesor.objects.filter(token=t).exists():
            t = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        self.token = t
        super(Profesor, self).save(*args, **kwargs)


class Jugador(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        default="",
        null=False
    )
    genero = models.IntegerField(choices=Genero.choices, default=Genero.OTRO)
    edad = models.PositiveIntegerField()
    gradoEscolar = models.PositiveIntegerField()
    tiempoJuego = models.PositiveIntegerField(blank=True, null=True)
    ramaPreferida = models.IntegerField(choices=Rama.choices, blank=True, null=True)
    profesor = models.CharField(max_length=10, blank=True, null=True)


class Sesion(models.Model):
    duracion = models.PositiveIntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    jugador = models.ForeignKey(Jugador, models.CASCADE, blank=False, null=False)


class Nivel(models.Model):
    completado = models.BooleanField()
    tiempo = models.PositiveIntegerField(blank=True, null=True) # Tiempo que tomó completarlo
    rama = models.IntegerField(choices=Rama.choices)
    tiempoTerminacion = models.DateTimeField(null=True) # Cuál es el mas reciente
    jugador = models.ForeignKey(Jugador, models.CASCADE, blank=False, null=False)