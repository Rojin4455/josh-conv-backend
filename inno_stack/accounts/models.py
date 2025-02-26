from django.db import models

class AuthCredential(models.Model):
    access_token = models.TextField()
    company_id = models.CharField(max_length=50)
    location_id = models.CharField(max_length=50)
    refresh_token = models.TextField()
    scope = models.TextField()
    token_type = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    user_type = models.CharField(max_length=50)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.token_type}"