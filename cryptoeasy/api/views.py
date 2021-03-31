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
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
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
    api_call()
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

@csrf_exempt
def deposit(request):
    if request.method == 'PUT':
        json = BytesIO(request.body)
        data = JSONParser().parse(json)
        result = token_auth(data['token'])

        if result == False:
            return JsonResponse({'response':'No permission'})

        else:
            try:
                wallet = Wallet.objects.get(user=result)
            except Wallet.DoesNotExist:
                return JsonResponse({'response':'wallet doesnt exist'})

            wallet.eur_balance = data['amount']
            wallet.save()

            return JsonResponse({'response':'Deposit added'})

    else:
        return JsonResponse({'response':'wrong request'})

@csrf_exempt
def buy(request):
    if request.method == 'PUT':
        json = BytesIO(request.body)
        data = JSONParser().parse(json)
        result = token_auth(data['token'])

        if result == False:
            return JsonResponse({'response':'No permission'})

        else:
            try:
                wallet = Wallet.objects.get(user=result)
            except Wallet.DoesNotExist:
                return JsonResponse({'response':'wallet doesnt exist'})

            if data['cryptocurrency'] == 'BTC':
                price = api_call('1')
            elif data['cryptocurrency'] == 'ETH':
                price = api_call('2')
            elif data['cryptocurrency'] == 'DOT':
                price = api_call('5')
            elif data['cryptocurrency'] == 'ADA':
                price = api_call('4')
            elif data['cryptocurrency'] == 'LTC':
                price = api_call('7')

            if wallet.eur_balance >= float(data['amount'])*price and data['cryptocurrency'] == 'BTC':
                wallet.bitcoin_balance =  wallet.bitcoin_balance + float(data['amount'])

            elif wallet.eur_balance >= float(data['amount'])*price and data['cryptocurrency'] == 'ETH':
                wallet.ethereum_balance = wallet.ethereum_balance + float(data['amount'])

            elif  wallet.eur_balance >= float(data['amount'])*price and data['cryptocurrency'] == 'DOT':
                wallet.polkadot_balance = wallet.polkadot_balance + float(data['amount'])

            elif  wallet.eur_balance >= float(data['amount'])*price and data['cryptocurrency'] == 'ADA':
                wallet.cardano_balance = wallet.cardano_balance + float(data['amount'])

            elif  wallet.eur_balance >= float(data['amount'])*price and data['cryptocurrency'] == 'LTC':
                wallet.litecoin_balance = wallet.litecoin_balance + float(data['amount'])

            else:
                return JsonResponse({'response': 'Not enough money'})

            wallet.eur_balance = float(wallet.eur_balance) - float(data['amount'])*price
            wallet.save()

            return JsonResponse({'response':'Cryptocurrency added'})

    else:
        return JsonResponse({'response':'wrong request'})


@csrf_exempt
def sell(request):
    if request.method == 'PUT':
        json = BytesIO(request.body)
        data = JSONParser().parse(json)
        result = token_auth(data['token'])

        if result == False:
            return JsonResponse({'response':'No permission'})

        else:
            try:
                wallet = Wallet.objects.get(user=result)
            except Wallet.DoesNotExist:
                return JsonResponse({'response':'wallet doesnt exist'})

            if data['cryptocurrency'] == 'BTC':
                price = api_call('1')
            elif data['cryptocurrency'] == 'ETH':
                price = api_call('2')
            elif data['cryptocurrency'] == 'DOT':
                price = api_call('5')
            elif data['cryptocurrency'] == 'ADA':
                price = api_call('4')
            elif data['cryptocurrency'] == 'LTC':
                price = api_call('7')

            if wallet.bitcoin_balance >= float(data['amount']) and data['cryptocurrency'] == 'BTC':
                wallet.bitcoin_balance = wallet.bitcoin_balance - float(data['amount'])
                wallet.eur_balance =  wallet.eur_balance + float(data['amount'])*price

            elif wallet.ethereum_balance >= float(data['amount']) and data['cryptocurrency'] == 'ETH':
                wallet.ethereum_balance = wallet.ethereum_balance - float(data['amount'])
                wallet.eur_balance = wallet.eur_balance + float(data['amount']) * price

            elif wallet.polkadot_balance >= float(data['amount']) and data['cryptocurrency'] == 'DOT':
                wallet.polkadot_balance = wallet.polkadot_balance - float(data['amount'])
                wallet.eur_balance = wallet.eur_balance + float(data['amount']) * price

            elif wallet.cardano_balance >= float(data['amount']) and data['cryptocurrency'] == 'ADA':
                wallet.cardano_balance = wallet.cardano_balance - float(data['amount'])
                wallet.eur_balance =  wallet.eur_balance + float(data['amount']) * price

            elif wallet.litecoin_balance >= float(data['amount']) and data['cryptocurrency'] == 'LTC':
                wallet.litecoin_balance = wallet.litecoin_balance - float(data['amount'])
                wallet.eur_balance = wallet.eur_balance + float(data['amount']) * price

            else:
                return JsonResponse({'response': 'Not enough crypto'})

            wallet.save()

            return JsonResponse({'response':'Cryptocurrency selled'})

    else:
        return JsonResponse({'response':'Wrong request'})

@csrf_exempt
def info(request):
    if request.method == 'POST':
        json = BytesIO(request.body)
        data = JSONParser().parse(json)
        result = token_auth(data['token'])

        if result == False:
            return JsonResponse({'response':'No permission'})

        else:
            try:
                user = User.objects.get(id=result)
            except User.DoesNotExist:
                return JsonResponse({'response':'User doesnt exist'})
            try:
                wallet = Wallet.objects.get(user=result)
            except Wallet.DoesNotExist:
                return JsonResponse({'response':'Wallet doesnt exist'})
            try:
                personal_info = PersonalInfo.objects.get(user=result)
            except PersonalInfo.DoesNotExist:
                return JsonResponse({'response':'PersonalInfo doesnt exist'})


            return JsonResponse({'User':UserSerializer(user).data, 'PersonalInfo':PersonalInfoSerializer(personal_info).data,'Wallet':WalletSerializer(wallet).data})


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

def token_auth(token):
    try:
        user = User.objects.get(token=token)
    except User.DoesNotExist:
        user = None

    if user != None:
        return user.id

    else:
        return False

def api_call(id):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    parameters = {
        'start': id,
        'limit': id,
        'convert': 'EUR'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '89491b09-0f1e-4585-80cf-a13097fdc682',
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data'][0]['quote']['EUR']['price']

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
