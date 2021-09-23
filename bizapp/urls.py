from django.urls import path 
from . import views 


urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('products/', views.all_products, name='products'),
    path('category/<str:id>/', views.product_category, name='category'),
    path('detail/<str:id>/', views.product_detail, name='detail'),
    path('loginform/', views.loginform, name='loginform'),
    path('logoutform/', views.logoutform, name='logoutform'),
    path('signupform/', views.signupform, name='signupform'),
    path('profile/', views.profile, name='profile'),
    path('update/', views.update, name='update'),
    path('password/', views.password, name='password'),
    path('shopcart/', views.shopcart, name='shopcart'),
    path('cart/', views.cart, name='cart'),
    path('increase/', views.increase, name='increase'),
    path('remove/', views.remove, name='remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('placeorder/', views.paidorder, name='paidorder'),
    path('completed/', views.completed, name='completed'),
]
