from .models import (UserProfile, Region,
                     City, District, Property, PropertyImage, Review, House)
from rest_framework import serializers, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .permissions import CheckReviewPermission


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'date_register')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','first_name','last_name','user_image','role']

class UserProfileDetailSerializer(serializers.ModelSerializer):
    date_register = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = UserProfile
        fields = ['first_name','last_name','username','email','age',
                  'phone_number','user_image','role','date_register',]

class UserProfileReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']

class UserProfilePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_image','first_name','last_name','date_register']

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['property_image']

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating']

class ReviewPropertySerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y')
    class Meta:
        model = Review
        fields = ['author','comment','rating','created_date']

class PropertyListSerializer(serializers.ModelSerializer):
    district = serializers.StringRelatedField()
    property_images = PropertyImageSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    created_date = serializers.DateField(format='%d-%m-%Y')
    get_avg_rating = serializers.SerializerMethodField()
    get_count_person = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = ['id','property_images','title','property_type','district','price','address',
                  'description','reviews','get_avg_rating','get_count_person','created_date']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_person(self, obj):
        return obj.get_count_person()

class PropertyDetailSerializer(serializers.ModelSerializer):
    district = serializers.StringRelatedField()
    property_images = PropertyImageSerializer(many=True)
    reviews = ReviewPropertySerializer(many=True)
    created_date = serializers.DateField(format='%d-%m-%Y')
    get_avg_rating = serializers.SerializerMethodField()
    get_count_person = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = ['seller','property_images','title','district','address',
                  'description','price','area','rooms','property_type','region','floor','total_floor',
                  'documents','condition','created_date','get_avg_rating','get_count_person','reviews']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_person(self, obj):
        return obj.get_count_person()


class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'



class DistrictListSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id','district_name']

class DistrictDetailSerializer(serializers.ModelSerializer):
    properties = PropertyListSerializer(many=True)
    class Meta:
        model = District
        fields = ['id','district_name','properties']


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','city_name',]

class CityDetailSerializer(serializers.ModelSerializer):
    properties = PropertyListSerializer(many=True)
    class Meta:
        model = City
        fields = ['id','city_name','properties']

class RegionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id','region_name']

class RegionDetailSerializer(serializers.ModelSerializer):
    properties = PropertyListSerializer(many=True)
    class Meta:
        model = Region
        fields = ['id','region_name','properties']


class HousePredictSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'
