from django.urls import path
from plains.views import *

urlpatterns = [
    # path('',home,name='home'),
    path('',PlainListView.as_view(),name='home'),
    #path('<int:pk>',home),
     path('detail/<int:pk>/',PlainDetailView.as_view(),name='detail'),
    path('update/<int:pk>/',PlainUpdateView.as_view(),name='update'),
    path('delete/<int:pk>/',PlainDeleteView.as_view(),name='delete'),
    path('add/',PlainCreateView.as_view(),name='create'),
    
]