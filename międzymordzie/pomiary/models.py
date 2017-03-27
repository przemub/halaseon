from django.db import models
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver


class Sonda(models.Model):
    położenie = models.CharField(max_length=100)
    ostatni_pomiar = models.DateTimeField()

    def __str__(self):
        return self.położenie

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
        return self.data.hour * 100 + self.data.minute

    class Meta:
        verbose_name_plural = "Pomiary"


@receiver(post_save, sender=Pomiar)
def nowy_pomiar(sender, instance, created, **kwargs):
    if not created:
        return

    instance.sonda.ostatni_pomiar = instance.data
    instance.sonda.save()
