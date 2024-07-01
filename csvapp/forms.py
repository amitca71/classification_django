from django import forms
from .models import  GroundTruth, EmbeddingModels
import json

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

#class PredictionForm(forms.ModelForm):
#    class Meta:
#        model = Prediction
#        fields = ['input', 'predicted', 'fixed_prediction', 'probability']
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.fields['fixed_prediction'].queryset = GroundTruth.objects.values_list('classification', flat=True).distinct()

class EmbeddingModelForm(forms.ModelForm):
    class Meta:
        model = EmbeddingModels
        fields = ['name', 'size', 'technology']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ModelSelectionForm(forms.Form):
    model = forms.ModelChoiceField(queryset=EmbeddingModels.objects.all())