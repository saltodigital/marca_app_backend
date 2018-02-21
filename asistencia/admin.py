from django.contrib import admin
from asistencia.models import (Horario, Asistencia, Retraso)


class AdminAsistencia(admin.ModelAdmin):
	list_display=('usuario','proyecto','entrada')
	search_fields=('entrada','usuario')
	list_filter=('proyecto','usuario')


class AdminHorario(admin.ModelAdmin):
	list_display=('proyecto','fechaInicio','fechaFin')
	search_fields=('fechaInicio','fechaFin')
	list_filter=('proyecto',)

admin.site.register(Asistencia,AdminAsistencia)
admin.site.register(Horario,AdminHorario)