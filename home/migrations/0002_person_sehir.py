# Generated by Django 4.0.4 on 2023-02-07 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='sehir',
            field=models.CharField(default='Yok', max_length=100),
        ),
    ]