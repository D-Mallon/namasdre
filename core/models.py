from django.db import models
from django.utils import timezone

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

    def save(self, *args, **kwargs):
        if not timezone.is_aware(self.start_time):
            self.start_time = timezone.make_aware(self.start_time)
        if not timezone.is_aware(self.end_time):
            self.end_time = timezone.make_aware(self.end_time)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_class_type_display()})"

class YogaClassBooking(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    yoga_class = models.ForeignKey(YogaClass, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.yoga_class.title} at {self.booking_time}"