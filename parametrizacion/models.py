# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

#Modelos generales.
class BaseModel(models.Model):
    nombre = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add = True)
    modified_on = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True
        permissions = (
            ("can_see_all", "Ver todos"),
            ("can_see_owner", "Solo los que creo"),
        )

    def __str__(self):
        return self.nombre

class Pais(BaseModel):
    validaRut = models.CharField(max_length=50)

class Region(BaseModel):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

class Municipio(BaseModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

class Persona(BaseModel):
    generos = (
        (u'0',u'[Seleccione...]'),
        (u'1',u'Masculino'),
        (u'2',u'Femenino')
    )
    rut = models.CharField(max_length=50, unique=True)
    primerApellido = models.CharField(max_length=100)
    segundoApellido = models.CharField(max_length=100)
    fechaNacimiento = models.DateField()
    genero = models.CharField(max_length=1,choices=generos, default=0)
    estadoCivil = models.CharField(max_length=1, default=0)
    correoElectronico = models.EmailField(max_length=200)
    telefono = models.CharField(max_length=100)
    telefonoFijo = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre + ' ' + self.primerApellido

class Empresa(BaseModel):
    rut = models.CharField(max_length=50, unique=True)
    field = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=255)
    correoElectronico = models.EmailField(max_length=200)
    telefono = models.CharField(max_length=100)
    telefonoFijo = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)

class Cargo(BaseModel):
    nivel = models.IntegerField()
    cliente = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class User(AbstractUser):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE,blank=True,null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        db_table = 'auth_user'





