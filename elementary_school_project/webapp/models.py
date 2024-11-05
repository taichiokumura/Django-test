from django.db import models
import random
import string

def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

class StudentInformation(models.Model):
    name_id = models.CharField(max_length=100, null=True)
    student_id = models.CharField(max_length=20, unique=True)
    year = models.IntegerField(default=2024, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name_id} {self.student_id} ({self.year})"

class CardInformation(models.Model):
    student = models.ForeignKey(StudentInformation, on_delete=models.CASCADE, null=True)
    unique_id = models.CharField(max_length=50, unique=True, default=generate_unique_id)
    photo = models.ImageField(upload_to='result_images/', default='SOME STRING')
    observation_date_images = models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    observation_place_images_1 = models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    observation_place_images_2 = models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    river_state_images = models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    living_thing_consideration_images = models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    year = models.IntegerField(default=2024, null=True, blank=True) 
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ImagePosition(models.Model):
    student = models.ForeignKey(StudentInformation, on_delete=models.CASCADE, null=True)
    card_info_unique_id = models.CharField(max_length=50, null=True)
    image_url = models.CharField(max_length=255)
    illustration_image = models.CharField(max_length=255, null=True, blank=True)
    river_location = models.CharField(max_length=50, null=True)
    x = models.FloatField()
    y = models.FloatField()
    year = models.IntegerField(default=2024, null=True, blank=True)

    def __str__(self):
        return f"{self.student} {self.unique_id} {self.image_url} ({self.x}, {self.y}) {self.year} {self.illustration_image}"
    
class AquaticLifeEncyclopedia(models.Model):
    name = models.CharField(max_length=100)
    model_file = models.FileField(upload_to='models/', blank=True, null=True) #3DモデルのURL
    discovered = models.BooleanField(default=False) #発見されたかどうか
  



