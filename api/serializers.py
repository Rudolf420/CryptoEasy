from django.forms import widgets
from rest_framework import serializers
from .models import User, PersonalInfo, Wallet

class UserSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(max_length=255,required=True)
    token = serializers.CharField(max_length=10,required=False)
    created_at = serializers.DateTimeField(required=False)
    last_login = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None:
            instance.email = attrs.get('email', instance.email)
            instance.password = attrs.get('password', instance.password)
            instance.token = attrs.get('token', instance.token)
            instance.created_at = attrs.get('created_at', instance.created_at)
            instance.last_login = attrs.get('last_login', instance.last_login)
            return instance

        return User(**attrs)

class PersonalInfoSerializer(serializers.Serializer):
    user = serializers.IntegerField(required=False)
    firstname = serializers.CharField(max_length=255)
    lastname = serializers.CharField(max_length=255)
    card_id = serializers.CharField(max_length=255)
    street = serializers.CharField(max_length=255)
    postal_code = serializers.IntegerField()
    city = serializers.CharField(max_length=255)
    debet_card_number = serializers.CharField(max_length=16)
    created_at = serializers.DateTimeField(required=False)
    last_update = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return PersonalInfo.objects.create(**validated_data)

    def update(self, instance, attrs):
        print(attrs)
        print(instance.data)
        instance.user = attrs.get('user', instance.user)
        return instance

