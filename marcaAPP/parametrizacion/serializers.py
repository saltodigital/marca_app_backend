from django.contrib.auth.models import Group
from rest_framework import serializers
from parametrizacion.models import Pais, Region, Municipio, Empresa, Cargo, User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class PaisSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Pais
		fields=('id','nombre','validaRut')

class RegionSerializer(serializers.HyperlinkedModelSerializer):
    pais_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Pais.objects.all())
    pais = PaisSerializer(read_only=True)
    class Meta:
        model = Region
    fields=('id','nombre','pais','pais_id')

class MunicipioSerializer(serializers.HyperlinkedModelSerializer):
    
    region_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Region.objects.all())
    region = RegionSerializer(read_only=True)
    class Meta:
        model = Municipio
        fields=('id','nombre','region','region_id')

class EmpresaSerializer(serializers.HyperlinkedModelSerializer):
    municipio_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Municipio.objects.all())
    municipio = MunicipioSerializer(read_only=True)
	#logo = serializers.ImageField(required=False)
    class Meta:
        model = Empresa
        fields=('url','id','nombre','rut','direccion','correoElectronico','telefono','telefonoFijo','municipio','municipio_id' )

#Api rest para Cargo
class CargoSerializer(serializers.HyperlinkedModelSerializer):
	empresa = EmpresaSerializer(read_only=True)

	class Meta:
		model = Cargo
		fields=('id','nombre','empresa','nivel')
