from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth import authenticate
from django.db import models 
from django.db.models import F
from django.db.models.functions import Concat,Cast
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed

from rest_framework import serializers

from .models import User
from . import models

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number','password')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):
        user = User.objects.create_user(phone_number=validated_data['phone_number'],password = validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone']

class SignInSerializer(serializers.Serializer):
 

    phone_number=serializers.CharField()
    password=serializers.CharField(write_only=True)
   
    tokens=serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = (
             'password', 'phone_number', 'tokens'
        )

        # read_only_fields = ('created_at', 'modified_at', 'created_by', 'modified_by')

    def get_tokens(self, obj):
        user = get_object_or_404(User, phone_number=obj.get('phone_number'))
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

   

    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number', '')
        password = attrs.get('password', '')
        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            raise AuthenticationFailed(_('Hisob maʼlumotlari notoʻgʻri, qayta urinib koʻring'))
        if not user.is_active:
            raise AuthenticationFailed(_("Hisob o'chirilgan, administrator bilan bog'laning"))
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            
            'tokens': user.tokens(),
            'phone_number': user.phone_number,
        }
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        return data
     
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Category
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Product
        fields="__all__"

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CartProduct
        fields=["product",]

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.OrderProduct
        fields=["quantity",'price','product']

class OrderProductExtraSerializer(serializers.Serializer):
    total_price=serializers.DecimalField(max_digits=25,decimal_places=2)
    order_products=OrderProductSerializer()


    class Meta:
        
        fields=['total_price','order_products']

