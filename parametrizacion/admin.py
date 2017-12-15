from django.contrib import admin
from .models import Persona, Pais, User
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


admin.site.register(Persona,AdminPersona)
admin.site.register(Pais,AdminPais)

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