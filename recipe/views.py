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

    def list(self, request, *args, **kwargs):
        pk = self.request.user.pk

        queryset = Recipe.objects.filter(user=pk)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()
        mutable_data['user'] = request.user.pk

        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            recipe = Recipe.objects.get(pk=pk)

            if recipe.user == request.user:
                serializer = self.get_serializer(recipe)
                return Response(serializer.data)
            else:
                return Response({"detail": "Recipe does not belong to the currently logged-in user."})

        except:
            return Response({"detail": "Recipe not found."})



class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
            )
            user.set_password(serializer.validated_data['password'])
            user.save()
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
