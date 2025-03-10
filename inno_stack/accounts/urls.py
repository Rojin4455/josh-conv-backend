from django.urls import path
from .views import AuthCredentialCreateView, ConversationView, LocationsView, LocationStatusUpdateView, LoginView, CheckAuthView, LogoutView

urlpatterns = [
    path('create-credentials/', AuthCredentialCreateView.as_view()),
    path('unread-messages/<str:location_id>/', ConversationView.as_view()),
    path('all-locations/', LocationsView.as_view()),
    path('locations-change-status/<int:location_id>/<str:stat>/', LocationStatusUpdateView.as_view(), name="location-status-update"),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('check-auth/', CheckAuthView.as_view()),
]