from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr
from pydub import AudioSegment


# Predefined intents and responses
INTENTS = {
    "show poorly performing machine": "Redirecting to poorly performing machines page...",
    "find my cell status": "Fetching the cell status...",
    "show me all parts with high rejection": "Redirecting to high rejection parts page...",
    "show me all machines with high cycle time": "Fetching machines with high cycle time...",
    "show me all machines with higher downtime since 10 AM": "Showing machines with higher downtime since 10 AM...",
    "why am I facing this servo failure frequently in my cnc machine": "Analyzing frequent servo failures...",
    "show me machines with non productive energy consuming machines": "Showing machines with non-productive energy consumption...",
}

def process_command(command):
    """
    Process the user's command and map it to an intent.
    """
    command = command.lower()
    for intent in INTENTS:
        if intent in command:
            return INTENTS[intent]
    return "Sorry, I didn't understand that command."


from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from pydub import AudioSegment
import speech_recognition as sr
import json


def process_command(command):
    """
    Mock function to process a command.
    Replace this with actual command processing logic.
    """
    return f"Processed command: {command}"


def text_command(request):
    """
    Handle text commands sent via POST.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            command = data.get("command", "")
            if not command:
                return JsonResponse({"response": "No text command provided."})
            # Process the text command
            response = f"Received and processed text command: {command}"
            return JsonResponse({"response": response})
        except json.JSONDecodeError:
            return JsonResponse({"response": "Invalid JSON data."})
    return JsonResponse({"response": "Invalid request method."})


@csrf_exempt
def voice_command(request):
    """
    Handle voice commands sent via POST with a WAV file.
    """
    if request.method == "POST" and "audio" in request.FILES:
        recognizer = sr.Recognizer()
        audio_file = request.FILES["audio"]
        try:
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
            command = recognizer.recognize_google(audio)
            response = f"Received and processed voice command: {command}"
            return JsonResponse({"response": response})
        except sr.UnknownValueError:
            return JsonResponse({"response": "Voice command not recognized."})
        except sr.RequestError:
            return JsonResponse({"response": "Speech recognition service is unavailable."})
        except Exception as e:
            return JsonResponse({"response": f"Error processing voice input: {str(e)}"})
    return JsonResponse({"response": "Invalid request or no audio file provided."})

