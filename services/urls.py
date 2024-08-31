from django.urls import path 
from . import views 

urlpatterns = [
    path("search-buses", views.SearchBuses.as_view()),
    path("block", views.Block.as_view()),
    path("book", views.BookBus.as_view())
]