from django.db import models
from django.utils import timezone


class Depremzede(models.Model):
    IL_CHOICES = (
        ("Adana", "Adana"),
        ("Batman", "Batman"),
        ("Bitlis", "Bitlis"),
        ("Bingöl", "Bingöl"),
        ("Diyarbakır", "Diyarbakır"),
        ("Elazığ", "Elazığ"),
        ("Gaziantep", "Gaziantep"),
        ("Hakkari", "Hakkari"),
        ("Hatay", "Hatay"),
        ("Kahramanmaraş", "Kahramanmaraş"),
        ("Kilis", "Kilis"),
        ("Malatya", "Malatya"),
        ("Mardin", "Mardin"),
        ("Muş", "Muş"),
        ("Osmaniye", "Osmaniye"),
        ("Siirt", "Siirt"),
        ("Şırnak", "Şırnak"),
        ("Van", "Van"),
    )
    DURUM_CHOICES = (
        ("Sağlıklı", "Sağlıklı"),
        ("Yaralı", "Yaralı"),
        ("Ölü", "Ölü"),
    )
    isim = models.CharField(max_length=100)
    il = models.CharField(max_length=100, choices=IL_CHOICES)
    adres = models.CharField(max_length=200, blank=True, null=True)
    tarif = models.CharField(max_length=200, blank=True, null=True)
    telefon = models.CharField(max_length=13)
    cikarildi = models.BooleanField(default=False)
    durum = models.CharField(
        max_length=100, choices=DURUM_CHOICES, blank=True, null=True
    )
    tarih = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Depremzedeler"
