from django.conf.urls import url, include
from .views import *


urlpatterns = [
    url(r'^search/', include('haystack.urls')),
    url(r'^save', item_save, name='save')
]
