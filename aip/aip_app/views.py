from django.shortcuts import render

# Create your views here.
from .sub_views.intent_view import process_command,text_command,voice_command
from .sub_views.text_process import text_command
from .sub_views.NLP import nlp_query_processor,nlp_view,format_table