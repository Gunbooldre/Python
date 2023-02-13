from django.db import models

# Create your models here.

class IsBitrix(models.Model):
    lead = models.CharField(max_length = 20,verbose_name='lead id')
    applicationId = models.CharField(max_length = 20,verbose_name='application id')
    clientId = models.CharField(max_length = 20,verbose_name='Клиента id')
    timeCreate = models.DateTimeField(auto_now_add = True,verbose_name='Время создания запроса')
    jsonRequest = models.JSONField(default=dict,verbose_name='Сам отправленный запрос')
    
    class Meta:
        managed = True
        db_table = "is_bitrix"
        verbose_name = "Интеграционная таблица bitrix"
        verbose_name_plural = "Интеграционная таблица bitrix"

    def __str__(self):
        return self.data
