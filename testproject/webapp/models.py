from django.db import models

FISH_CHOICES = [
    ('1', 'メダカ'),
    ('2', 'キンブナ'),
    ('3', 'シマドジョウ'),
    ('4', 'タイリクバラタナゴ'),
]

# Create your models here.
class Document(models.Model):
    photo = models.ImageField(upload_to='result_images/', default='SOME STRING')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    gray = models.ImageField(default='Not Set')
    fish = models.CharField(verbose_name="種類名", max_length=50, choices= FISH_CHOICES, blank=True)
    description = models.CharField(max_length=255, blank=True)