from django.forms import widgets
from rest_framework import serializers
from .models import User, PersonalInfo, Wallet, Cryptodetail
import datetime
from django.utils import timezone

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
    photo = serializers.CharField(required=False)
    city = serializers.CharField(max_length=255)
    debet_card_number = serializers.CharField(max_length=16)
    created_at = serializers.DateTimeField(required=False)
    last_update = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return PersonalInfo.objects.create(**validated_data)

    def update(self, instance, attrs):
        instance.user = attrs.get('user', instance.user)
        instance.firstname = attrs.get('firstname', instance.firstname)
        instance.lastname = attrs.get('lastname', instance.lastname)
        instance.card_id = attrs.get('card_if', instance.card_id)
        instance.street = attrs.get('street', instance.street)
        instance.postal_code = attrs.get('postal_code', instance.postal_code)
        instance.city = attrs.get('city', instance.city)
        instance.photo = attrs.get('photo', instance.photo)
        instance.debet_card_number = attrs.get('debet_card_number', instance.debet_card_number)
        instance.created_at = attrs.get('created_at', instance.created_at)
        instance.last_update = datetime.datetime.now(tz=timezone.utc)
        instance.save()
        return instance

    class Meta:
        model = PersonalInfo
        fields = '__all__'


class WalletSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    eur_balance = serializers.FloatField()
    bitcoin_balance = serializers.FloatField()
    ethereum_balance = serializers.FloatField()
    cardano_balance = serializers.FloatField()
    litecoin_balance = serializers.FloatField()
    polkadot_balance = serializers.FloatField()
    created_at = serializers.DateTimeField()
    last_update = serializers.DateTimeField()

    def create(self, validated_data):
        return Wallet.objects.create(**validated_data)

    def restore_object(self, attrs, instance=None):

        if instance is not None:
            instance.user = attrs.get('user', instance.user)
            instance.eur_balance = attrs.get('eur_balance', instance.eur_balance)
            instance.bitcoin_balance = attrs.get('bitcoin_balance', instance.bitcoin_balance)
            instance.ethereum_balance = attrs.get('ethereum_balance', instance.ethereum_balance)
            instance.cardano_balance = attrs.get('cardano_balance', instance.cardano_balance)
            instance.litecoin_balance = attrs.get('litecoin_balance',instance.litecoin_balance)
            instance.polkadot_balance = attrs.get('polkadot_balance',instance.polkadot_balance)
            instance.created_at = attrs.get('created_at',instance.created_at)
            instance.last_update = datetime.datetime.now(tz=timezone.utc)
            return instance

        return User(**attrs)

class CryptodetailSerializer(serializers.Serializer):
    api_response = serializers.JSONField()
    last_update = serializers.DateTimeField()

    def create(self, validated_data):
        return Cryptodetail.objects.create(**validated_data)

    def restore_object(self, attrs, instance=None):

        if instance is not None:
            instance.api_response = attrs.get('api_response', instance.api_response)
            instance.last_update = attrs.get('last_update', instance.last_update)

            return instance

        return Cryptodetail(**attrs)