from django.db import models
from django.conf import settings

# Create your models here.
class Friendship(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="profile")
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friends") 
    request = models.BooleanField(default=False, null=False)
    accept = models.BooleanField(default=False, null=False)

    class Meta:
        unique_together = [["profile", "friend"]]



