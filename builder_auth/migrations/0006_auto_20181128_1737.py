# Generated by Django 2.1.3 on 2018-11-28 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder_auth', '0005_auto_20181128_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(error_messages={'invalid': 'Пользователь с такой почтой уже существует.'}, max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
