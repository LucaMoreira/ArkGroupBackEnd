from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.response import Response
from beta.models import User
from beta.decorators import check_auth
from .models import Medcine, Choice, CONSUMPTION_CHOICES
from rest_framework import status
from .serializers import MedcineSerializer
from django.conf import settings


HEADERS : dict = {
    "Access-Control-Allow-Origin": settings.FRONTEND_URL,
    "Access-Control-Allow-Methods": "POST, PUT, PATCH, GET, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Origin, X-Api-Key, X-Requested-With, Content-Type, Accept, Authorization"
    }
SUCCESS : int  = status.HTTP_200_OK
ERROR   : int  = status.HTTP_400_BAD_REQUEST


@api_view(["POST"])
@check_auth(['Client'])
def get_meds(request):
    try:
        username   = request.data['user']
        medcines   = Medcine.objects.filter(owner=username) if Medcine.objects.filter(owner=username).exists() else {}
        data       = {
            "meds": MedcineSerializer(medcines, many=True).data
        }
        return Response(data, status=SUCCESS, headers=HEADERS)

    except Exception as e:
        return Response(status=ERROR, headers=HEADERS)


@api_view(["POST"])
@check_auth(['Client'])
def create_med(request):
    try:
        username        = request.data['user']
        name            = request.data['name']
        consumption     = request.data['consumption']
        amount_consumed = request.data['amount_consumed']
        initial_amount  = request.data['initial_amount']
        purchase_date   = request.data['purchase_date']
        owner           = User.objects.get(username=username)
        medcine         = Medcine.objects.create(name=name, amount_consumed=amount_consumed, initial_amount=initial_amount, purchase_date=purchase_date, owner=owner)
        for day in consumption:
            day_name = CONSUMPTION_CHOICES[day-1][0]
            choice   = Choice.objects.get(choice=day_name)
            medcine.consumption.add(choice)
        medcine.save()

        return Response(status=SUCCESS, headers=HEADERS)
    except Exception as e:
        return Response(status=ERROR, headers=HEADERS)


@api_view(["POST"])
@check_auth(['Client'])
def update_med(request):
    try:
        id                      = request.data['id']
        username                = request.data['user']
        name                    = request.data['name']
        consumption             = request.data['consumption']
        initial_amount          = request.data['initial_amount']
        purchase_date           = request.data['purchase_date']
        owner                   = User.objects.get(username=username)
        medcine                 = Medcine.objects.get(id=id)
        for day in consumption:
            day_name = CONSUMPTION_CHOICES[day-1][0]
            choice   = Choice.objects.get(choice=day_name)
            medcine.consumption.add(choice)
        medcine.initial_amount  = initial_amount
        medcine.purchase_date   = purchase_date
        medcine.save()

        return Response(status=SUCCESS, headers=HEADERS)
    
    except Exception as e:
        return Response(status=ERROR, headers=HEADERS)


@api_view(["POST"])
@check_auth(['Client'])
def delete_med(request):
    try:
        id       = request.data['id']
        username = request.data['user']
        owner    = User.objects.get(username=username)
        medicine = Medcine.objects.get(id=id, owner=owner)
        medicine.delete()
        
        return Response(status=SUCCESS, headers=HEADERS)
    
    except Exception as e:
        return Response(status=ERROR, headers=HEADERS)