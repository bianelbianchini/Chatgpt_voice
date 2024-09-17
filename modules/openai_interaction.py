# modules/openai_interaction.py
import openai

def configure_openai(api_key):
    openai.api_key = api_key

def get_openai_response(context, user_message):
    context.append({"role": "user", "content": user_message})
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=context
    )
    return response.choices[0].message.content

def build_context(conversations):
    context = []
    for conv in conversations:
        context.append({"role": "user", "content": conv["user_message"]})
        context.append({"role": "assistant", "content": conv["bot_response"]})
    return context