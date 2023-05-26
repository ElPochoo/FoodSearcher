"""
URL configuration for foodproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from food import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('scrap_baguette', views.scrap_baguette, name='scrap_baguette'),
    path('scrap_MikeAndBens', views.scrap_MikeAndBens, name='scrap_MikeAndBens'),
    path('scrap_kfc', views.scrap_kfc, name='scrap_kfc'),
    path('sortbyprice', views.sortbyprice, name='sortbyprice'),
    path('sortby_price', views.sortby_price, name='sortby_price'),
    path('inf', views.inf, name='inf'),
    path('sup_inf', views.sup_inf, name='sup'),
    
]
