from django.db import models

from ..models import operation_status_Info


class cells_Info(models.Model):
    c_id=models.CharField(max_length=50, unique=True)
    c_name=models.CharField(max_length=150)
    c_operator_name=models.CharField(max_length=50)
    c_status=models.ForeignKey(operation_status_Info, null=True, blank=True)

    class Meta:
        ordering = ["c_id"]

    def __str__(self):
        return self.c_id