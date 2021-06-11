from django.urls import path
from Main import views


urlpatterns = [
    path('schemas', views.schemas),
    path('new_schema', views.new_schema),
    path('dataset_table', views.dataset_table),
    path('download', views.download),
    path('', views.fakecsv)
]
