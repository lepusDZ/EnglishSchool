from django.db import models
from django_quill.fields import QuillField
from django.urls import reverse

class Main(models.Model):
    title = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.title

class Photo(models.Model):
    photo = models.ImageField(upload_to='photos/')  # Specify the upload directory for the images
    caption = models.CharField(max_length=255, blank=True)  # Add a field for a caption (optional)
    created_at = models.DateTimeField(auto_now_add=True)  # Add a field to store the creation timestamp

    def __str__(self):
        return f"Photo {self.id}"

