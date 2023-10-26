from django.contrib.auth import authenticate, logout, login, get_user_model
from django.contrib.auth.models import User
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer, UserSerializer


class RecipeView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
            )
            # Use set_password to securely hash the password
            user.set_password(serializer.validated_data['password'])
            user.save()
            # user = User.objects.create(username="username", email="email", password="password")
            # user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        response_data = {
            "message": "This is the user registration endpoint. Use a POST request to register a new user."
        }
        return Response(response_data, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return Response(UserSerializer(user).data)

        return Response({"Error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        response_data = {
            "message": "This is the user login endpoint. Use a POST request to login."
        }
        return Response(response_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
