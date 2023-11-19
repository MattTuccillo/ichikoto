from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
