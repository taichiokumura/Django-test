from django.db import models

# Create your models here.
class StudentInformation(models.Model):
    student_id = models.CharField(max_length=20, unique=True)

class CardInformation(models.Model):
    student = models.ForeignKey(StudentInformation, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='result_images/', default='SOME STRING')
    observation_date_images = models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    observation_place_images_1 = models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    observation_place_images_2 = models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    river_state_images = models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    living_thing_consideration_images =models.ImageField(upload_to='result_images/', default='SOME STRING', max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)