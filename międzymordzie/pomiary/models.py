from django.db import models
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver

from colorful.fields import RGBColorField

newValue = {}

class Sonda(models.Model):
    położenie = models.CharField(max_length=100)
    ostatni_pomiar = models.DateTimeField()

    data_ostatni_fragment = models.DateTimeField(default=timezone.now)
    data_ostatni_dzien = models.DateTimeField(default=timezone.now)
    data_ostatni_miesiac = models.DateTimeField(default=timezone.now)

    kolor = RGBColorField(default='#000000')

    def __str__(self):
        return self.położenie

    def pomiary(self):
        #return sorted(self.pomiar_set.all(), key=lambda x: x.godzina())
        return self.pomiar_set.all()

    def fragmenty(self):
        return self.fragment_set.all()

    def dni(self):
        return self.dzien_set.all()

    def miesiace(self):
        return self.miesiac_set.all()

    @staticmethod
    def hex_rgb(value):
        # Dzięki pan Stack Overflow
        value = value.lstrip('#')
        lv = len(value)
        return [ str(int(value[i:i + lv // 3], 16)) for i in range(0, lv, lv // 3) ]

    def kolor_alpha(self):
        return 'rgba(' + ', '.join(self.hex_rgb(self.kolor)) + ', 0.2)'

    class Meta:
        verbose_name_plural = "Sondy"


class Pomiar(models.Model):
    sonda = models.ForeignKey(Sonda, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    wynik = models.DecimalField(max_digits=5, decimal_places=1)

    def wynikf(self):
        return "{} dB".format(self.wynik)

    wynikf.short_description = 'Wynik pomiaru'

    def __str__(self):
        return "{} dB, {}".format(self.wynik, self.sonda.położenie)

    class Meta:
        verbose_name_plural = "Pomiary"

class Fragment(models.Model):
    sonda = models.ForeignKey(Sonda, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    wynik = models.DecimalField(max_digits=5, decimal_places=1)

    class Meta:
        verbose_name_plural = "Fragmenty"

class Dzien(models.Model):
    sonda = models.ForeignKey(Sonda, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    wynik = models.DecimalField(max_digits=5, decimal_places=1)

    class Meta:
        verbose_name_plural = "Dni"

class Miesiac(models.Model):
    sonda = models.ForeignKey(Sonda, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    wynik = models.DecimalField(max_digits=5, decimal_places=1)

    class Meta:
        verbose_name_plural = "Miesiące"

class Przerwa(models.Model):
    nazwa_przerwy = models.CharField(max_length=100, default='Brak nazwy')
    czas_start = models.TimeField(default=timezone.now)
    czas_koniec = models.TimeField(default=timezone.now)

    def __str__(self):
        return self.nazwa_przerwy

    def godzina_koniec(self):
        return czas_koniec.hour*3600 + czas_koniec.min * 60 + czas_koniec.sec

    class Meta:
        verbose_name_plural = "Przerwy"

###########################################################

@receiver(post_save, sender=Pomiar)
def nowy_pomiar(sender, instance, created, **kwargs):
    if not created:
        return

    instance.sonda.ostatni_pomiar = instance.data
    instance.sonda.save()

@receiver(post_save, sender=Fragment)
def nowy_pomiar(sender, instance, created, **kwargs):
    if not created:
        return

    instance.sonda.data_ostatni_fragment = instance.data
    instance.sonda.save()

@receiver(post_save, sender=Dzien)
def nowy_pomiar(sender, instance, created, **kwargs):
    if not created:
        return

    instance.sonda.dzien_ostatni_fragment = instance.data
    instance.sonda.save()

@receiver(post_save, sender=Miesiac)
def nowy_pomiar(sender, instance, created, **kwargs):
    if not created:
        return

    instance.sonda.miesiac_ostatni_fragment = instance.data
    instance.sonda.save()
