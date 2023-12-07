from django.http import JsonResponse
from usermanagement.serializer import *
from django.contrib.auth.hashers import make_password, check_password
from datetime import date
import random
from django.contrib.auth import authenticate, login

class UserController:
    @staticmethod
    def signUpUser(request):
        userModel = User()
        try:
            serializer = UserSerializer(data = request)
            if serializer.is_valid():
                user = User.objects.filter(email = request['email']).first()
                if user is None:
                    userModel.first_name = ""
                    userModel.last_name = ""
                    userModel.username = request['username']
                    userModel.email = request['email']
                    # userModel.password = request['password']
                    encryptedpassword = make_password(request['password'])
                    userModel.password = encryptedpassword
                    userModel.is_superuser = 'True'
                    userModel.last_login = date.today()
                    userModel.is_active = 'True'
                    userModel.is_staff = 'True'
                    userModel.save()
                    return JsonResponse({'message': 'User added successfully','success': True, 'status':201}, status=201)
                else:
                    return JsonResponse({'message': "A user with that email already exists.",'success': False, 'status':403}, status=403)
            else:
                return JsonResponse({'message': serializer.errors,'success': False, 'data': '', 'status':403}, status=403)
        except:
            return JsonResponse({'message': 'Login failed','success': False, 'data': '', 'status':500}, status=500)

