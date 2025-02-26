from rest_framework import serializers
from .models import AuthCredential

class AuthCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthCredential
        fields = '__all__'