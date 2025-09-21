from django.db import models
from django.conf import settings


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title
    

class Snippet(models.Model):
    title = models.CharField(max_length=250)
    note = models.TextField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="snippets")
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="snippets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title