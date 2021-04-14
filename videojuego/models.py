from django.db import models
from django.utils.translation import gettext_lazy as _
import random, string


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
    nombre = models.CharField(max_length=50)
    genero = models.IntegerField(choices=Genero.choices, default=Genero.OTRO)
    edad = models.PositiveIntegerField()
    correoElectronico = models.EmailField()
    gradoEscolar = models.PositiveIntegerField()
    token = models.CharField(max_length=10,
                           blank=True,
                           editable=False)

    def save(self, *args, **kwargs):
        t = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        while Profesor.objects.filter(token=t).exists():
            t = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        self.token = t
        super(Profesor, self).save(*args, **kwargs)


class Jugador(models.Model):
    nombre = models.CharField(max_length=50)
    genero = models.IntegerField(choices=Genero.choices, default=Genero.OTRO)
    edad = models.PositiveIntegerField()
    gradoEscolar = models.PositiveIntegerField()
    tiempoJuego = models.PositiveIntegerField()
    ramaPreferida = models.IntegerField(choices=Rama.choices)
    profesor = models.ForeignKey(Profesor, models.SET_NULL, blank=True, null=True)


class Sesion(models.Model):
    horaInicio = models.DateTimeField()
    horaFin = models.DateTimeField()
    jugador = models.ForeignKey(Jugador, models.CASCADE, blank=False, null=False)


class Nivel(models.Model):
    completado = models.BooleanField()
    tiempo = models.PositiveIntegerField()
    rama = models.IntegerField(choices=Rama.choices)
    tiempoTerminacion = models.DateTimeField(null=True)
    jugador = models.ForeignKey(Jugador, models.CASCADE, blank=False, null=False)
