from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework.response import Response
import requests
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core.cache import cache
from django.utils import timezone
import logging


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
    


    
        
class LocationsView(generics.ListAPIView):
    queryset = AuthCredential.objects.all()
    serializer_class = AuthCredentialSerializer
    permission_classes = [AllowAny]


class LocationStatusUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, location_id, stat):
        print("hererer")
        print("Status:L ",stat)
        location = get_object_or_404(AuthCredential, id=location_id)
        location.is_blocked = True if stat == "true" else False
        location.save()

        return Response(
            {"message": "Location status updated successfully", "location": AuthCredentialSerializer(location).data},
            status=status.HTTP_200_OK
        )
    





logger = logging.getLogger(__name__)

class ConversationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, location_id):
        if not location_id:
            return Response({'error': 'Location ID is required'}, status=400)
        
        global_cache_key = f"ghl_unread_messages:{location_id}"
        
        try:
            cached_data = cache.get(global_cache_key)
            print(cached_data,"reached hererrre 1")
            
            if not cached_data or self.is_cache_expired(cached_data):
                print("reached here cached_data and it not expired:", cached_data, self.is_cache_expired(cached_data))
                lock_key = f"{global_cache_key}_lock"
                lock_acquired = cache.add(lock_key, True, 30)  # 30-second lock
                
                if lock_acquired:
                    try:
                        new_data = self.fetch_ghl_unread_messages(location_id)
                        
                        # Cache the new data for 1 minute
                        cache.set(global_cache_key, new_data, 60)
                    except Exception as e:
                        logger.error(f"Error fetching GHL messages: {e}")
                        if cached_data:
                            return Response(cached_data)
                        raise
                    finally:
                        cache.delete(lock_key)
                        cached_data = cache.get(global_cache_key)

                else:

                    return Response(cached_data or {'unreadCount': 0})
            
            return Response(cached_data or {'unreadCount': 0})
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'error': 'An unexpected error occurred'}, status=500)
    
    def is_cache_expired(self, cached_data):
        """
        Check if the cached data is older than 1 minute
        """
        if not cached_data:
            return True
        
        current_time = timezone.now().timestamp()
        cached_time = cached_data.get('timestamp', 0)
        
        return (current_time - cached_time) > 60  # More than 1 minute old
    
    def fetch_ghl_unread_messages(self, location_id):


        print("ghl api called")
        try:
            credentials = AuthCredential.objects.get(location_id=location_id)
            access_token = credentials.access_token
            
            url = "https://services.leadconnectorhq.com/conversations/search"
            querystring = {"locationId": location_id, "status": "unread"}
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Version": "2021-04-15",
                "Accept": "application/json"
            }

            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            
            total_unread_messages = sum(convo["unreadCount"] for convo in data["conversations"])
            
            return {
                'unreadCount': total_unread_messages,
                'timestamp': timezone.now().timestamp()
            }
        
        except AuthCredential.DoesNotExist:
            raise ValueError('Credentials not found for this location')
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error in GHL API call: {str(e)}")
