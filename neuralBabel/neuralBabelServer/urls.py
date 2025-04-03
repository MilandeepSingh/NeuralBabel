from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.fetch_profile, name='fetch_profile'),
    path('words/<str:language_name>/', views.fetch_words_for_language, name='fetch_words_for_language'),
    path('add_existing_language_to_user/<str:language_name>/', views.add_existing_language_to_user, name='add_existing_language_to_user'),
    path('associate_word_with_user/<str:language_name>/<str:word>/', views.associate_word_with_user, name='associate_word_with_user'),
]