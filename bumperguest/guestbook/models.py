from django.db import models
from ulid import ULID


class Guest(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Entry(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ulid = models.CharField(max_length=26, unique=True)

    class Meta:
        indexes = [
            # models.Index(fields=["guest"]), # not needed because Django creates an index for ForeignKey fields
            # models.Index(fields=["ulid"]), # not needed because Django creates an index for unique fields
            models.Index(fields=["created_at"]), # because we sometimes sort by created_at
        ]

    def save(self, *args, **kwargs):
        # Generate a ULID only if this is a new instance or the ULID is not set
        if not self.ulid:
            self.ulid = str(ULID())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subject
