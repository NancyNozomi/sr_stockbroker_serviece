"""sr_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from stockbroker_service import views

urlpatterns = [
    path('', views.index),
    path("index", views.index),
    path("login", views.log_in),
    path("list", views.get_usr_info),
    path("visual", views.visual),
    path("trade_request", views.trade_request),
    path("trade", views.trade),
    path("trade_finished", views.get_usr_info),
    path("query", views.query)
]

