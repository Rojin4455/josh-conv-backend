from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'


    def ready(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        import json
        
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=23,
            period=IntervalSchedule.HOURS,
        )
        
        PeriodicTask.objects.get_or_create(
            name='Refresh access tokens',
            task='accounts.tasks.refresh_access_tokens',
            interval=schedule,
            kwargs=json.dumps({}),
            expires=None,
        )




        
