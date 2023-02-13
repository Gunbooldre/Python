# Generated by Django 4.1.3 on 2023-01-31 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('is_bitrix24', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IsBitrix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lead', models.CharField(max_length=20, verbose_name='lead id')),
                ('applicationId', models.CharField(max_length=20, verbose_name='application id')),
                ('clientId', models.CharField(max_length=20, verbose_name='Клиента id')),
                ('timeCreate', models.DateTimeField(auto_now_add=True, verbose_name='Время создания запроса')),
                ('jsonRequest', models.JSONField(default=dict, verbose_name='Сам отправленный запрос')),
            ],
            options={
                'verbose_name': 'Интеграционная таблица allur',
                'verbose_name_plural': 'Интеграционная таблица allur',
                'db_table': 'is_bitrix',
                'managed': True,
            },
        ),
        migrations.DeleteModel(
            name='Lead',
        ),
    ]
