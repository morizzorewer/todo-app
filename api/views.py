from django.shortcuts import render
from api.serializers import UserSerializer,TodoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework import authentication,permissions
from reminder.models import Todos
from rest_framework import serializers



# Create your views here.
class SignUpView(APIView):
    def post(self,request,*args,**kwargs):
        serializers=UserSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data)
        
        else:
            return Response(data=serializers.errors)

class TodosView(ViewSet)  :
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):
        qs=Todos.objects.filter(user=request.user)
        serializers=TodoSerializer(qs,many=True)
        return Response(data=serializers.data)
    
    def create(self,request,*args,**kwargs):
        serializers=TodoSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(user=request.user)
            return Response(data=serializers.data)      
        else:
            return Response(data=serializers.errors)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todos.objects.get(id=id)
        serializers=TodoSerializer(qs)
        return Response(data=serializers.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todos.objects.get(id=id)
        if qs.user==request.user:
            qs.delete()
        else:  
           raise serializers.ValidationError("permision denied")
        return Response(data={"message":"deleted"})
    
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todos.objects.get(id=id)
        serializers=TodoSerializer(data=request.data,instance=todo_object)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data)
        else:
            return Response(data=serializers.errors)


class TodoViewSetView(ModelViewSet):
    queryset=Todos.objects.all()
    serializer_class=TodoSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classesermission=[permissions.IsAuthenticated]
    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
        