from django.db import models

FISH_CHOICES = [
    ('1', 'メダカ'),
    ('2', 'キンブナ'),
    ('3', 'シマドジョウ'),
    ('4', 'タイリクバラタナゴ'),
]

# Create your models here.
class CardInformation(models.Model):
    photo = models.ImageField(upload_to='result_images/', default='SOME STRING')
    cutout_images = models.ImageField(upload_to='result_images/', default='SOME STRING')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    fish = models.CharField(verbose_name="種類名", max_length=50, choices= FISH_CHOICES, blank=True)
    explanation = models.CharField(max_length=255, blank=True)

    def cutout_image(self, cutout_url):
        self.cutout_images.name = cutout_url
        self.save() 

class StudentInformation(models.Model):
    student_id = models.CharField(max_length=20, unique=True)