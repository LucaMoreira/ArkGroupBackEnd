from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.response import Response
from beta.models import User
from beta.decorators import check_auth
from .models import Medcine, Choice
from rest_framework import status
from .serializers import MedcineSerializer


HEADERS : dict = {
    "Access-Control-Allow-Origin": "http://localhost:3000",
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
        purchase_date   = purchase_date.split('/')[2] + '-' + purchase_date.split('/')[1] + '-' + purchase_date.split('/')[0]
        medcine         = Medcine.objects.create(name=name, amount_consumed=amount_consumed, initial_amount=initial_amount, purchase_date=purchase_date, owner=owner)
        consumption     = Choice(choice=consumption)
        medcine.consumption.add(consumption.id)
        medcine.save()

        return Response(status=SUCCESS, headers=HEADERS)
    
    except Exception as e:
        return Response(status=ERROR, headers=HEADERS)


@api_view(["POST"])
@check_auth(['Client'])
def update_med(request):
    try:
        username                = request.data['user']
        name                    = request.data['name']
        consumption             = request.data['consumption']
        amount_consumed         = request.data['amount_consumed']
        initial_amount          = request.data['initial_amount']
        purchase_date           = request.data['purchase_date']
        owner                   = User.objects.get(username=username)
        purchase_date           = purchase_date.split('/')[2] + '-' + purchase_date.split('/')[1] + '-' + purchase_date.split('/')[0]
        medcine                 = Medcine.objects.get(name=name, owner=owner)
        consumption             = Choice(choice=consumption)
        medcine.name            = username
        medcine.consumption.add(consumption.id)
        medcine.amount_consumed = amount_consumed
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