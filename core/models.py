from django.db import models

# Create your models here.

class YogaClass(models.Model):
    CLASS_TYPE_CHOICES = [
        ('online', 'Online'),
        ('in_person', 'In Person'),
    ]

    title = models.CharField(max_length=100)
    class_type = models.CharField(max_length=10, choices=CLASS_TYPE_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.get_class_type_display()})"