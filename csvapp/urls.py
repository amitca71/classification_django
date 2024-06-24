from django.urls import path
from .views import upload_csv, ground_truth_list, prediction_list, prediction_update, index, delete_ground_truth, delete_prediction, delete_both

urlpatterns = [
    path('', index, name='index'),  # Default route
    path('upload_csv/', upload_csv, name='upload_csv'),
    path('ground_truth/', ground_truth_list, name='ground_truth_list'),
    path('predictions/', prediction_list, name='prediction_list'),
    path('predictions/update/<int:pk>/', prediction_update, name='prediction_update'),
    path('delete_ground_truth/', delete_ground_truth, name='delete_ground_truth'),
    path('delete_prediction/', delete_prediction, name='delete_prediction'),
    path('delete_both/', delete_both, name='delete_both'),
]

