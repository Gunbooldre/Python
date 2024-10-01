from django.db import models
from django.contrib.auth.models import User



class ListPeopleModel(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='ФИО')
    dep = models.CharField(max_length=200, blank=True, null=True, verbose_name='Департамент')
    responsiveness = models.PositiveSmallIntegerField(default=0,choices=[(i, i) for i in range(1, 6)], verbose_name='Отзывчивый')
    friendliness = models.PositiveSmallIntegerField(default=0,choices=[(i, i) for i in range(1, 6)], verbose_name='Доброжелательный')
    boss = models.ForeignKey('ListBossModel',on_delete=models.CASCADE, blank=True,null=True,verbose_name="id boss")


    class Meta:
        managed = True
        db_table = "people_list_model"
        verbose_name = "Таблица сотрудников"
        verbose_name_plural = "Таблица сотрудников"

    # def __str__(self):
    #     return self.name

class ListBossModel(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='ФИО')
    dep = models.CharField(max_length=200, blank=True, null=True, verbose_name='Департамент')

    class Meta:
        managed = True
        db_table = "boss_list_model"
        verbose_name = "Таблица боссов"
        verbose_name_plural = "Таблица боссов"

    def __int__(self):
        return self.id

class UsersModel(models.Model):
    login = models.CharField(max_length=200,blank=True , null = True,  verbose_name='Логин', unique=True)
    password = models.CharField(max_length=200,blank=True , null = True, verbose_name='Пароль')
    timeInput = models.DateTimeField(default=None, null = True, blank=True, verbose_name='Дата последнего входа')
    last_login = models.DateTimeField(auto_now=True)
    timeAuthEdit = models.DateTimeField(default=None,null = True, blank=True, verbose_name='Дата изменения пароля')
    isVoted = models.BooleanField(default=True, blank=True, null=True, verbose_name='Значение')
    boss_id = models.ForeignKey(ListBossModel,on_delete=models.CASCADE, blank=True,null=True,verbose_name="id boss")
    user_id = models.ForeignKey(ListPeopleModel,on_delete=models.CASCADE, blank=True,null=True,verbose_name="id user")


    class Meta:
        managed = True
        db_table = "ligin_user_model"
        verbose_name = "Таблица пользователей"
        verbose_name_plural = "Таблица пользователей"


    def __str__(self):
        return self.login


