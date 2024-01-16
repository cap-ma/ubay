from django.urls import path
from .views import (ProductListView,ProductListByCategoryView,AddToCartView,\
    RegisterView,SignInView,OrderProductView,GetCartProductView,Insert_into_view
    )



urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('sign-in/',SignInView.as_view(),name='sign-in'),

    path('products/',ProductListView.as_view(),name='product-list'),
    path('products_by_category',ProductListByCategoryView.as_view(),name='products-by-category'),
    path('add_to_cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('order_product',OrderProductView.as_view(),name='order-product'),
    path('get_cartproducts',GetCartProductView.as_view(),name='cart-product'),
    path('inser_db',Insert_into_view.as_view(),name='insert-db')

]
