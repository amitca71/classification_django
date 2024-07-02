from django.urls import path
from .views import upload_csv, ground_truth_list,index, prediction_list,delete_ground_truth, delete_all,list_embedding_models, add_model, embedding_task, predict

urlpatterns = [
    path('', index, name='index'),  # Default route
    path('upload_csv/', upload_csv, name='upload_csv'),
    path('ground_truth/', ground_truth_list, name='ground_truth_list'),
    path('predictions/', prediction_list, name='prediction_list'),
#    path('predictions/update/<int:pk>/', prediction_update, name='prediction_update'),
    path('delete_ground_truth/', delete_ground_truth, name='delete_ground_truth'),
#    path('delete_prediction/', delete_prediction, name='delete_prediction'),
    path('delete_all/', delete_all, name='delete_all'),
    path('add_model/', add_model, name='add_model'),
    path('list_embedding_models/', list_embedding_models, name='list_embedding_models'),
    path('select_model/', embedding_task, name='select_model'),
    path('predict/', predict, name='predict'),
]

