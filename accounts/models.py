from django.db import models
from django.utils import timezone


# Create Leads Model (DB Table).
class Leads(models.Model):
    time_stamp = models.DateTimeField(default=timezone.now, blank=False)
    email_address = models.EmailField(unique=True)

    class Meta:
        verbose_name_plural = "Leads"

    def __str__(self):
        return self.email_address
