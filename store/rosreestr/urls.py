from django.urls import path
from . import views

urlpatterns = [
	path('', views.search, name='search'),
	path('object_info/', views.object_info, name='object_info'),
	path('gallery', views.SpatialDataItemListView.as_view(), name='gallery')
]