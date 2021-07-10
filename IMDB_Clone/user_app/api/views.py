import re
from django.http.response import HttpResponse
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.utils.serializer_helpers import ReturnDict
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

#from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def LogoutView(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status = status.HTTP_200_OK)

@api_view(['POST'])
def RegisterView(request):
    if request.method == "POST":

        serializer = RegisterSerializer(data=request.data)

        data ={}
    
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Registered Successfully !'
            data['username'] = account.username
            data['email'] =     account.email
            #token1 = Token.objects.get_or_create(user=account)
            token = Token.objects.get(user=account).key

            
            data['token'] = token
        else:
            data = serializer.errors
    return Response(data,status=status.HTTP_201_CREATED)