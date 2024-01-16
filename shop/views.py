from django.shortcuts import render

import pandas as pd

from .serializers import SignInSerializer,CartProductSerializer,ProductSerializer,OrderProductSerializer,OrderProductExtraSerializer

from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView,CreateAPIView,GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import Product,Order
from . import models
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import RegisterSerializer,UserSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": RegisterSerializer(user,context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

class SignInView(GenericAPIView):
    serializer_class = SignInSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer,'serialzier')

        if serializer.is_valid(raise_exception=True):
            print(serializer.data)
            return Response(serializer.data, 200)
        return Response({'message:Unathenticated'},status=401)

class ProductListView(ListAPIView):
  
    serializer_class=ProductSerializer

    def get_queryset(self):
        queryset=models.Product.objects.filter(is_active=True)
        return queryset
    
class ProductListByCategoryView(ListAPIView):
    serializer_class=ProductSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="The make of the product",
                              type=openapi.TYPE_STRING),
          
        ],
        responses={200: 'OK'}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        category=self.request.query_params.get('category')
        print(category,'this is categ')
        if category:
            queryset=models.Product.objects.filter(category__name=category,is_active=True)
        else:
            queryset = models.Product.objects.filter(is_active=True)
        return queryset
    
class AddToCartView(CreateAPIView):
    queryset=models.CartProduct.objects.all()
    serializer_class=CartProductSerializer

    def create(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=401)
       
        product_id=request.data.get('product')
        print(product_id,'product_id')
        print(request.user,'user')

        product=get_object_or_404(models.Product,id=product_id)
        try:
            models.CartProduct.objects.create(product=product,created_by=request.user,modified_by=request.user)
            return Response({'message':"Succesfully created"},status=200)
        except:
            return Response({'message':'Error happened'},status=400)

class GetCartProductView(ListAPIView):
   
    serializer_class=CartProductSerializer

    def get_queryset(self):
        print(self.request.user)
       
        queryset=models.CartProduct.objects.filter(created_by=self.request.user)
        if queryset.exists():
            return queryset
        else:
            return models.CartProduct.objects.none()
        


from django.db import transaction      
class OrderProductView(CreateAPIView):
    queryset=models.OrderProduct.objects.all()
    serializer_class=OrderProductExtraSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=401)
        
        order = Order.objects.create(total_price=request.data.get('total_price'))
        print(request.data.get('order_products'),'this is json')
        for order_product_data in request.data.get('order_products'):

            product_id = order_product_data['product']
            quantity = order_product_data['quantity']
            price = order_product_data['price']

            product = Product.objects.get(id=int(product_id))

            order_product = models.OrderProduct.objects.create(
                product=product,
                order=order,
                quantity=quantity,
                price=price
            )
        return Response({'message':'Succesfully saved'},status=200)

        
from openpyxl import load_workbook

class Insert_into_view(APIView):
    def get(self,request,*args,**kwrgs):
        df=pd.read_excel('PriceList.xlsx') 
        for index,data in df.iterrows():
            print(data)
            if index>3:
                Product.objects.create(title=data['Unnamed: 2'],price=float(data['Unnamed: 3']),is_active=True,box=data['Unnamed: 4'])
           


            # models.Product.objects.create(title=data[''])


    
    

