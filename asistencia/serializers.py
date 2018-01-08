from django.contrib.auth.models import Group
from rest_framework import serializers
from asistencia.models import (Horario, Asistencia, Retraso)
from parametrizacion.serializers import (UserSerializer, PersonaSerializer,
ProyectoSerializer)
from parametrizacion.models import (Pais, Region, Municipio, Empresa, Cargo, 
User, ContactoEmpresa, Persona, Estado, Tipo, Proyecto, ContactoProyecto,ProyectoUsuario)

class AsistenciaSerializer(serializers.HyperlinkedModelSerializer):
    usuario=UserSerializer(read_only=True)
    usuario_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=User.objects.all())
    proyecto=ProyectoSerializer(read_only=True)
    proyecto_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Proyecto.objects.all())
    class Meta:
        model = Asistencia
        fields=('id','usuario','usuario_id','proyecto','proyecto_id','entrada','longitud','latitud')

class RetrasoSerializer(serializers.HyperlinkedModelSerializer):
    usuario=UserSerializer(read_only=True)
    usuario_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=User.objects.all())
    proyecto=ProyectoSerializer(read_only=True)
    proyecto_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Proyecto.objects.all())
    class Meta:
        model = Asistencia
        fields=('id','usuario','usuario_id','proyecto','proyecto_id','fecha','motivo')


