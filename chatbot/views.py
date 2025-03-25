from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from chatbot.models import Chat
from ia_assistence.utils import ask_ai, get_chat_history
from django.contrib.auth.mixins import LoginRequiredMixin


class ChatbotView(LoginRequiredMixin, View):
    def get(self, request):
        chats = Chat.objects.filter(user=request.user)
        return render(request, 'chatbot.html', {'chats': chats})

    def post(self, request):
        context = get_chat_history(
            chats = Chat.objects.filter(user=request.user)
        )
        
        message = request.POST.get('message')

        response = ask_ai(
            message=message,
            context=context,
        )
        
        chat = Chat(
            user=request.user,
            message=message,
            response=response,
        )
        
        chat.save()

        return JsonResponse({'message': message, 'response': response})