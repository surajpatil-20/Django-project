from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):

    DEPARTMENTS = [
        ('Computer Science', 'Computer Science'),
        ('Mechanical', 'Mechanical'),
        ('Civil', 'Civil'),
        ('Electrical', 'Electrical'),
        ('Data Science','Data Science')
    ]

    YEARS = [
        ('First Year', 'First Year'),
        ('Second Year', 'Second Year'),
        ('Third Year', 'Third Year'),
        ('Fourth Year', 'Fourth Year'),
    ]

    title = models.CharField(max_length=200)
    department = models.CharField(max_length=25, choices=DEPARTMENTS, default="computer")
    year = models.CharField(max_length=25, choices=YEARS,default=1)
    file = models.FileField(upload_to='protected/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.department} - Year {self.year}"
# Create your models here.
