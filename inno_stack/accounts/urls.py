from django.urls import path
from .views import AuthCredentialCreateView, ConversationView

urlpatterns = [
    path('create-credentials/', AuthCredentialCreateView.as_view()),
    path('unread-messages/<str:location_id>/', ConversationView.as_view())
]