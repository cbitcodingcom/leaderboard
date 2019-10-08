from . import views
from django.urls import path

urlpatterns = [
	path('', views.index, name='index'),
	path('update', views.update, name='update'),
	path('confirm', views.confirm, name='confirm')
]