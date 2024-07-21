from rest_framework import serializers
from .models import User

#serializers.py
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'