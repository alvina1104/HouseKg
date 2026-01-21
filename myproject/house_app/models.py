from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(80)], null=True,
                                           blank=True)
    phone_number = PhoneNumberField()
    user_image = models.ImageField(upload_to='user_photos',null=True,blank=True)
    RoleChoices = (
        ('seller','seller'),
        ('buyer','buyer'))
    role = models.CharField(choices=RoleChoices, max_length=20,default='buyer')
    date_register = models.DateField(auto_now_add=True)

class Region(models.Model):
    region_name = models.CharField(max_length=100)

class City(models.Model):
    region = models.ForeignKey(Region,on_delete=models.CASCADE)
    city_name = models.CharField(max_length=100)

class District(models.Model):
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    district_name = models.CharField(max_length=100)

class Property(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    PropertyChoices = (
    ('apartment','apartment'),
    ('house','house'),
    ('commercial property','commercial property'),
    ('room','room'),
    ('plot','plot'),
    ('dacha','dacha'),
    ('parking/garage','parking/garage')
    )
    property_type = models.CharField(max_length=120,choices=PropertyChoices)
    region = models.ForeignKey(Region,on_delete=models.CASCADE)
    district = models.ForeignKey(District,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=5,decimal_places=1)
    price = models.PositiveBigIntegerField()
    rooms = models.PositiveIntegerField()
    floor = models.PositiveIntegerField()
    total_floor = models.PositiveIntegerField()
    ConditionChoices = (
    ('for finishing','for finishing'),
    ('European-standard renovation','European-standard renovation'),
    ('good','good'),
    ('average','average'),
    ('unfinished','unfinished'),
    ('any','any'))
    condition = models.CharField(max_length=120,choices=ConditionChoices,default='any')
    documents = models.BooleanField()
    seller = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

class PropertyImage(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE)
    property_image = models.ImageField(upload_to='property_photos')

class Review(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='reviews_written')
    seller = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='reviews_received')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i))for i in range(1, 6)])
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)




