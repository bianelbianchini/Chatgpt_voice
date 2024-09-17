# modules/voice.py
import speech_recognition as sr
import pyttsx3

def get_microphone():
    return sr.Microphone()

def recognize_speech_from_mic(microphone, timeout=10, phrase_time_limit=None):
    recognizer = sr.Recognizer()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Escuchando...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("Reconociendo...")
            response = recognizer.recognize_google(audio, language="es-ES")
            return response
        except sr.WaitTimeoutError:
            print("No se recibió ninguna respuesta. Esperando...")
        except sr.RequestError:
            print("API de reconocimiento de voz no disponible.")
            return None
        except sr.UnknownValueError:
            print("No se pudo reconocer el habla.")
            return None

def speak_text(text):
    engine = pyttsx3.init()

    # Obtener todas las voces disponibles
    voices = engine.getProperty('voices')

    # Mostrar todas las voces disponibles para verificar
    for voice in voices:
        print(f"Voz: {voice.name}, ID: {voice.id}")

    # Seleccionar la voz de Microsoft Sabina o Helena (primero Sabina, si no, Helena)
    for voice in voices:
        if "Microsoft Sabina" in voice.name:
            engine.setProperty('voice', voice.id)
            print(f"Usando voz: {voice.name}")
            break
        elif "Microsoft Helena" in voice.name:
            engine.setProperty('voice', voice.id)
            print(f"Usando voz: {voice.name}")
            break

    # Ajustar velocidad y volumen
    engine.setProperty('rate', 180)  # Ajustar velocidad según prefieras
    engine.setProperty('volume', 1.0)  # Volumen máximo

    # Decir el texto
    engine.say(text)
    engine.runAndWait()