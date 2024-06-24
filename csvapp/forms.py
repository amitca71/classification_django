from django import forms
from .models import Prediction, GroundTruth

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['input', 'predicted', 'fixed_prediction', 'probability']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fixed_prediction'].queryset = GroundTruth.objects.values_list('classification', flat=True).distinct()

