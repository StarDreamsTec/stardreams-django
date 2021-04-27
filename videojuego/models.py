from itertools import groupby

from django.db import models
from django.db.models import Sum, F
from django.utils.translation import gettext_lazy as _
import random, string
from django.contrib.auth.models import User
import datetime


# Create your models here.

class Genero(models.IntegerChoices):
    MUJER = 1, _('Mujer')
    HOMBRE = 2, _('Hombre')
    OTRO = 3, _('Otro')


class Rama(models.IntegerChoices):
    NONE = 0, _('Indefinido')
    CIENCIA = 1, _('Ciencia')
    TEC = 2, _('Tecnología')
    ING = 3, _('Ingeniería')
    MAT = 4, _('Matemáticas')


class Personaje(models.IntegerChoices):
    ASTRO = 1, _('Astronauta')
    CIENTIFICA = 2, _('Científica')


class GradoEscolar(models.IntegerChoices):
    PRIM1 = 1, _('Primaria 1º')
    PRIM2 = 2, _('Primaria 2º')
    PRIM3 = 3, _('Primaria 3º')
    PRIM4 = 4, _('Primaria 4º')
    PRIM5 = 5, _('Primaria 5º')
    PRIM6 = 6, _('Primaria 6º')
    SEC1 = 7, _('Secundaria 1º')
    SEC2 = 8, _('Secundaria 2º')
    SEC3 = 9, _('Secundaria 3º')


class Profesor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        default="",
        null=False
    )
    genero = models.IntegerField(choices=Genero.choices, default=Genero.OTRO, null=True)
    edad = models.PositiveIntegerField()
    gradoEscolar = models.PositiveIntegerField(choices=GradoEscolar.choices, null=False)
    token = models.CharField(max_length=10,
                             blank=True,
                             null=True,
                             editable=True)

    def save(self, *args, **kwargs):
        t = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        while Profesor.objects.filter(token=t).exists():
            t = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        self.token = t
        super(Profesor, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.get_full_name()


class Jugador(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        default="",
        null=False
    )
    genero = models.IntegerField(choices=Genero.choices, default=Genero.OTRO)
    edad = models.PositiveIntegerField()
    gradoEscolar = models.IntegerField(choices=GradoEscolar.choices, null=False)
    ramaPreferida = models.IntegerField(choices=Rama.choices, blank=True, null=True, default=Rama.NONE)
    profesor = models.CharField(max_length=10, blank=True, null=True)
    personaje = models.IntegerField(choices=Personaje.choices, default=Personaje.ASTRO)

    def __str__(self):
        return self.user.get_full_name()

    def is_complete(self):
        ciencia = Nivel.objects.filter(jugador=self, completado=True, rama=Rama.CIENCIA).exists()
        tec = Nivel.objects.filter(jugador=self, completado=True, rama=Rama.TEC).exists()
        ing = Nivel.objects.filter(jugador=self, completado=True, rama=Rama.ING).exists()
        mat = Nivel.objects.filter(jugador=self, completado=True, rama=Rama.MAT).exists()
        return ciencia and tec and ing and mat

    def total_time(self):
        sesion_time = Sesion.objects.filter(jugador=self).annotate(duration=F('fin') - F('inicio'))
        return sesion_time.aggregate(sum=Sum('duration'))['sum']

    def sesion_num(self):
        count = Sesion.objects.filter(jugador=self).count()
        return count


class Sesion(models.Model):
    inicio = models.DateTimeField(blank=True, null=True)
    fin = models.DateTimeField(blank=True, null=True)
    jugador = models.ForeignKey(Jugador, models.CASCADE, blank=False, null=False)

    def __str__(self):
        return str(self.jugador) + " " + str(self.inicio.date())


class Nivel(models.Model):  # Intento Nivel
    completado = models.BooleanField()
    tiempo = models.FloatField(blank=True, null=True)  # Tiempo que tomó completarlo
    rama = models.IntegerField(choices=Rama.choices)
    tiempoTerminacion = models.DateTimeField(null=True)  # Cuál es el mas reciente
    jugador = models.ForeignKey(Jugador, models.CASCADE, blank=False, null=False)

    def __str__(self):
        return str(self.jugador) + " " + str(self.rama)
