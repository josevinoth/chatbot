from django.db import models

class operation_status_Info(models.Model):
    os_name=models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["os_name"]

    def __str__(self):
        return self.os_name