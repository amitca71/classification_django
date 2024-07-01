from django.db import models, connection
from pgvector.django import VectorField
from django.db.models.signals import post_save
from django.dispatch import receiver
class GroundTruthClass(models.Model):
    content = models.CharField(max_length=300, primary_key=True)
#    embedding = models.JSONField()
    class Meta:
        db_table = 'ground_truth_classes' 
    def __str__(self):
        return self.content
class GroundTruthInput(models.Model):
    content = models.CharField(max_length=300, primary_key=True) 
#    c = models.JSONField()
    class Meta:
        db_table = 'ground_truth_input' 
    def __str__(self):
        return self.content

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
    content = models.ForeignKey(GroundTruthClass, on_delete=models.CASCADE)
    model = models.ForeignKey(EmbeddingModels, on_delete=models.CASCADE)
    embedding = VectorField(dimensions=384)
    class Meta:
        db_table = 'class_embedding'     
        unique_together = ('content', 'model')
@receiver(post_save, sender=ClassEmbeddings)
def update_ts_class_vector(sender, instance, created, **kwargs):
    print ("in update_ts_input_vector")
    if created:
        sql = """
            UPDATE class_embedding
            SET content_tsvector = to_tsvector('yiddish', content_id)
            WHERE id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [instance.id])
class InputEmbeddings(models.Model):
    content = models.ForeignKey(GroundTruthInput, on_delete=models.CASCADE)
    model = models.ForeignKey(EmbeddingModels, on_delete=models.CASCADE)
    embedding = VectorField(dimensions=384)
    class Meta:
        db_table = 'input_embedding'     
        unique_together = ('content', 'model')
@receiver(post_save, sender=InputEmbeddings)
def update_ts_input_vector(sender, instance, created, **kwargs):
    print ("in update_ts_input_vector")
    if created:
        sql = """
            UPDATE input_embedding
            SET content_tsvector = to_tsvector('yiddish', content_id)
            WHERE id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [instance.id])
#class Prediction(models.Model):
#    input = models.CharField(max_length=200)
#    predicted = models.CharField(max_length=100)
#    fixed_prediction = models.CharField(max_length=100, blank=True)
#    probability = models.FloatField()
#    embedding = models.JSONField()
#    class Meta:
#        db_table = 'prediction' 
#    def __str__(self):
#        return self.input
class CategoryHint(models.Model):
    ts_word = models.CharField(max_length=30, primary_key=True)
    category = models.CharField(max_length=30)
    class Meta:
        db_table = 'category_hint' 
    def __str__(self):
        return self.ts_word

# Create your models here.
class VinputEmbeddingWithCategory(models.Model):
    category = models.CharField(max_length=30)
    content_id = models.CharField(max_length=300)
    embedding = VectorField(dimensions=384)
    content_tsvector = models.TextField() 

    class Meta:
        managed = False  # This ensures Django does not manage this model's table
        db_table = 'v_input_embedding_with_category' 

class VclassEmbeddingWithCategory(models.Model):
    category = models.CharField(max_length=30)
    content_id = models.CharField(max_length=300)
    embedding = VectorField(dimensions=384)
    content_tsvector = models.TextField() 

    class Meta:
        managed = False  # This ensures Django does not manage this model's table
        db_table = 'v_class_embedding_with_category' 