import os
from django.conf import settings
from langchain_groq import ChatGroq
from markdown import markdown

os.environ['GROQ_API_KEY'] = settings.GROQ_API_KEY

def get_chat_history(chats):
    chat_history = []
    for chat in chats:
        chat_history.append(('human', chat.message))
        chat_history.append(('ai', chat.response))
    return chat_history

def ask_ai(context, message):
    model = ChatGroq(model='llama-3.2-90b-vision-preview')
    
    messages = [
        (
            'system',
            'Você é um assistente responsável responder dúvidas sobre assuntos diversos dos usúarios'
            'Seja educado e respeitoso'
            'Responda em formato markdown.'
        ),
    ]

    if context:
        messages.extend(context)
    
    messages.append(('human', message))

    print(messages)

    response = model.invoke(messages)
    return markdown(response.content, output_format='html')
