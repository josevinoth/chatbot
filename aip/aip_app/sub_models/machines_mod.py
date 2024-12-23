from django.db import models

class machines_Info(models.Model):
    m_id=models.CharField(max_length=50, unique=True)
    m_name=models.CharField(max_length=150)
    m_performance_score=models.FloatField(default=0.0)
    m_cycle_time=models.FloatField(default=0.0)
    m_down_time_start=models.DateTimeField()
    m_down_time_mins=models.FloatField(default=0.0)
    m_energy_consumed=models.FloatField(default=0.0)
    m_productive_hors=models.FloatField(default=0.0)
    class Meta:
        ordering = ["m_id"]

    def __str__(self):
        return self.m_id