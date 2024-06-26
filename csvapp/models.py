from django.db import models
from pgvector.django import VectorField

class GroundTruthClass(models.Model):
    classification = models.CharField(max_length=300, primary_key=True)
#    embedding = models.JSONField()
    class Meta:
        db_table = 'ground_truth_classes' 
    def __str__(self):
        return self.classification
class GroundTruthInput(models.Model):
    input = models.CharField(max_length=300, primary_key=True) 
#    embedding = models.JSONField()
    class Meta:
        db_table = 'ground_truth_input' 
    def __str__(self):
        return self.input

class GroundTruth(models.Model):
    input = models.ForeignKey(GroundTruthInput, on_delete=models.CASCADE)
    classification = models.ForeignKey(GroundTruthClass, on_delete=models.CASCADE)
#    category = models.CharField(max_length=100)
#    embedding = models.JSONField()
    class Meta:
        db_table = 'ground_truth' 
        unique_together = ('input', 'classification')
    def __str__(self):
        return self.input

class Prediction(models.Model):
    input = models.CharField(max_length=200)
    predicted = models.CharField(max_length=100)
    fixed_prediction = models.CharField(max_length=100, blank=True)
    probability = models.FloatField()
    embedding = models.JSONField()
    class Meta:
        db_table = 'prediction' 
    def __str__(self):
        return self.input

# Create your models here.
