from .models import (UserProfile, Region,
                     City, District, Property, PropertyImage, Review)
from modeltranslation.translator import TranslationOptions,register

@register(UserProfile)
class ProductTranslationOptions(TranslationOptions):
    fields = ()

@register(Region)
class ProductTranslationOptions(TranslationOptions):
    fields = ('region_name',)

@register(City)
class ProductTranslationOptions(TranslationOptions):
    fields = ('region', 'city_name')

@register(District)
class ProductTranslationOptions(TranslationOptions):
    fields = ('city', 'district_name')

@register(Property)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description' ,'region' ,'district', 'address', 'area', 'documents')

@register(PropertyImage)
class ProductTranslationOptions(TranslationOptions):
    fields = ()

@register(Review)
class ProductTranslationOptions(TranslationOptions):
    fields = ()