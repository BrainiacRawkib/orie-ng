from django.urls import path
from .views import *

app_name = 'contacts'

urlpatterns = [
    # contact urls
    path('contact-us/', ContactView.as_view(), name='contact'),
    path('sent/', MessageSentView.as_view(), name='message-sent')
]
