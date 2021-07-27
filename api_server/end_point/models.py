from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Currency_value(models.Model):
    value = models.FloatField()
    cur_name = models.CharField(max_length=3)
    dato = models.CharField(max_length=11)

    class Meta:
        unique_together = (("cur_name", "dato"),)

    def __str__(self):
        return '{},{}: {}'.format(self.cur_name,self.dato,self.value)

class CustomUser(AbstractUser):
  #  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254,unique=True)
    dummy =models.CharField(max_length=50, default="", blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['USERNAME']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return f"{self.name} & {self.name}"