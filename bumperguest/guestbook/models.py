from django.db import models


class Guest(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Entry(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
