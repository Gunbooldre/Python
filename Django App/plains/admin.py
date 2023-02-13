from django.contrib import admin

from plains.models import Plain

# Register your models here.


#ЕЕ потом напишешь
class PlainAdmin(admin.ModelAdmin):
    class Meta:
        model = Plain
    list_display = ('name', 'fromCity','toCity','travel_time')
    list_editable = ('travel_time',)

# Это для начало 
#admin.site.register(Plain)
admin.site.register(Plain,PlainAdmin)