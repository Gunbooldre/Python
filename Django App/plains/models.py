from genericpath import exists
from turtle import mode
from django.db import models
from django.forms import ValidationError

from cities.models import City

# Create your models here.

class Plain (models.Model):
    name = models.CharField(max_length=50,unique=True,verbose_name = "Номер самолета")
    travel_time = models.PositiveIntegerField(verbose_name = 'Время в пути')
    fromCity= models.ForeignKey(City,on_delete=models.CASCADE,related_name='from_city_set',verbose_name ='Из какого Города')
    toCity = models.ForeignKey(City,on_delete=models.CASCADE,related_name='to_city_set',verbose_name ='В какой Город')

    def __str__(self):
        return f'Самолет №{self.name} из города {self.fromCity}'

    class Meta:
        verbose_name = 'Самолет'
        verbose_name_plural =  'Самолеты'
        ordering = ['travel_time']
    
    def clean(self):
        if self.fromCity == self.toCity:
            raise ValidationError('Изменить Город прибытия')
        qs = Plain.objects.filter(
            fromCity=self.fromCity,toCity=self.toCity,travel_time=self.travel_time).exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError('Изменить время пути')


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
