"""pro1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from api.views import MenuItemDisplay,Manageusers,Manageusersrud,ManageDelivery,Managedeliveryrud,managecart,managerdcart,orderView,orderviewrud
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/menu-items',MenuItemDisplay.as_view()),
    path('api/menu-items/<int:id>',MenuItemDisplay.as_view()),
    path('api/manager/users',Manageusers.as_view()),
    path('api/manager/users/<int:pk>',Manageusersrud.as_view()),
    path('api/delivery/users',ManageDelivery.as_view()),
    path('api/delivery/users/<int:pk>',Managedeliveryrud.as_view()),
    path('api/cart/menu-items',managecart.as_view()),
    path('api/cart/menu-items/<int:pk>',managerdcart.as_view()),
    path('api/order',orderView.as_view()),
    path('api/order/<int:pk>',orderviewrud.as_view())

]
