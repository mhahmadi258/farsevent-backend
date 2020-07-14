from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validators
from django.core import exceptions

from .models import City

User = get_user_model()

class UserCreationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'token',
            'username',
            'email',
            'phone',
            'password',
            'first_name',
            'last_name',
        )
        extra_kwargs = {
            'phone':{'write_only':True},
            'password':{'write_only':True},
            'first_name':{'write_only':True},
            'last_name':{'write_only':True},
        }

    def create(self,validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        token = Token.objects.create(user =user)
        validated_data['token'] = token
        return validated_data

    def validate(self, attrs):
        user = User(**attrs)

        password = attrs.get('password')
        errors = dict()

        try:
            validators.validate_password(password=password,user = user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
             raise serializers.ValidationError(errors)
        
        return super().validate(attrs)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id',
            'name'
        )