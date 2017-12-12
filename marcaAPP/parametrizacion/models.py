# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings

#Modelos generales.
class BaseModel(models.Model):
	nombre = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
	modified_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizacion')

	class Meta:
 		abstract = True

	def __str__(self):
		return self.nombre

class Pais(BaseModel):
    validaRut = models.CharField(max_length=50)

class Region(BaseModel):
    pais = models.ForeignKey(Pais)

class Municipio(BaseModel):
    region = models.ForeignKey(Region)

class Persona(BaseModel):
	generos = ((u'0',u'[Seleccione...]'),(u'1',u'Masculino'),
		(u'2',u'Femenino'),)
    estadoCiviles = ((u'0',u'[Seleccione...]'),(u'1',u'Soltero'),
		(u'2',u'Casado'),)	
	rut = models.IntegerField()
	#tipoIdentificacion = models.ForeignKey(Tipo , related_name = 'fk_Persona_tipo',on_delete=models.PROTECT)
	primerApellido = models.CharField(max_length=100)
    segundoApellido = models.CharField(max_length=100)
	fechaNacimiento = models.DateField()
	genero = models.CharField(max_length=1,choices=generos, default=0)
    estadoCivil = models.CharField(max_length=1,choices=estadoCiviles, default=0)
    correoElectronico = models.EmailField(max_length=200)
    telefono = models.CharField(max_length=100)
    telefonoFijo = models.CharField(max_length=100)
    
	def __str__(self):
		return self.nombre + ' ' + self.primerApellido

	class Meta:		
		unique = [
			["rut",],
		]

class Empresa(BaseModel):
	rut = models.CharField(max_length=255, unique=True)
	direccion = models.CharField(max_length=255)

class Cargo(BaseModel):
	empresa = models.ForeignKey(Empresa)
	firma_cartas = models.BooleanField(default=False)



