from django.db import models
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver

from colorful.fields import RGBColorField

class Sonda(models.Model):
    położenie = models.CharField(max_length=100)
    ostatni_pomiar = models.DateTimeField()

    kolor = RGBColorField(default='#000000')

    def __str__(self):
        return self.położenie

    def pomiary(self):
        return sorted(self.pomiar_set.all(), key=lambda x: x.godzina())

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

    def godzina(self):
        # Nie bijcie
        data = timezone.localtime(self.data)
        return data.hour * 100 + data.minute

    class Meta:
        verbose_name_plural = "Pomiary"


@receiver(post_save, sender=Pomiar)
def nowy_pomiar(sender, instance, created, **kwargs):
    if not created:
        return

    instance.sonda.ostatni_pomiar = instance.data
    instance.sonda.save()
