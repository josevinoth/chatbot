from django.urls import path
from . import views
from django.contrib.auth import views as auth_views #import this
urlpatterns = [
    path("text_command/", views.text_command, name="text_command"),
    path("voice-command/", views.voice_command, name="voice_command"),
    path("nlp_view/", views.nlp_view, name="nlp_view"),

]