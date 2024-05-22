from django.db import models

# Create your models here.
class StudentInformation(models.Model):
    student_id = models.CharField(max_length=20, unique=True)

class CardInformation(models.Model):
    student = models.ForeignKey(StudentInformation, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='result_images/', default='SOME STRING')
    observation_date_images = models.ImageField(upload_to='result_images/', default='SOME STRING')
    observation_place_images_1 = models.ImageField(upload_to='result_images/', default='SOME STRING')
    observation_place_images_2 = models.ImageField(upload_to='result_images/', default='SOME STRING')
    river_state_images = models.ImageField(upload_to='result_images/', default='SOME STRING')
    living_thing_consideration_images =models.ImageField(upload_to='result_images/', default='SOME STRING')
    # cutout_images = models.ImageField(upload_to='result_images/', default='SOME STRING')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # def cutout_image(self, cutout_url):
    #     self.cutout_images.name = cutout_url
    #     self.save() 