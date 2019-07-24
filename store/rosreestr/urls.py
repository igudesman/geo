from django.urls import path
from . import views

urlpatterns = [
	path('', views.search, name='search'),
	path('not_found/', views.not_found, name='not_found'),
	path('object_info/', views.object_info, name='object_info'),
]