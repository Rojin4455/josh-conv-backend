from celery import shared_task
from django.conf import settings
from django.utils import timezone
import logging
from .models import AuthCredential
from .utils import refresh_access_token as refresh_token_function

logger = logging.getLogger(__name__)

@shared_task
def refresh_access_tokens():

    print(f"[{timezone.now()}] Running token refresh task")
    

    try:
        tokens = AuthCredential.objects.all() 
        
        print(f"Found {tokens.count()} tokens to refresh")
        
        count = 0
        for token in tokens:
            try:
               
                print("before calling the refresh access token fuinction ----------> ", token)
                refresh_token_function(token)
                count += 1
                print(f"Successfully refreshed token id: {token.id}")
            except Exception as e:
                error_msg = f"Error refreshing token {token.id}: {str(e)}"
                print(error_msg)
                logger.error(error_msg)
        
        success_msg = f"Successfully refreshed {count} tokens"
        print(success_msg)
        logger.info(success_msg)
        return success_msg
    
    except Exception as e:
        error_msg = f"Error in refresh_access_tokens task: {str(e)}"
        print(error_msg)
        logger.error(error_msg)
        return f"Error: {str(e)}"