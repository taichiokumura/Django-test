from django.db import models
import random
import string

def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

class StudentInformation(models.Model):
    student_id = models.CharField(max_length=20, unique=True)

class CardInformation(models.Model):
    student = models.ForeignKey(StudentInformation, on_delete=models.CASCADE, null=True)
    unique_id = models.CharField(max_length=50, unique=True, default=generate_unique_id)
    photo = models.ImageField(upload_to='result_images/', default='SOME STRING')
    observation_date_images = models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    observation_place_images_1 = models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    observation_place_images_2 = models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    river_state_images = models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    living_thing_consideration_images = models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ImagePosition(models.Model):
    student = models.ForeignKey(StudentInformation, on_delete=models.CASCADE, null=True)
    card_info_unique_id = models.CharField(max_length=50, null=True)
    image_url = models.CharField(max_length=255)
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return f"{self.student} {self.unique_id} {self.image_url} ({self.x}, {self.y})"



