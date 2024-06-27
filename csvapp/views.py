from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import GroundTruth, Prediction, GroundTruthClass, GroundTruthInput, EmbeddingModels, ClassEmbeddings
from .forms import CSVUploadForm, PredictionForm, EmbeddingModelForm, ModelSelectionForm
from sentence_transformers import SentenceTransformer, models


import csv
from io import TextIOWrapper, StringIO
import pandas as pd
def index(request):
    return render(request, 'csvapp/index.html')

def delete_ground_truth(request):
    if request.method == 'POST':
        GroundTruth.objects.all().delete()
        return redirect('index')
    return render(request, 'csvapp/confirm_delete.html', {'table': 'GroundTruth'})

def delete_prediction(request):
    if request.method == 'POST':
        Prediction.objects.all().delete()
        return redirect('index')
    return render(request, 'csvapp/confirm_delete.html', {'table': 'Prediction'})

def delete_all(request):
    if request.method == 'POST':
        GroundTruth.objects.all().delete()
        GroundTruthClass.objects.all().delete()
        GroundTruthInput.objects.all().delete()
        Prediction.objects.all().delete()
#        EmbeddingModels.objects.all().delete()
        ClassEmbeddings.objects.all().delete()
        return redirect('index')
    return render(request, 'csvapp/confirm_delete.html', {'table': 'All'})
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Ensure 'csv_file' is in request.FILES
            if 'csv_file' not in request.FILES:
                form.add_error('csv_file', 'This field is required.')
            else:
                try:
                    # Read the CSV file into a Pandas DataFrame
                    df = pd.read_csv(request.FILES['csv_file']).drop_duplicates().dropna()
                    df_class=df[['classification']].drop_duplicates()
                    instances = [GroundTruthClass(classification=row['classification']) for index, row in df_class.iterrows()]
                    GroundTruthClass.objects.bulk_create(instances)
                    instances = [GroundTruthInput(input=row['input']) for index, row in df.iterrows()]
                    GroundTruthInput.objects.bulk_create(instances)      
                    # Example: Process the DataFrame (print first few rows)
                    instances = [GroundTruth(input_id=row['input'], classification_id=row['classification']) for index, row in df.iterrows()]                   
                    GroundTruth.objects.bulk_create(instances)

                except UnicodeDecodeError:
                    csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='latin1')
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        GroundTruth.objects.create(
                            input=row['input'],
                            classification=row['classification'],
                            category=row['category']
                        )
                return redirect('ground_truth_list')
    else:
        form = CSVUploadForm()
    return render(request, 'csvapp/upload_csv.html', {'form': form})


def ground_truth_list(request):
    ground_truths = GroundTruth.objects.all()
    paginator = Paginator(ground_truths, 50)  # Show 10 ground truths per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'csvapp/ground_truth_list.html', {'page_obj': page_obj})

def prediction_update(request, pk):
    prediction = get_object_or_404(Prediction, pk=pk)
    if request.method == 'POST':
        form = PredictionForm(request.POST, instance=prediction)
        if form.is_valid():
            form.save()
            return redirect('prediction_list')
    else:
        form = PredictionForm(instance=prediction)
    return render(request, 'csvapp/prediction_form.html', {'form': form, 'prediction': prediction})

def prediction_list(request):
    predictions = Prediction.objects.all()
    return render(request, 'csvapp/prediction_list.html', {'predictions': predictions})

# Create your views here.
def add_model(request):
    if request.method == 'POST':
        form = EmbeddingModelForm(request.POST)
        if form.is_valid():
            form.save()
            # Handle success or redirect
    else:
        form = EmbeddingModelForm()
    return render(request, 'csvapp/model_choice.html', {'form': form})

def list_embedding_models(request):
    embedding_models = EmbeddingModels.objects.all()
    return render(request, 'csvapp/list_embedding_models.html', {'embedding_models': embedding_models})
def embedding_task(request):
    if request.method == 'POST':
        form = ModelSelectionForm(request.POST)
        if form.is_valid():
            selected_model = form.cleaned_data['model']
            
            # Retrieve all ground truth classifications
            classifications = GroundTruthClass.objects.all()
            
            # Perform embedding using SentenceTransformer
            model_name = selected_model.name
            embedding_model = SentenceTransformer(model_name)
            
            embedding_results = []
            for classification in classifications:
                text_to_embed = classification.classification
                embedding_vector = embedding_model.encode([text_to_embed])[0].tolist()
                
                # Save the embedding result to EmbeddingResult table
                embedding_result = ClassEmbeddings.objects.create(
                    classification=classification,
                    model=selected_model,
                    embedding_vector=embedding_vector
                )
                embedding_results.append(embedding_result)
            
            return render(request, 'csvapp/embedding_results.html', {'results': embedding_results})
    else:
        form = ModelSelectionForm()
    
    return render(request, 'csvapp/select_model.html', {'form': form})