from django.urls import path
from . import views 
from .views import my_lists # LYSS: needed to add this for my added path

urlpatterns = [
    path("", views.index, name="index"), # CORINNE JUL 10: homepage path
    path("search/", views.search_results, name="search_results"), # CORINNE JUL 10: search results path
    path("clear-history/", views.clear_search_history, name="clear_search_history"), # CORINNE JUL 10: clear search history path
    path("accounts/login/", views.login_view, name="login_view"), # CORINNE JUL 11: login view path
    path("accounts/signup/", views.signup_view, name="signup_view"), # CORINNE JUL 11: signup view path
    path("accounts/logout/", views.logout_view, name="logout_view"), # CORINNE JUL 11: logout view path
    path("my-lists/", my_lists, name="my_lists"), # LYSS: Added this path for my lists!

]


