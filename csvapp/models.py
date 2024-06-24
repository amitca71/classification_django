from django.db import models

class GroundTruth(models.Model):
    input = models.CharField(max_length=200)
    classification = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.input

class Prediction(models.Model):
    input = models.CharField(max_length=200)
    predicted = models.CharField(max_length=100)
    fixed_prediction = models.CharField(max_length=100, blank=True)
    probability = models.FloatField()

    def __str__(self):
        return self.input

# Create your models here.
