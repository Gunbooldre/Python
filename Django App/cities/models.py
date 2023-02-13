from django.urls import reverse
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

    #Перед тем как написать этот моммент нужно будет допустить ошибку

    def get_absolute_url(self):
        return reverse('cities:detail', kwargs={'pk':self.pk})