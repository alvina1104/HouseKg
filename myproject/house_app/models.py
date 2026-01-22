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

    def __str__(self):
        return self.region_name

class City(models.Model):
    region = models.ForeignKey(Region,on_delete=models.CASCADE,related_name='cities')
    city_name = models.CharField(max_length=100)

    def __str__(self):
        return self.city_name

class District(models.Model):
    city = models.ForeignKey(City,on_delete=models.CASCADE,related_name='districts')
    district_name = models.CharField(max_length=100)

    def __str__(self):
        return self.district_name

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
    region = models.ForeignKey(Region,on_delete=models.CASCADE,related_name='properties')
    city = models.ForeignKey(City,on_delete=models.CASCADE,related_name='properties')
    district = models.ForeignKey(District,on_delete=models.CASCADE,related_name='properties')
    address = models.CharField(max_length=100)
    area = models.CharField()
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
    created_date = models.DateField(auto_now_add=True)
    seller = models.ForeignKey(UserProfile,on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return self.title

    def get_avg_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(i.rating for i in reviews) / reviews.count(), 1)
        return 0

    def get_count_person(self):
        return self.reviews.count()

class PropertyImage(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='property_images')
    property_image = models.ImageField(upload_to='property_photos')

class Review(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='reviews_written')
    seller = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='reviews_received')
    property = models.ForeignKey(Property, on_delete=models.CASCADE,related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i))for i in range(1, 6)])
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author},{self.seller}'




