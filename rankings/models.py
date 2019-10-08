from django.db import models

# Create your models here.

class Hacker(models.Model):
	name = models.CharField(max_length=300)
	score = models.FloatField()
	time = models.FloatField()

