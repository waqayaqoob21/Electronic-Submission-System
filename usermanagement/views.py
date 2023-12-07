from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from usermanagement.userController import *
from rest_framework_simplejwt.views import TokenObtainPairView
from usermanagement.serializer import MyTokenObtainPairSerializer

# Create your views here.

user_obj = UserController()


class SignUpUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = user_obj.signUpUser(request.data)
        return result


class UserLoginApiView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user_data = {'id': serializer.user.id, 'username': serializer.user.username,
                             'email': serializer.user.email, 'first_name': serializer.user.first_name,
                             'last_name': serializer.user.last_name, 'is_superuser': serializer.user.is_superuser
                             }
                return JsonResponse(
                    {'message': "Login Successfully", 'Token': serializer.validated_data,
                     'data': user_data}, status=200)

            else:
                return JsonResponse({'message': "Invalid username or password"}, status=401)
        except Exception as e:
            return JsonResponse({'message': 'Internal Server Error.'}, status=500)
