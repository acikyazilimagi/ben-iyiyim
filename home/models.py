from django.db import models
from django.utils import timezone
# Create your models here.



class Person(models.Model):
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
        ("iyiyim", "İyiyim"),
        ("yardim", "Enkaz altında değilim fakat yardıma ihtiyacım var"),
        ("enkaz-altinda", "Enkaz altındayım"),
    )

    isim = models.CharField(max_length=100)
    sehir = models.CharField(max_length=100, choices=IL_CHOICES)
    adres = models.CharField(max_length=256)
    tel = models.CharField(max_length=11, default="Yok")
    durum = models.CharField(max_length=100, choices=DURUM_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
