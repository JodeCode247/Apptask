
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,serializers
from mytask.models import MyUsers,UserProfile,UserAppDownload,AdminApps
from .serializer import UserSerializer
from django.http import HttpResponseNotFound,Http404

@api_view(['GET'])
def get_users(request):
    users = MyUsers.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user(request,pk):
    try:
        user = MyUsers.objects.get(id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except:
        raise Http404
        #return HttpResponseNotFound('ERROR, USER NOT FOUND')

def get_user_info():
    pass