"""marcaAPP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from rest_framework import routers
from parametrizacion import views
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'pais', views.PaisViewSet)
router.register(r'regiones', views.RegionViewSet)
router.register(r'municipios', views.MunicipioViewSet)
router.register(r'cargos', views.CargoViewSet)
router.register(r'empresas', views.EmpresaViewSet)
router.register(r'estados', views.EstadoViewSet)
router.register(r'tipos', views.TipoViewSet)
router.register(r'personas', views.PersonaViewSet)
router.register(r'proyectos', views.ProyectoViewSet)

schema_view = get_schema_view(title='Documentacion Marca APP API',renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^docs', schema_view, name="docs"),
    url(r'^api/', include(router.urls)), 
]
