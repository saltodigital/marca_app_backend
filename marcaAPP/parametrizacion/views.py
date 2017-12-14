from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from parametrizacion.models import Pais, Region, Municipio, Empresa, Cargo, User
from marcaAPP.resource import MessageNC, ResponseNC
from parametrizacion.serializers import UserSerializer, GroupSerializer, PaisSerializer, RegionSerializer, MunicipioSerializer, EmpresaSerializer, CargoSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PaisViewSet(viewsets.ModelViewSet):
	"""
	Retorna una lista de paises, puede utilizar el parametro (dato) por medio del cual, se podra buscar por todo o parte del nombre.
	"""
	model=Pais
	queryset = model.objects.all()
	serializer_class = PaisSerializer

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Response({ResponseNC.message:'',ResponseNC.status:'success',ResponseNC.data:serializer.data})
		except:
			return Response({ResponseNC.message:MessageNC['vacio'],'success':'fail',ResponseNC.data:''},status=status.HTTP_404_NOT_FOUND)


	def list(self, request, *args, **kwargs):
		try:
			queryset = super(ProvinciaViewSet, self).get_queryset()
			dato = self.request.query_params.get('dato', None)
			if dato:
				qset = (
					Q(nombre__icontains=dato)
					)
				queryset = self.model.objects.filter(qset)
			#utilizar la variable ignorePagination para quitar la paginacion
			ignorePagination= self.request.query_params.get('ignorePagination',None)
			if ignorePagination is None:
				page = self.paginate_queryset(queryset)
				if page is not None:
					serializer = self.get_serializer(page,many=True)	
					return self.get_paginated_response({ResponseNC.message:'','success':'ok',
					ResponseNC.data:serializer.data})
	
			serializer = self.get_serializer(queryset,many=True)
			return Response({ResponseNC.message:'','success':'ok',
					ResponseNC.data:serializer.data})			
		except:
			return Response({ResponseNC.message:MessageNC['errorServidor'],ResponseNC.status:'error',ResponseNC.data:''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


	def create(self, request, *args, **kwargs):
		if request.method == 'POST':
			try:
				serializer = PaisSerializer(data=request.DATA,context={'request': request})

				if serializer.is_valid():
					serializer.save()
					return Response({ResponseNC.message:'El registro ha sido guardado exitosamente','success':'ok',
						ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
				else:
				 	return Response({ResponseNC.message:'datos requeridos no fueron recibidos','success':'fail',
			 		ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
			except:
			 	return Response({ResponseNC.message:'Se presentaron errores al procesar los datos','success':'error',
			  		ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

	def update(self,request,*args,**kwargs):
		if request.method == 'PUT':
			try:
				partial = kwargs.pop('partial', False)
				instance = self.get_object()
				serializer = PaisSerializer(instance,data=request.DATA,context={'request': request},partial=partial)
				if serializer.is_valid():
					self.perform_update(serializer)
					return Response({ResponseNC.message:'El registro ha sido actualizado exitosamente','success':'ok',
						ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
				else:
				 	return Response({ResponseNC.message:'datos requeridos no fueron recibidos','success':'fail',
			 		ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
			except:
			 	return Response({ResponseNC.message:'Se presentaron errores al procesar los datos','success':'error',
					ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

	def destroy(self,request,*args,**kwargs):
		try:
			instance = self.get_object()
			self.perform_destroy(instance)
			return Response({ResponseNC.message:'El registro se ha eliminado correctamente','success':'ok',
				ResponseNC.data:''},status=status.HTTP_204_NO_CONTENT)
		except:
			return Response({ResponseNC.message:'Se presentaron errores al procesar la solicitud','success':'error',
			ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)	

class RegionViewSet(viewsets.ModelViewSet):
    """
	Retorna una lista de Reggiones, puede utilizar el parametro (dato) a traver del cual, se podra buscar por todo o parte del nombre, tambien puede buscar las regiones que hacen parte de determinado pais.
    """
    model=Region
    queryset = model.objects.all()
    serializer_class = RegionSerializer

    def retrieve(self,request,*args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({ResponseNC.message:'',ResponseNC.status:'success',ResponseNC.data:serializer.data})
        except:
            return Response({ResponseNC.message:'No se encontraron datos','success':'fail',ResponseNC.data:''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = super(RegionViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)
            id_pais = self.request.query_params.get('id_pais', None)

            if dato or id_pais:
                if dato:
                    qset = (Q(nombre__icontains=dato))
                if id_pais:
                    if dato:
                        qset=qset&(Q(pais_id=id_pais))
                    else:
                        qset=(Q(pais_id=id_pais))

                queryset = self.model.objects.filter(qset)
            #utilizar la variable ignorePagination para quitar la paginacion
            ignorePagination= self.request.query_params.get('ignorePagination',None)
            if ignorePagination is None:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page,many=True)	
                    return self.get_paginated_response({ResponseNC.message:'','success':'ok',
                    ResponseNC.data:serializer.data})

            serializer = self.get_serializer(queryset,many=True)
            return Response({ResponseNC.message:'','success':'ok',ResponseNC.data:serializer.data})
        except:
            return Response({ResponseNC.message:'Se presentaron errores de comunicacion con el servidor',ResponseNC.status:'error',ResponseNC.data:''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                serializer = RegionSerializer(data=request.DATA,context={'request': request})

                if serializer.is_valid():
                    serializer.save(pais_id=request.DATA['pais_id'])
                    return Response({ResponseNC.message:'El registro ha sido guardado exitosamente','success':'ok',
                    ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({ResponseNC.message:'datos requeridos no fueron recibidos','success':'fail',
                    ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({ResponseNC.message:'Se presentaron errores al procesar los datos','success':'error',
                ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,*args,**kwargs):
        if request.method == 'PUT':
            try:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = RegionSerializer(instance,data=request.DATA,context={'request': request},partial=partial)
                if serializer.is_valid():
                    self.perform_update(serializer)
                    return Response({ResponseNC.message:'El registro ha sido actualizado exitosamente','success':'ok',
                    ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({ResponseNC.message:'datos requeridos no fueron recibidos','success':'fail',
                    ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({ResponseNC.message:'Se presentaron errores al procesar los datos','success':'error',
                ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,*args,**kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({ResponseNC.message:'El registro se ha eliminado correctamente','success':'ok',
            ResponseNC.data:''},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({ResponseNC.message:'Se presentaron errores al procesar la solicitud','success':'error',
            ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

class MunicipioViewSet(viewsets.ModelViewSet):
    """
    Retorna una lista de Municipios, puede utilizar el parametro (dato) a traver del cual, se podra buscar por todo o parte del nombre, tambien puede buscar los municipios que hacen parte de determinada region.
    """
    model=Municipio
    queryset = model.objects.all()
    serializer_class = MunicipioSerializer

    def retrieve(self,request,*args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({ResponseNC.message:'',ResponseNC.status:'success',ResponseNC.data:serializer.data})
        except:
            return Response({ResponseNC.message:'No se encontraron datos','success':'fail',ResponseNC.data:''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = super(MunicipioViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)
            id_region= self.request.query_params.get('id_region', None)

            if dato or id_region:
                if dato:
                    qset = (Q(nombre__icontains=dato))
                if id_region:
                    if dato:
                        qset=qset&(Q(region_id=id_region))
                    else:
                        qset=(Q(region_id=id_region))

                queryset = self.model.objects.filter(qset)
            #utilizar la variable ignorePagination para quitar la paginacion
            ignorePagination= self.request.query_params.get('ignorePagination',None)
            if ignorePagination is None:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page,many=True)	
                    return self.get_paginated_response({ResponseNC.message:'','success':'ok',
                    ResponseNC.data:serializer.data})

            serializer = self.get_serializer(queryset,many=True)
            return Response({ResponseNC.message:'','success':'ok',
            ResponseNC.data:serializer.data})
        except:
            return Response({ResponseNC.message:'Se presentaron errores de comunicacion con el servidor',ResponseNC.status:'error',ResponseNC.data:''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                serializer = MunicipioSerializer(data=request.DATA,context={'request': request})

                if serializer.is_valid():
                    serializer.save(region_id=request.DATA['region_id'])
                    return Response({ResponseNC.message:'El registro ha sido guardado exitosamente','success':'ok',
                    ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({ResponseNC.message:'datos requeridos no fueron recibidos','success':'fail',
                    ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({ResponseNC.message:'Se presentaron errores al procesar los datos','success':'error',
                ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,*args,**kwargs):
        if request.method == 'PUT':
            try:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = MunicipioSerializer(instance,data=request.DATA,context={'request': request},partial=partial)
                if serializer.is_valid():
                    self.perform_update(serializer)
                    return Response({ResponseNC.message:'El registro ha sido actualizado exitosamente','success':'ok',
                    ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({ResponseNC.message:'datos requeridos no fueron recibidos','success':'fail',
                    ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({ResponseNC.message:'Se presentaron errores al procesar los datos','success':'error',
                ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,*args,**kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({ResponseNC.message:'El registro se ha eliminado correctamente','success':'ok',
            ResponseNC.data:''},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({ResponseNC.message:'Se presentaron errores al procesar la solicitud','success':'error',
            ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
#Fin api rest para municipio

class CargoViewSet(viewsets.ModelViewSet):
    """
    Retorna una lista de Cargos, puede utilizar el parametro (dato) a traver del cual, se podra buscar por todo o parte del nombre, tambien puede buscar por medio de la empresa de cual pertenece dicho cargo.
    """
    model= Cargo
	#model_log=Logs
	#model_acciones=Acciones
    nombre_modulo='parametrizacion.cargo'
    queryset = model.objects.all()
    serializer_class = CargoSerializer

    def retrieve(self,request,*args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'message':'','status':'success','data':serializer.data})
        except:
            return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        try:
            paginacion = self.request.query_params.get('sin_paginacion', None)

            queryset = super(CargoViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)
            empresa_filtro=self.request.query_params.get('empresa_filtro', None)
            if empresa_filtro:
                empresa_id = empresa_filtro
                qset=(Q(empresa_id=empresa_id))
            else:
                empresa_id = self.request.query_params.get('empresa_id', request.user.usuario.empresa.id)
                qset=(Q(empresa=empresa_id))

            if dato:
                qset = qset & (Q(nombre__icontains=dato))

            queryset = self.model.objects.filter(qset)

            if paginacion==None:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page,many=True)	
                    return self.get_paginated_response({'message':'','success':'ok',
                    'data':serializer.data})

                serializer = self.get_serializer(queryset,many=True)
                return Response({'message':'','success':'ok','data':serializer.data})
            else:
                serializer = self.get_serializer(queryset,many=True)
                return Response({'message':'','success':'ok','data':serializer.data})
        except:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Fin Api rest para Cargo