# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

#Modelos generales.
class BasePermisoModel(models.Model):
    created_on = models.DateTimeField(auto_now_add = True)
    modified_on = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True
        permissions = (
            ("can_see_all", "Ver todos"),
            ("can_see_owner", "Solo los que creo"),
        )

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
    estadoCiv = (
        (u'0',u'[Seleccione...]'),
        (u'S',u'Soltero'),
        (u'C',u'Casado'),
        (u'O',u'Otro'),
    )
    rut = models.CharField(max_length=50, unique=True)
    primerApellido = models.CharField(max_length=100)
    segundoApellido = models.CharField(max_length=100)
    fechaNacimiento = models.DateField()
    genero = models.CharField(max_length=1,choices=generos, default=0)
    estadoCivil = models.CharField(max_length=1, choices=estadoCiv,default=0)
    correoElectronico = models.EmailField(max_length=200)
    telefono = models.CharField(max_length=100)
    telefonoFijo = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre + ' ' + self.primerApellido

class Empresa(BaseModel):
    rut = models.CharField(max_length=50, unique=True,
    validators=[RegexValidator(regex='^([0-9]+-[0-9K])$',
    message='Rut no valido',code='invalid_rut')])
    field = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    correoElectronico = models.EmailField(max_length=200)
    telefono = models.CharField(max_length=100)
    telefonoFijo = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    numero = models.CharField(max_length=100,blank=True,null=True)
    estado = models.BooleanField( default = 1 )
    fechaEstadoProyecto = models.DateField(null = True , blank = True)

class Cargo(BaseModel):
    nivel = models.IntegerField()
    cliente = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class User(AbstractUser):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE,blank=True,null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        db_table = 'auth_user'

class ContactoEmpresa(BasePermisoModel):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=255,null = True , blank = True) 

class EmpresaUsuario(BasePermisoModel):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE) 

    class Meta:
        unique_together = (("usuario" , "empresa"),)

class Estado(BaseModel):
    app = models.CharField(max_length = 250)
    color = models.CharField(max_length = 250 , blank= True)
    icono = models.CharField(max_length = 250 , blank= True)
    estado = models.BooleanField( default = 1 )
    codigo = models.IntegerField(blank= True,null=True)
    orden=models.IntegerField()

    def __unicode__(self):
        return self.app + '.' + self.nombre
    class Meta:
        unique_together = (("app" , "codigo" ),)

    def ObtenerID(self,app,codigo):
        return Estado.objects.get(app=app,codigo=codigo).id

class Tipo(BaseModel):
    app = models.CharField(max_length = 250)
    color = models.CharField(max_length = 250 , blank=True)
    codigo = models.IntegerField(blank= True,null=True)
    icono = models.CharField(max_length = 200 , blank=True)

    def __unicode__(self):
        return self.app + '.' + self.nombre
    class Meta:
        unique_together = (("app" , "codigo" ),)

    def ObtenerID(self,app,codigo):
        return Tipo.objects.get(app=app,codigo=codigo).id

class Proyecto(BaseModel):
    municipio = models.ForeignKey(Municipio , related_name = 'f_Municipio_parametrizacion' , on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=255,null = True , blank = True)
    estado = models.ForeignKey(Estado , related_name = 'f_Estado_proyecto_estado' , on_delete=models.PROTECT )
    valorAdjudicado = models.FloatField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    tipo = models.ForeignKey(Tipo , related_name = 'f_P_tipo_proyecto' , on_delete=models.PROTECT)
    fechaInicio = 	models.DateField(null = True , blank = True)
    fechaFin = models.DateField(null = True , blank = True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    idProyecto = models.CharField(max_length=10,null = True , blank = True)
    nombreCalle = models.CharField(max_length=255,null = True , blank = True)
    numero = models.CharField(max_length=50,null = True , blank = True)
    codigoPostal = models.CharField(max_length=50,null = True , blank = True)
    ip = models.CharField(max_length=25,null = True , blank = True)

    class Meta:
        unique_together = (("nombre" , "empresa"),)

class ContactoProyecto(BasePermisoModel):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=255,null = True , blank = True) 

    class Meta:
        unique_together = (("persona" , "proyecto"),)

class ProyectoUsuario(BasePermisoModel):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE) 
    desde = models.DateField(null = True , blank = True)
    hasta = models.DateField(null = True , blank = True)
    horas = models.FloatField(default=0)

    class Meta:
        unique_together = (("usuario" , "proyecto"),)
