from django.urls import path, include
from .views import (UserProfileListAPIView,UserProfileDetailAPIView, RegionListAPIView,RegionDetailAPIView,
                    CityListAPIView,CityDetailAPIView, DistrictListAPIView,DistrictDetailAPIView,
                    PropertyListAPIView,PropertyDetailAPIView, ReviewCreateAPIView,
                    RegisterView, LoginView, LogoutView, PropertyCreateAPIView)
from rest_framework import routers

router = routers.SimpleRouter()



urlpatterns = [
    path('', include(router.urls)),
    path('region/', RegionListAPIView.as_view(),name='region_list'),
    path('region/<int:pk>/', RegionDetailAPIView.as_view(),name='region_detail'),
    path('city/', CityListAPIView.as_view(),name='city_list'),
    path('city/<int:pk>/', CityDetailAPIView.as_view(),name='city_detail'),
    path('district/', DistrictListAPIView.as_view(),name='district'),
    path('district/<int:pk>/', DistrictDetailAPIView.as_view(),name='district_detail'),
    path('property/', PropertyListAPIView.as_view(),name='property_list'),
    path('property/<int:pk>/', PropertyDetailAPIView.as_view(),name='property_detail'),
    path('user/', UserProfileListAPIView.as_view(),name='user_list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(),name='user_detail'),
    path('review/', ReviewCreateAPIView.as_view(),name='reviews'),
    path('register/', RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('property_create/', PropertyCreateAPIView.as_view(),name='property_create'),
]