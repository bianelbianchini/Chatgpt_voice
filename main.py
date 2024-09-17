# main.py
import os
from dotenv import load_dotenv
from modules import db, voice, openai_interaction

def interactive_terminal():
    print("Bienvenido a la terminal interactiva. Di 'Asistente' para activar y 'Eso es todo' para cerrar.")
    
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv()

    # Obtener la clave de API desde las variables de entorno
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"API Key: {api_key}")  # Verificar que la API Key se cargue correctamente

    if api_key is None:
        raise ValueError("La clave de API no se ha encontrado en las variables de entorno")

    # Configurar la clave de API para el cliente de OpenAI
    openai_interaction.configure_openai(api_key)

    microphone = voice.get_microphone()
    
    while True:
        print("Esperando la palabra clave...")
        trigger_word = voice.recognize_speech_from_mic(microphone, phrase_time_limit=5)
        if trigger_word and "asistente" in trigger_word.lower():
            first_response = "Sistema Activado. Estoy a vuestro servicio"
            print(first_response)
            voice.speak_text(first_response)
            context = openai_interaction.build_context(db.get_all_conversations())
            while True:
                user_message = voice.recognize_speech_from_mic(microphone, phrase_time_limit=None)
                if user_message is None:
                    continue
                if "eso es todo" in user_message.lower():
                    last_response = "Sistema Desactivado"
                    voice.speak_text(last_response)
                    print(last_response)
                    break
                print(f"Tú: {user_message}")
                bot_response = openai_interaction.get_openai_response(context, user_message)
                print(f"Bot: {bot_response}")
                voice.speak_text(bot_response)
                db.save_conversation(user_message, bot_response)
                context.append({"role": "user", "content": user_message})
                context.append({"role": "assistant", "content": bot_response})

if __name__ == "__main__":
    interactive_terminal()