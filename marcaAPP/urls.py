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
from rest_framework_swagger.views import get_swagger_view
from rest_framework.renderers import SwaggerUIRenderer, OpenAPIRenderer

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'pais', views.PaisViewSet)
router.register(r'region', views.RegionViewSet)
router.register(r'municipios', views.MunicipioViewSet)
router.register(r'cargos', views.CargoViewSet)
router.register(r'empresa', views.EmpresaViewSet)

schema_view = get_swagger_view(title='Documentacion Marca APP API',renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    url(r'^', schema_view, name="docs"),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls'))
]
