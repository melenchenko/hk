from django.conf import settings
from django.db import models
from django.utils import timezone

class Load(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads/')
    created_date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=40, default='Demo')

    def __str__(self):
        return self.title
