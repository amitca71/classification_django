from django.shortcuts import render, redirect, get_object_or_404
from django.apps import apps
from pgvector.django import L2Distance
from django.db.models import Count, CharField, Value, aggregates, fields
from django.contrib.postgres.aggregates import ArrayAgg



from django.core.paginator import Paginator
from .models import GroundTruth, GroundTruthClass, GroundTruthInput, EmbeddingModels, ClassEmbeddings, InputEmbeddings, VinputEmbeddingWithCategory, VclassEmbeddingWithCategory, Prediction
from .forms import CSVUploadForm, EmbeddingModelForm, ModelSelectionForm
from sentence_transformers import SentenceTransformer, models


import csv
from io import TextIOWrapper, StringIO
import pandas as pd
def index(request):
#    results=VinputEmbeddingWithCategory.objects.filter(category='Other').values('category', 'content_id', 'content_tsvector', 'embedding')
#    print (results[1])
#    Item.objects.order_by(L2Distance('embedding', [3, 1, 2]))[:5]
    return render(request, 'csvapp/index.html')

def delete_ground_truth(request):
    if request.method == 'POST':
        GroundTruth.objects.all().delete()
        return redirect('index')
    return render(request, 'csvapp/confirm_delete.html', {'table': 'GroundTruth'})

#def delete_prediction(request):
#    if request.method == 'POST':
#        Prediction.objects.all().delete()
#        return redirect('index')
#    return render(request, 'csvapp/confirm_delete.html', {'table': 'Prediction'})

def delete_all(request):
    if request.method == 'POST':
#        GroundTruth.objects.all().delete()
#        GroundTruthClass.objects.all().delete()
#        GroundTruthInput.objects.all().delete()
#        Prediction.objects.all().delete()
#        EmbeddingModels.objects.all().delete()
        ClassEmbeddings.objects.all().delete()
        InputEmbeddings.objects.all().delete()
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
                    instances = [GroundTruthClass(content=row['classification']) for index, row in df_class.iterrows()]
                    GroundTruthClass.objects.bulk_create(instances)
                    instances = [GroundTruthInput(content=row['input']) for index, row in df.iterrows()]
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

#def prediction_update(request, pk):
#    prediction = get_object_or_404(Prediction, pk=pk)
#    if request.method == 'POST':
#        form = PredictionForm(request.POST, instance=prediction)
#        if form.is_valid():
#            form.save()
#            return redirect('prediction_list')
#    else:
#        form = PredictionForm(instance=prediction)
#    return render(request, 'csvapp/prediction_form.html', {'form': form, 'prediction': prediction})

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


def create_dynamic_instance(model_name, field_values, create_instance=True):
    try:
        # Retrieve the model dynamically
        model_class = apps.get_model(app_label='csvapp', model_name=model_name.__name__)

        # Create an instance of the model dynamically
        if(create_instance):
            instance = model_class.objects.create(**field_values)
        else:
            instance = model_class(**field_values)
        return instance  # Optionally return the created instance

    except AttributeError:
        print(f"Model '{model_name}' does not exist.")

########################################################
def create_embeddings(source_entity, destination_entity,source_column_name, selected_model,embedding_model):
    embedding_results = []
    in_records_lst = source_entity.objects.all()
    for record in in_records_lst:
        embedding_vector = embedding_model.encode([getattr(record, source_column_name)])[0].tolist()
        field_values = {
            source_column_name: record,
            'model': selected_model,
            'embedding': embedding_vector
        }    
        embedded_record=create_dynamic_instance(destination_entity, field_values)
        print(embedded_record)
#bulk not used because vector will not be created
        embedding_results.append(embedded_record)
#    destination_entity.objects.bulk_create(embedding_results)
    return(embedding_results)

################################################
def embedding_task(request):
    if request.method == 'POST':
        form = ModelSelectionForm(request.POST)
        if form.is_valid():
            selected_model = form.cleaned_data['model']
            model_name = selected_model.name
            embedding_model = SentenceTransformer(model_name)
            embedding_results=create_embeddings(GroundTruthInput, InputEmbeddings,'content', selected_model, embedding_model )
            embedding_results=create_embeddings(GroundTruthClass, ClassEmbeddings,'content', selected_model, embedding_model )
            return render(request, 'csvapp/embedding_results.html', {'results': embedding_results})
    else:
        form = ModelSelectionForm()
    return render(request, 'csvapp/select_model.html', {'form': form})


################################################
def predict(request):
    if request.method == 'GET':
        prediction_list=[]
        queryset = VinputEmbeddingWithCategory.objects.values(
            'id', 'content_id', 'model_id', 'embedding'
        ).annotate(
            categories=ArrayAgg('category', distinct=True)
        )
        # Execute the query and fetch results
        results = list(queryset)

        # Print or process the results
        for result in results:
            print(f"ID: {result['id']}, Content ID: {result['content_id']}, Model ID: {result['model_id']}, Categories: {result['categories']}")
            queryset_cat = VclassEmbeddingWithCategory.objects.filter(
            model_id=result['model_id'],
            category__in=result['categories']
            ).annotate(
                embedding_diff=L2Distance('embedding', result['embedding'])
            ).order_by('embedding_diff').values_list('content_id', flat=True)[:2]
            results_cats = list(queryset_cat)
            gt_input = GroundTruthInput.objects.filter(content=result['content_id']).first()

            field_values = {
                "input": gt_input,
                "model_id": result['model_id'],
                "categories_array": result['categories'],
                "predictedion_array": results_cats,

            }    
            prediction_record=create_dynamic_instance(Prediction, field_values, create_instance=False)
            prediction_list.append(prediction_record)
        Prediction.objects.bulk_create(prediction_list)
        return redirect('index')
    return render(request, 'csvapp/prediction_list.html', {'table': 'All'})