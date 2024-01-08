from django.db import models

# Create your models here.
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='result_images/', default='SOME STRING')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    gray = models.ImageField(default='Not Set')