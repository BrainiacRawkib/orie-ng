from django.db import models
from django.utils.timezone import now


class Contact(models.Model):
    """Contact model."""

    name = models.CharField(max_length=50)
    email = models.EmailField(blank=False)
    message = models.TextField()
    date = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.name} sent a message.'
