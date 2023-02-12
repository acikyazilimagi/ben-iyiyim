# Generated by Django 4.1.6 on 2023-02-12 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_person_address_alter_person_durum_alter_person_isim'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='address',
            field=models.GenericIPAddressField(default='0.0.0.0'),
        ),
        migrations.AddField(
            model_name='person',
            name='notlar',
            field=models.CharField(default='Yok', max_length=200),
        ),
    ]