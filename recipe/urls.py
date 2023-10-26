from django.urls import include, path
from rest_framework import routers
from .views import RecipeView, RegisterView, LoginView, LogoutView

#
router = routers.DefaultRouter()
router.register('', RecipeView)
urlpatterns = [
    path('recipe/', include(router.urls)),
    path("user/register/", RegisterView.as_view(), name='register'),
    path("user/login/", LoginView.as_view(), name='login'),
    path("user/logout/", LogoutView.as_view(), name='logout'),
]
