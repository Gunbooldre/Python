# Generated by Django 4.1.1 on 2023-02-08 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_alter_usersmodel_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersmodel',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.listpeoplemodel', verbose_name='id user'),
        ),
    ]
