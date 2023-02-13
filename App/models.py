from django.db import models
from django.contrib.auth.models import User


class patient_data(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    Pregnancies=models.CharField(max_length=50)
    GLucose=models.CharField(max_length=50)
    Blood_Pressure=models.CharField(max_length=50)
    Skin_Thickness=models.CharField(max_length=50)
    Insulin=models.CharField(max_length=50)
    BMI=models.CharField(max_length=50)
    DPF=models.CharField(max_length=50)
    Age=models.CharField(max_length=50)
    Result=models.CharField(max_length=50)
# Create your models here.
