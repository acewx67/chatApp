from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Chat(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    timestamp = models.DateField(auto_now=True)

    # def __str__(self):
    #     return self.group