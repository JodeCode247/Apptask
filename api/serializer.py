from rest_framework import serializers
from mytask.models import MyUsers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUsers
        fields = ['id','username','email','user_type',]
        #exclude = ['is_superuser','is_active']
        