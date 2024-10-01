from django.db import models

import os


class Lead(models.Model):
    lead_name = models.CharField(max_length=55)
    lead_id_on_bs = models.CharField(max_length=36, null=True, blank=True)
    client_id = models.CharField(max_length=36, null=True, blank=True)
    app_id = models.CharField(max_length=36, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    request_from_partner = models.JSONField(default=dict, verbose_name='Сам отправленный запрос')
    documents_sent_status = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.lead_name



    