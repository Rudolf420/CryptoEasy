# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class PersonalInfo(models.Model):
    user = models.IntegerField(blank=True, null=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    card_id = models.CharField(unique=True, max_length=255)
    street = models.CharField(max_length=255)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=255)
    photo = models.BinaryField(blank=True, null=True)
    debet_card_number = models.CharField(max_length=16)
    created_at = models.DateTimeField()
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Personal_info'


class User(models.Model):
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    last_login = models.DateTimeField()
    token = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'User'


class Wallet(models.Model):
    user = models.IntegerField(blank=True, null=True)
    eur_balance = models.FloatField(blank=True, null=True)
    bitcoin_balance = models.FloatField(blank=True, null=True)
    ethereum_balance = models.FloatField(blank=True, null=True)
    cardano_balance = models.FloatField(blank=True, null=True)
    litecoin_balance = models.FloatField(blank=True, null=True)
    polkadot_balance = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField()
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Wallet'
