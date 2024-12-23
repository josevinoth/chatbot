from django.db import models

from ..models import machines_Info


class parts_Info(models.Model):
    p_id=models.CharField(max_length=50, unique=True)
    p_name=models.CharField(max_length=150)
    p_rejection_rate=models.FloatField(default=0.0)
    p_machine_id=models.ForeignKey(machines_Info, null=True, blank=True,on_delete=models.CASCADE,related_name='p_machine_id', db_column='p_machine_id')

    class Meta:
        ordering = ["p_id"]

    def __str__(self):
        return self.p_id