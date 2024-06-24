from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import GroundTruth, Prediction
from .forms import CSVUploadForm, PredictionForm
import csv
from io import TextIOWrapper
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

def delete_both(request):
    if request.method == 'POST':
        GroundTruth.objects.all().delete()
        Prediction.objects.all().delete()
        return redirect('index')
    return render(request, 'csvapp/confirm_delete.html', {'table': 'Both'})
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Ensure 'csv_file' is in request.FILES
            if 'csv_file' not in request.FILES:
                form.add_error('csv_file', 'This field is required.')
            else:
                try:
                    file = request.FILES['csv_file']
                    decoded_file = file.read().decode('utf-8').splitlines()
                    reader = csv.reader(decoded_file)
                    next(reader)  # Skip the header row
                    for row in reader:
                        GroundTruth.objects.create(input=row[0], classification=row[1], category=row[2])
#                    csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
#                    reader = csv.DictReader(csv_file)
#                    for row in reader:
#                        GroundTruth.objects.create(
#                            input=row[0],
#                            classification=row['classification'],
#                            category=row['category']
#                        )
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

#def upload_csv(request):
#   if request.method == 'POST':
#        form = CSVUploadForm(request.POST, request.FILES)
#        if form.is_valid():
#            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
#            reader = csv.DictReader(csv_file)
#            for row in reader:
#                GroundTruth.objects.create(
#                    input=row[0],
#                    classification=row[1],
#                    category=row[2]
#                )
#            return redirect('ground_truth_list')
#   else:
#        form = CSVUploadForm()
#   return render(request, 'csvapp/upload_csv.html', {'form': form})
#def upload_csv(request):
#    if request.method == 'POST':
#        form = CSVUploadForm(request.POST, request.FILES)
#        if form.is_valid():
#            file = request.FILES['file']
#            decoded_file = file.read().decode('utf-8').splitlines()
#            reader = csv.reader(decoded_file)
#            next(reader)  # Skip the header row
#            for row in reader:
#                GroundTruth.objects.create(input=row[0], cls=row[1], category=row[2])
#            return redirect('ground_truth_list')
#    else:
#        form = CSVUploadForm()
#    return render(request, 'csvapp/upload_csv.html', {'form': form})
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
