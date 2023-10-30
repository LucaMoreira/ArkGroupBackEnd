from rest_framework import status
from rest_framework.test import APITestCase
from django.http import HttpResponse
from beta.models import User
from .models import Medcine, Choice, CONSUMPTION_CHOICES
import json

USER     : str = 'Luca'
EMAIL    : str = 'luca@example.com'
PASSWORD : str = 'senha'


class ApiTests(APITestCase):
    """
    Ensure all api routes are working correctly.
    """
    
    
    def setUp(self) -> None:
        """
        Ensure we can create and login with a user.
        """
        
        for choice in CONSUMPTION_CHOICES:
            Choice.objects.create(choice=choice[0])
        
        register_url   : str   = '/create_user/'
        register_data  : dict  = {
            "username" : USER,
            "email"    : EMAIL,
            "password1": PASSWORD,
            "password2": PASSWORD
        }
        register_response : HttpResponse = self.client.post(register_url, register_data, format='json')
        self.token        : str          = json.loads(register_response.content)['token']
        self.assertEqual(register_response.status_code, status.HTTP_200_OK, 'Register failed!')
        
        user          = User.objects.get(username=USER)
        user.is_staff = True
        user.save()
        
        login_url     : str  = '/login/'
        login_data    : dict = {
            'username': USER, 
            'password': PASSWORD
        }
        login_response : HttpResponse = self.client.post(login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK, 'Login failed!')


    def test_create_med(self) -> None:
        """
        Ensure we can create a medcine.
        """
        
        url  : str  = '/create-med/'
        data : dict = {
            'user'           : USER,
            'token'          : self.token,
            'name'           : 'Minesulida',
            'consumption'    : [1,2,3],
            'amount_consumed': '2',
            'initial_amount' : '60',
            'purchase_date'  : '2023-10-20'
        }
        response : HttpResponse = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Could not create medcine!')
        self.id = Medcine.objects.get(name='Minesulida').id
    
    
    def test_get_meds(self) -> None:
        """
        Ensure we can get all user medcines.
        """
        
        url  : str  = '/get-meds/'
        data : dict = {
            'user'  : USER,
            'token' : self.token,
        }
        response : HttpResponse = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Could not get all user medcines!')
    
    
    def test_update_med(self) -> None:
        """
        Ensure we can update a medcine.
        """
        self.test_create_med()
        url  : str  = '/update-med/'
        data : dict = {
            'user'           : USER,
            'token'          : self.token,
            'id'             : Medcine.objects.get(name='Minesulida').id,
            'name'           : 'Minesulida',
            'consumption'    : [1,2,3],
            'amount_consumed': '2',
            'initial_amount' : '60',
            'purchase_date'  : '2023-03-20'
        }
        response : HttpResponse = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Could not update medcine!')
    
    
    def test_delete_med(self) -> None:
        """
        Ensure we can delete a medcine.
        """
        self.test_create_med()
        url  : str  = '/delete-med/'
        data : dict = {
            'user'           : USER,
            'token'          : self.token,
            'id'             : Medcine.objects.get(name='Minesulida').id
        }
        response : HttpResponse = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Could not delete medcine!')