
from ast import Return
from multiprocessing import context
from django.shortcuts import render
from django.urls import is_valid_path
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from TODO.models import Todos
from TODO.serializers import TodoSerializer,RegistrationSerializer
from django.contrib.auth.models import User
from rest_framework import authentication,permissions

# Create your views here.

class TodoViews(ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Todos.objects.all()
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)

    # def create(self,request,*args, **kwargs):
    #     serializer=TodoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.error) 

    def create(self,request,*args, **kwargs):
        serializer=TodoSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)    

       

    def retrieve(self,request,*args, **kwargs):
        id=kwargs.get("pk")   
        qs=Todos.objects.get(id=id) 
        serializer=TodoSerializer(qs,many=False)
        return Response(data=serializer.data)

    def destroy(sef,request,*args, **kwargs):
        id=kwargs.get("pk")
        qs=Todos.objects.get(id=id).delete() 
        return Response(data="deleted")       

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Todos.objects.get(id=id)
        serializer=TodoSerializer(data=request.data,instanve=object)
        if serializer.is_valid:
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)    


class TodoModelViewset(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]



    serializer_class=TodoSerializer
    queryset=Todos.objects.all()
    def create(self,request,*args, **kwargs):
        serializer=TodoSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)    


    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     serializer=TodoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         Todos.objects.create(**serializer._validated_data,user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)


    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)
        
    

    # def list(self,request,*args, **kwargs):
    #      qs=Todos.objects.filter(data=request.User)
    #      serializer=TodoSerializer(qs,many=True)
    #      return Response(data=serializer.data)




    @action(methods=["GET"],detail=False)
    def Pending_todos(self,request,*args, **kwargs):
        qs=Todos.objects.filter(status=False,user=request.user)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)


    @action(methods=["GET"],detail=False)
    def completed_todos(self,request,*args, **kwargs):
        qs=Todos.objects.filter(status=True)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)


    @action(methods=["post"],detail=True)
    def mark_as_done(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        qs=Todos.objects.filter(status=True)
        object=Todos.objects.get(id=id)
        object.status=True
        object.save()
        serializer=TodoSerializer(object,many=False)
        return Response(data=serializer.data)

                                                                
class UserView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()


    # def create(self,request,*args, **kwargs):
    #     serializer=RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response (data=serializer.errors)    