import binascii
import os

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.crypto import get_random_string
from io import BytesIO
from rest_framework.parsers import JSONParser
from .models import User, PersonalInfo, Wallet
from .serializers import UserSerializer, PersonalInfoSerializer
import requests
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.utils import timezone

# Create your views here.

@csrf_exempt
def register(request):

    if request.method == 'POST':

        json = BytesIO(request.body)
        data = JSONParser().parse(json)
        data.update({'created_at': datetime.datetime.now(tz=timezone.utc), 'last_update': datetime.datetime.now(tz=timezone.utc), 'last_login': datetime.datetime.now(tz=timezone.utc), 'token':generate_key()})
        user = UserSerializer(data=data)
        personal_info = PersonalInfoSerializer(data=data)


        if user.is_valid() and personal_info.is_valid():

            if user_exists(data["email"]):
                response = {'Failed': 'email is already used'}
                return JsonResponse(response)

            elif card_exists(data["card_id"]):
                response = {'Failed': 'card id is already used'}
                return JsonResponse(response)

            else:
                user.save()
                print(personal_info.data)
                personal_info = PersonalInfoSerializer(personal_info, {'user':10}, partial=True)
                personal_info.is_valid()
                personal_info.save()



        return JsonResponse(personal_info.errors)


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