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
from django.urls import path, include

from testApp import views
from testApp.views import example_view

urlpatterns = [
    path('test_api/', views.test_api, name='test_api'),
    path('get_test_models/', views.get_test_models, name='get_test_models'),
    path('get_test_model_by_sub_model_name/', views.get_test_model_by_sub_model_name,
         name='get_test_model_by_sub_model_name'),
    path('test_models_api/', views.TestApiViewSet.as_view({'post': 'create'}), name='test_models_create'),
    path('test_models_api/<int:pk>/', views.TestApiViewSet.as_view(
        {'put': 'update', 'delete': 'destroy', 'get': 'retrieve'}),
         name='test_models_update_delete'),
    path('example/', example_view, name='example_view'),
]
