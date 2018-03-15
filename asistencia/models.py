# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from parametrizacion.models import (BaseModel, BasePermisoModel, User, Persona, Estado, Tipo, Proyecto)
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import datetime

class Horario(BaseModel):
    jornadas = (
        (1,u'Lunes'),
        (2,u'Martes'),
        (3,u'Miercoles'),
        (4,u'Jueves'),
        (5,u'Viernes'),
        (6,u'Sabado'),
        (7,u'Domingo')
    )
    fechaInicio = 	models.DateField()
    fechaFin = models.DateField()
    horaInicio = 	models.TimeField()
    horaFin = models.TimeField()
    primerDia = models.IntegerField(choices=jornadas,default=1)
    ultimoDia = models.IntegerField(choices=jornadas,default=6)
    jornada = models.CharField(default='1',max_length=25)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    cantidadHoras = models.IntegerField(default=24)

class Asistencia(BasePermisoModel):
    entrada = models.DateField(auto_now_add = True)
    horaEntrada = 	models.TimeField(auto_now_add=True)
    longitud = models.FloatField()
    latitud = models.FloatField()
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Retraso(BasePermisoModel):
    fecha = models.DateTimeField(auto_now_add = True)
    motivo = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

