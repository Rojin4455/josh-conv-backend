import requests
from django.conf import settings
from django.utils import timezone 
from datetime import timedelta

def refresh_access_token(credentials):
    print("credentials tokenL", credentials)
    refresh_token = credentials.refresh_token

    
    response = requests.post('https://services.leadconnectorhq.com/oauth/token', data={
        'grant_type': 'refresh_token',
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'refresh_token': refresh_token
    })
    
    new_tokens = response.json()



    
    credentials.access_token = new_tokens['access_token']
    credentials.refresh_token = new_tokens.get('refresh_token', refresh_token)
    credentials.expires_at = timezone.now() + timedelta(seconds=new_tokens['expires_in'])
    credentials.save()
    
    return credentials