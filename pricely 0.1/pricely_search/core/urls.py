from django.urls import path
from . import views
from .views import my_lists # LYSS: needed to add this for my added path

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search_results, name="search_results"),
    path("clear-history/", views.clear_search_history, name="clear_search_history"),
    path("my-lists/", my_lists, name="my_lists"), # LYSS: Added this path for my lists!
]


