from django.db import models

# Create your models here.
class CardInformation(models.Model):
    photo = models.ImageField(upload_to='result_images/', default='SOME STRING')
    cutout_images = models.ImageField(upload_to='result_images/', default='SOME STRING')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def cutout_image(self, cutout_url):
        self.cutout_images.name = cutout_url
        self.save() 

class StudentInformation(models.Model):
    student_id = models.CharField(max_length=20, unique=True)