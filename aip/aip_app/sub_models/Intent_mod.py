from django.db import models

class Intent(models.Model):
    name = models.CharField(max_length=255)
    response = models.TextField()

    def __str__(self):
        return self.name
