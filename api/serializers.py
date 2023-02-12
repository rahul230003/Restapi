from rest_framework import serializers
from .models import Category,MenuItem,Cart,Order
from django.contrib.auth.models import User,Group
class Categoryserializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class MenuItemserializer(serializers.ModelSerializer):
    class Meta:
        model=MenuItem
        fields = '__all__'
class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class Cartserializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields = '__all__'
    
class Orderserializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'


