from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from PIL import Image


class Ticket(models.Model):
    """Modèle de ticket."""
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Représentation d'un ticket sous forme de chaînes de caractères."""
        return self.title

    def resize_image(self):
        """Redimentionne la taille d'une image tout en gardant le ratio d'origine."""
        image = Image.open(self.image)
        max_height = 800
        ratio_width = image.width / image.height * max_height
        image.thumbnail(size=(max_height, ratio_width))
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        """Surcharge de la méthode de classe avec redimention d'une image s'il y en a une."""
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()


class Review(models.Model):
    """Modèle de critique."""
    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=None)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Représentation d'une critique sous forme de chaînes de caractères."""
        return self.headline
