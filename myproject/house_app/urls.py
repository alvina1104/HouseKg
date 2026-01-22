from django.urls import path, include
from .views import (UserProfileViewSet, RegionViewSet, CityViewSet, DistrictViewSet,
                    PropertyViewSet, PropertyImageViewSet, ReviewViewSet)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'cities', CityViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'property_image', PropertyImageViewSet)
router.register(r'reviews', ReviewViewSet)


urlpatterns = [
    path('', include(router.urls)),
]