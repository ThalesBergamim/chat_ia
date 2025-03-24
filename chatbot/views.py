from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from chatbot.models import Chat
from langchain_groq import ChatGroq
from markdown import markdown
from django.conf import settings
import os

os.environ['GROQ_API_KEY'] = settings.GROQ_API_KEY

def ask_ai(message):
    model = ChatGroq(model='llama-3.2-90b-vision-preview')
    messages = [
        (
            'system',
            'Você é um assistente responsável por tirar dúvidas sobre assuntos diversos.'             
            'Respoda com educação'
            'Responda em formato markdown.'
        ),
        (
            'human',
            message,
        ),
    ]
    response = model.invoke(messages)
    return markdown(response.content, output_format='html')

def get_chat_history(chats):
    chat_history = []
    for chat in chats:
        chat_history.append(
            ('human', chat.message,)
        )
        chat_history.append(
            ('ai', chat.response,)
        )
    return chat_history

class ChatbotView(View):
    def get(self, request):
        chats = Chat.objects.all()
        return render(request, 'chatbot.html', {'chats': chats})

    def post(self, request):
        context = get_chat_history(
            chats=Chat.objects.all()
        )
        
        message = request.POST.get('message')

        response = ask_ai(
            message=message,
            context=context,
        )
        
        chat = Chat(
            message=message,
            response=response,
        )
        
        chat.save()

        return JsonResponse({'message': message, 'response': response})