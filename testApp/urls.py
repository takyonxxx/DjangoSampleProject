"""ViaManagerLocal URL Configuration

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
from django.urls import path

from testApp import views
from testApp.views import docs

urlpatterns = [
    path('test_api/', views.test_api, name='test_api'),
    path('test_db/', views.test_db, name='test_db'),
    path('orders_api/', views.OrderViewSet.as_view({'post': 'create', 'get': 'list'}), name='orders_api'),
    path('orders_api/<int:pk>/', views.OrderViewSet.as_view(
        {'put': 'update', 'delete': 'destroy', 'get': 'retrieve'}),
         name='update_orders_api'),
    path('docs/', docs, name='docs'),
]
