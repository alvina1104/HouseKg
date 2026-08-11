from pyexpat import features
from rest_framework import viewsets, generics, permissions, status, views
from .serializers import (UserProfileListSerializer, UserProfileDetailSerializer,
                          RegionListSerializer, RegionDetailSerializer,
                          CityListSerializer, CityDetailSerializer,
                          DistrictListSerializer, DistrictDetailSerializer,
                          PropertyListSerializer, PropertyDetailSerializer, PropertyCreateSerializer,
                          ReviewCreateSerializer, UserRegisterSerializer, UserLoginSerializer, HousePredictSerializer)
from .models import (UserProfile, Region, City, District, Property,Review)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PropertyFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from .pagination import PropertyPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import CheckPropertyPermission, CheckReviewPermission
import joblib
from django.conf import settings
import os

neighborhood = ['Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr',
            'Crawfor', 'Edwards', 'Gilbert', 'IDOTRR', 'MeadowV',
            'Mitchel', 'NAmes', 'NPkVill', 'NWAmes', 'NoRidge',
            'NridgHt', 'OldTown', 'SWISU', 'Sawyer', 'SawyerW',
            'Somerst', 'StoneBr', 'Timber', 'Veenker']


model_path = os.path.join(settings.BASE_DIR, 'model.pkl')
model = joblib.load(model_path)

scaler_path = os.path.join(settings.BASE_DIR, 'scaler.pkl')
scaler = joblib.load(scaler_path)


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

class UserProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer

class RegionListAPIView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionListSerializer

class RegionDetailAPIView(generics.RetrieveAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionDetailSerializer

class CityListAPIView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializer

class CityDetailAPIView(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailSerializer

class DistrictListAPIView(generics.ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictListSerializer

class DistrictDetailAPIView(generics.RetrieveAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictDetailSerializer

class PropertyListAPIView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyListSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['region_name','city_name','district_name']
    ordering_fields =['price','created_date','area']
    pagination_class = PropertyPagination

class PropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer

class PropertyCreateAPIView(generics.CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyCreateSerializer
    permission_classes = [CheckPropertyPermission]


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [CheckReviewPermission]


class PredictPrice(views.APIView):

    def post(self,request):
        instance = HousePredictSerializer(data=request.data)
        if instance.is_valid():
            data = instance.validated_data
            new_neighborhood = data.get('Neighborhood')
            neighborhood1_0 = [1 if new_neighborhood == i else 0 for i in neighborhood]



            features = [
                        data['GrLivArea'],
                        data['YearBuilt'],
                        data['GarageCars'],
                        data['TotalBsmtSF'],
                        data['FullBath'],
                        data['OverallQual'],
                        ] + neighborhood1_0

            scaled_data = scaler.transform([features])
            pred = model.predict(scaled_data)[0]
            house = instance.save(predict_price=round(pred))


            return Response({'Price Predict': round(pred),
                             'data': HousePredictSerializer(house).data}, status=status.HTTP_200_OK)
        return Response(instance.errors, status=status.HTTP_400_BAD_REQUEST)
