import binascii
import os

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.crypto import get_random_string
from io import BytesIO
from rest_framework.parsers import JSONParser
from .models import User, PersonalInfo, Wallet
from .serializers import UserSerializer, PersonalInfoSerializer, WalletSerializer
import requests
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.utils import timezone
from django.contrib.auth import authenticate

# Create your views here.

@csrf_exempt
def register(request):
    if request.method == 'POST':

        json = BytesIO(request.body)
        data = JSONParser().parse(json)
        data.update({'created_at': datetime.datetime.now(tz=timezone.utc), 'last_update': datetime.datetime.now(tz=timezone.utc), 'last_login': datetime.datetime.now(tz=timezone.utc), 'token':generate_key()})
        user = UserSerializer(data=data)

        if user.is_valid():

            if user_exists(data["email"]):
                response = {'Failed': 'email is already used'}
                return JsonResponse(response)

            elif card_exists(data["card_id"]):
                response = {'Failed': 'card id is already used'}
                return JsonResponse(response)

            else:
                user.save()
                data['user'] = int(User.objects.get(email=data['email']).id)
                personal_info = PersonalInfoSerializer(data=data)
                personal_info.is_valid()
                personal_info.save()
                data['eur_balance'], data['bitcoin_balance'],data['ethereum_balance'],data['cardano_balance'],data['litecoin_balance'], data['polkadot_balance'] = 0,0,0,0,0,0
                wallet = WalletSerializer(data=data)
                wallet.is_valid()
                wallet.save()
                return JsonResponse({'response':'Registered succesfuly'})


        return JsonResponse({'response':'wrong request'})

@csrf_exempt
def delete(request):
    if request.method == 'DELETE':
        json = BytesIO(request.body)
        data = JSONParser().parse(json)
        response = {}
        try:
            u = User.objects.get(token=data['token'])
            id = u.id
            p = PersonalInfo.objects.get(user=id)
            p.delete()
            w = Wallet.objects.get(user=id)
            w.delete()
            u.delete()
            response["response"] = "user deleted"

        except User.DoesNotExist:
            response["response"] = "user doesnt exist"


        return JsonResponse(response)

    else:
        return JsonResponse({'response':'wrong request'})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        json = BytesIO(request.body)
        data = JSONParser().parse(json)
        result = authentification(data['email'],data['password'])

        if result == True:
            return JsonResponse({"response":"Wrong email"})

        elif result == False:
            return JsonResponse({"response": "Wrong password"})

        else:
            return JsonResponse({"response": result})


    else:
        return JsonResponse({'response':'wrong request'})

def user_exists(email):
    if User.objects.filter(email=email).exists():
        return True

    return False

def card_exists(card_id):
    if PersonalInfo.objects.filter(card_id=card_id).exists():
        return True

    return False


def generate_key():
    key = get_random_string(10)
    while User.objects.filter(token=key).exists():
        key = get_random_string(10)

    return str(key)

def authentification(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None

    if user != None:
        print(user)
        if(user.password == password):
            token = generate_key()
            user.token = token
            user.save()
            return token

        else:
            return False

    else:
        return True

