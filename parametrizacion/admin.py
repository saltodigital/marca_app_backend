from django.contrib import admin
from parametrizacion.models import (Pais, Region, Municipio, Empresa, Cargo, 
User, ContactoEmpresa, Persona, Estado, Tipo, Proyecto, ContactoProyecto,ProyectoUsuario)
from django.contrib.auth.admin import UserAdmin
from parametrizacion.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm
)

class AdminPersona(admin.ModelAdmin):
	list_display=('rut','nombre','primerApellido','fechaNacimiento','genero',)
	search_fields=('nombre','primerApellido','rut')
	list_filter=('genero','estadoCivil')

class AdminPais(admin.ModelAdmin):
	list_display=('nombre',)

class AdminRegion(admin.ModelAdmin):
    	list_display=('nombre',)

class AdminMunicipio(admin.ModelAdmin):
    	list_display=('nombre',)

class AdminCargo(admin.ModelAdmin):
    	list_display=('nombre',)

admin.site.register(Persona,AdminPersona)
admin.site.register(Pais,AdminPais)
admin.site.register(Region,AdminRegion)
admin.site.register(Municipio,AdminMunicipio)
admin.site.register(Cargo,AdminCargo)

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (
            None, {
                'fields': (
                    'cargo',
                    'persona'
                )
            }
        ),
    )

class UserAdmin(CustomUserAdmin):
    list_display =  (
        'id',
        'username',
        'email',
        'is_staff',
        'is_active',
        'is_superuser',
        'cargo',
        'persona',
        'last_login',
        'date_joined'
    )

admin.site.register(User,UserAdmin)

class UsarioProyectoline(admin.TabularInline):
    model = ProyectoUsuario
    extra = 3
    classes = ['collapse']

class ContactoProyectoInline(admin.TabularInline):
    model = ContactoProyecto
    extra = 3
    classes = ['collapse']

class ContactoEmpresaline(admin.TabularInline):
    model = ContactoEmpresa
    extra = 3
    classes = ['collapse']
    
class AdminProyecto(admin.ModelAdmin):
    inlines = [ UsarioProyectoline,ContactoProyectoInline ]
    list_display = ('nombre', 'descripcion')
    
admin.site.register(Proyecto, AdminProyecto)

class AdminEmpresa(admin.ModelAdmin):
    inlines = [ ContactoEmpresaline, ]
    list_display = ('nombre', 'rut')
    
admin.site.register(Empresa, AdminEmpresa)

