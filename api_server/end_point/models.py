from django.db import models

# Create your models here.
class Currency_value(models.Model):
    value = models.FloatField()
    cur_name = models.CharField(max_length=3)
    dato = models.CharField(max_length=11)

    class Meta:
        unique_together = (("cur_name", "dato"),)

    def __str__(self):
        return '{},{}: {}'.format(self.cur_name,self.dato,self.value)