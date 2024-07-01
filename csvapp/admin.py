from django.contrib import admin

# Register your models here.
from .models import VinputEmbeddingWithCategory, VclassEmbeddingWithCategory
admin.site.register(VinputEmbeddingWithCategory)
admin.site.register(VclassEmbeddingWithCategory)

