from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'depremzedeler', views.PersonViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('report', views.report, name="report"),
    path('search', views.search, name="search"),
    path('api/', include(router.urls)),
]