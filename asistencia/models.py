# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from parametrizacion.models import (BaseModel, BasePermisoModel, User, Persona, Estado, Tipo, Proyecto)
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import datetime

class Horario(BaseModel):
    fechaInicio = 	models.DateField()
    fechaFin = models.DateField()
    horaInicio = 	models.TimeField()
    horaFin = models.TimeField()
    primerDia = models.IntegerField()
    ultimoDia = models.IntegerField()
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

class Asistencia(BasePermisoModel):
    entrada = models.DateField(auto_now_add = True)
    horaEntrada = 	models.TimeField()
    longitud = models.FloatField()
    latitud = models.FloatField()
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Retraso(BasePermisoModel):
    fecha = models.DateTimeField(auto_now_add = True)
    motivo = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

