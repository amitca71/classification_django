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
    class Meta:
        db_table = 'ground_truth' 
        unique_together = ('input', 'classification')
    def __str__(self):
        return self.input
class EmbeddingModels(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    size = models.IntegerField(choices=[(384, "384 dimensions"), (768, "768 dimensions")], blank=True)  # Choices will be populated dynamically
    technology = models.CharField(max_length=50, choices=[("SentenceTransformer", "SentenceTransformer (hugging face)")], blank=True)  # Choices will be populated dynamically
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'embedding_models' 

class ClassEmbeddings(models.Model):
    classification = models.ForeignKey(GroundTruthClass, on_delete=models.CASCADE)
    model = models.ForeignKey(EmbeddingModels, on_delete=models.CASCADE)
    embedding_vector = VectorField(dimensions=384)
    class Meta:
        db_table = 'class_embedding'     
        unique_together = ('classification', 'model')

class InputEmbeddings(models.Model):
    input = models.ForeignKey(GroundTruthInput, on_delete=models.CASCADE)
    model = models.ForeignKey(EmbeddingModels, on_delete=models.CASCADE)
    embedding_vector = VectorField(dimensions=384)
    class Meta:
        db_table = 'input_embedding'     
        unique_together = ('input', 'model')
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
