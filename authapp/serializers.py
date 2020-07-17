from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validators
from django.contrib.auth import authenticate
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
            'image',
            'password',
            'first_name',
            'last_name',
        )
        extra_kwargs = {
            'phone': {'write_only': True},
            'password': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'image': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        token = Token.objects.create(user=user)
        validated_data['token'] = token
        return validated_data

    def validate(self, attrs):
        user = User(**attrs)

        password = attrs.get('password')
        errors = dict()

        try:
            validators.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField(read_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'phone',
            'image',
            'password',
            'new_password',
            'first_name',
            'last_name',
            'birth_date',
            'city',
            'city_name',
            'address',
        )
        extra_kwargs = {
            'username': {'read_only': True},
            'email': {'read_only': True},
            'password': {'write_only': True},
            'city': {'write_only': True},
        }

    def get_city_name(self, obj):
        if obj.city:
            return obj.city.name
        else:
            return ''

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        new_password = validated_data.pop('new_password')
        user = self.context['request'].user
        if not authenticate(username=user.username, password=password):
            raise serializers.ValidationError(
                {'password': ['wrong current password']})
        else:
            user.set_password(new_password)
            user.save()
        return super().update(instance, validated_data)

    def validate(self, attrs):
        user = self.context['request'].user

        password = attrs.get('password')
        new_password = attrs.get('new_password')

        if (password and not new_password) or (not password and new_password):
            raise serializers.ValidationError(
                {'none_field': ['fill both password and new password']})

        errors = dict()

        try:
            validators.validate_password(password=new_password, user=user)
        except exceptions.ValidationError as e:
            errors['new_password'] = list(e.messages)

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