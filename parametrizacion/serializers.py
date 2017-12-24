from django.contrib.auth.models import Group
from rest_framework import serializers
from parametrizacion.models import (Pais, Region, Municipio, Empresa, Cargo, 
User, ContactoEmpresa, Persona, Estado, Tipo)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('url', 'first_name', 'last_name', 'email', 'password','groups')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

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

class PersonaSerializer(serializers.HyperlinkedModelSerializer):
    municipio_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Municipio.objects.all())
    municipio = MunicipioSerializer(read_only=True)
    class Meta:
        model = Persona
        fields=('url','id','primerApellido','segundoApellido','rut','genero','estadoCivil','direccion','correoElectronico','telefono','telefonoFijo','municipio','municipio_id' )

class EmpresaContactoSerializer(serializers.HyperlinkedModelSerializer):
    
	persona=PersonaSerializer(read_only=True)
	persona_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Persona.objects.all())

	class Meta:
		model = ContactoEmpresa
		fields=('id','persona','persona_id')

class EstadoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Estado
        fields=('id', 'app', 'nombre', 'icono', 'color')

class TipoSerializer(serializers.HyperlinkedModelSerializer):
    	
    class Meta:
        model = Tipo
        fields=( 'id','app', 'nombre' , 'icono' , 'color')