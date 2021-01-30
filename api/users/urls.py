from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'users'

router = DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = [
    url('^', include(router.urls), name='Users'),

]