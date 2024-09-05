from django.http import JsonResponse
from django.shortcuts import render
from functools import wraps

from django.views import View

class CheckSessionAuthentication:
    def __init__(self, request):
        self.session_id = request.COOKIES.get('sessionid')
        self.cookies = request.COOKIES
        print("request.COOKIES.get:",self.session_id)
        print("cookies ",self.cookies)

    def authenticate(self):
        if self.session_id:
            print("session valid")
            # Если сессия существует, возвращаем True для аутентификации
            return True
        else:
            print("session not valid")
            # Если сессия не существует, возвращаем False для отказа в аутентификации
            return False

def login_view(request):
    return render(request, 'login-form.html')

# Create your views here.


def user_profile(request, username):
    session_auth = CheckSessionAuthentication(request)
    if session_auth.authenticate():
        # Если аутентификация прошла успешно, продолжаем выполнение
        print("Authentication successful")
        return render(request, 'main-page.html', {'username': username})

    else:
        # Если аутентификация не удалась, возвращаем сообщение об ошибке
        print("Authentication failed")
        return JsonResponse({'status': 'error', 'message': 'Authentication failed'}, status=401)






