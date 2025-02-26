from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework.response import Response
import requests

class AuthCredentialCreateView(generics.CreateAPIView):
    queryset = AuthCredential.objects.all()
    serializer_class = AuthCredentialSerializer

    def perform_create(self, serializer):
        location_id = self.request.data.get("location_id")


        auth_credential, created = AuthCredential.objects.update_or_create(
            location_id=location_id,
            defaults={**serializer.validated_data}
        )

        return auth_credential
    

class ConversationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, location_id):
        print("reached here")
        if not location_id:
            return Response({'error': 'Location ID is required'}, status=400)
        
        try:
            credentials = AuthCredential.objects.get(location_id=location_id)
            access_token = credentials.access_token
            
            url = "https://services.leadconnectorhq.com/conversations/search"

            querystring = {"locationId":location_id,"status":"unread"}

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Version": "2021-04-15",
                "Accept": "application/json"
            }

            response = requests.get(url, headers=headers, params=querystring)
            
            response.raise_for_status()
            data = response.json()
            
            total_unread_messages = sum(convo["unreadCount"] for convo in data["conversations"])
            print("Total unread messages:", total_unread_messages)
            
            return Response({
                'unreadCount': total_unread_messages
            })
        
        except AuthCredential.DoesNotExist:
            return Response({'error': 'Credentials not found for this location'}, status=404)
        except requests.exceptions.RequestException as e:
            print("Error in API call:", str(e))
            return Response({'error': str(e)}, status=500)