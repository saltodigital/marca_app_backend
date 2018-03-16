from django.contrib.auth.models import Group
from rest_framework import serializers
from asistencia.models import (Horario, Asistencia, Retraso)
from parametrizacion.serializers import (UserSerializer, PersonaSerializer,
ProyectoSerializer)
from parametrizacion.models import (Pais, Region, Municipio, Empresa, Cargo, 
User, ContactoEmpresa, Persona, Estado, Tipo, Proyecto,ProyectoUsuario)

class AsistenciaSerializer(serializers.HyperlinkedModelSerializer):
    usuario=UserSerializer(read_only=True)
    usuario_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=User.objects.all())
    proyecto=ProyectoSerializer(read_only=True)
    proyecto_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Proyecto.objects.all())
    class Meta:
        model = Asistencia
        fields=('id','usuario','usuario_id','proyecto','proyecto_id','entrada','horaEntrada','longitud','latitud')

class RetrasoSerializer(serializers.HyperlinkedModelSerializer):
    usuario=UserSerializer(read_only=True)
    usuario_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=User.objects.all())
    class Meta:
        model = Retraso
        fields=('id','usuario','usuario_id','fecha','motivo')

class HorarioSerializer(serializers.HyperlinkedModelSerializer):
    proyecto=ProyectoSerializer(read_only=True)
    proyecto_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Proyecto.objects.all())
    class Meta:
        model = Horario
        fields=('id','nombre','fechaInicio','fechaFin','proyecto','proyecto_id','horaInicio','horaFin','primerDia','jornada','cantidadHoras','ultimoDia')


