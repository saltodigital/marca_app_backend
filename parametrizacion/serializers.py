from django.contrib.auth.models import Group
from rest_framework import serializers
from parametrizacion.models import (Pais, Region, Municipio, Empresa, Cargo, 
User, ContactoEmpresa, Persona, Estado, Tipo, Proyecto, ContactoProyecto,ProyectoUsuario)


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
        fields=('url','id','nombre','rut','direccion','correoElectronico','telefono','telefonoFijo','municipio','municipio_id','field')

#Api rest para Cargo
class CargoSerializer(serializers.HyperlinkedModelSerializer):
    cliente = EmpresaSerializer(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Empresa.objects.all())
    class Meta:
        model = Cargo
        fields=('id','nombre','cliente_id','cliente','nivel')

class PersonaSerializer(serializers.HyperlinkedModelSerializer):
    municipio_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Municipio.objects.all())
    municipio = MunicipioSerializer(read_only=True)
    class Meta:
        model = Persona
        fields=('url','id','nombre','primerApellido','segundoApellido','rut','genero','estadoCivil',
        'correoElectronico','telefono','telefonoFijo','municipio','municipio_id','fechaNacimiento')

class EmpresaContactoSerializer(serializers.HyperlinkedModelSerializer):
    persona=PersonaSerializer(read_only=True)
    persona_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Persona.objects.all())
    empresa=EmpresaSerializer(read_only=True)
    empresa_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Empresa.objects.all())
    class Meta:
        model = ContactoEmpresa
        fields=('id','persona','persona_id','empresa','empresa_id','cargo')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    persona=PersonaSerializer(read_only=True)
    #persona_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Persona.objects.all())
    cargo=CargoSerializer(read_only=True)
    #cargo_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Cargo.objects.all())
    class Meta:
        model = User
        fields = ('url', 'first_name', 'last_name', 'email', 'password','groups','username','id','persona','cargo')
    '''
    def restore_object(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user
    '''
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save
        return user
    


class EstadoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Estado
        fields=('id', 'app', 'nombre', 'icono', 'color','orden')

class TipoSerializer(serializers.HyperlinkedModelSerializer):
    	
    class Meta:
        model = Tipo
        fields=( 'id','app', 'nombre' , 'icono' , 'color')

class ProyectoSerializer(serializers.HyperlinkedModelSerializer):
    municipio_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Municipio.objects.all())
    municipio = MunicipioSerializer(read_only=True)
    estado_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Estado.objects.all())
    #estado = EstadoSerializer(read_only=True)
    tipo_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Tipo.objects.all())
    #tipo = EstadoSerializer(read_only=True)
    empresa=EmpresaSerializer(read_only=True)
    empresa_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Empresa.objects.all())
    class Meta:
        model = Proyecto
        fields=('url','id','nombre','descripcion','valorAdjudicado','latitud','longitud','fechaInicio',
        'fechaFin','municipio','municipio_id','empresa','empresa_id','estado_id','tipo_id')

class ProyectoContactoSerializer(serializers.HyperlinkedModelSerializer):
    persona=PersonaSerializer(read_only=True)
    persona_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Persona.objects.all())
    proyecto=ProyectoSerializer(read_only=True)
    proyecto_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Proyecto.objects.all())
    class Meta:
        model = ContactoProyecto
        fields=('id','persona','persona_id','proyecto','proyecto_id','cargo')

class ProyectoUsuarioSerializer(serializers.HyperlinkedModelSerializer):
    usuario=UserSerializer(read_only=True)
    usuario_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=User.objects.all())
    cargo=CargoSerializer(read_only=True)
    cargo_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Cargo.objects.all())
    proyecto=ProyectoSerializer(read_only=True)
    proyecto_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Proyecto.objects.all())
    class Meta:
        model = ProyectoUsuario
        fields=('id','usuario','usuario_id','proyecto','proyecto_id','cargo','cargo_id')