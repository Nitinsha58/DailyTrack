from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class DailyTrack(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'Profile', default='')
    income = models.IntegerField()
    expense = models.IntegerField()
    note = models.TextField(null = True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return f'Income {self.income} Income {self.expense}'
