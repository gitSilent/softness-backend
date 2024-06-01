"""
URL configuration for softness project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from cart.views import CartAPIView, CartItemIncreaseAPIView, CartItemDecreaseAPIView, CartItemAPIView
from orders.views import OrdersAPIView
from products.views import ProductsAPIView, ProductAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from users.views import UserAPIView, CityAPIView, CitiesAPIView, FavoriteListAPIView, FavoriteListItemAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/products/', ProductsAPIView.as_view()),
    path('api/v1/products/<int:pk>/', ProductAPIView.as_view()),

    path('api/v1/cart/', CartAPIView.as_view()),
    path('api/v1/cartitem/<int:cart_item_id>/', CartItemAPIView.as_view()),
    path('api/v1/cartitem/increase/<int:cart_item_id>/', CartItemIncreaseAPIView.as_view()),
    path('api/v1/cartitem/decrease/<int:cart_item_id>/', CartItemDecreaseAPIView.as_view()),

    path('api/v1/cities/', CitiesAPIView.as_view()),
    path('api/v1/cities/<int:pk>', CityAPIView.as_view()),
    path('api/v1/userinfo/', UserAPIView.as_view()),

    path('api/v1/favoritelist/', FavoriteListAPIView.as_view()),
    path('api/v1/favoritelist/<int:pk>', FavoriteListItemAPIView.as_view()),

    path('api/v1/orders/', OrdersAPIView.as_view()),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
