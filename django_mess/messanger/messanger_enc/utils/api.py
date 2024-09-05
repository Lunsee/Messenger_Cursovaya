from cryptography.fernet import Fernet
from django.http import JsonResponse, HttpResponse
import uuid
from django.shortcuts import redirect
from django.conf import settings
from functools import wraps
from ..views import CheckSessionAuthentication
from django.contrib.auth.models import User
from django.db import connection
import base64


key = b'bYg9iF2P8HD3E5JnUYWpA1vPbS34C7OaJ8NlX9aDrF0='
print(key)

def submit_data_reg(request):
    if request.method == 'POST':
        print("POST reg HTTP TRUE")
        data = request.POST
        print(f"data: {data}")
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not CheckAvailableUsers_in_DB(username):
            print("This username not busy!")
            try:
                # Создаем нового пользователя
                user = User.objects.create_user(username=username, password=password)
                return JsonResponse({'status': 'success', 'message': 'User created successfully'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        else:
            return JsonResponse({'status': 'error', 'message': 'This Username is busy'}, status=405)
    else:
        return JsonResponse({'status': 'error', 'message': 'Method POST not allowed'}, status=405)




def check_user(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        print(f"имя которое мы проверяем: {username}")
        user_exists = User.objects.filter(username=username).exists()
        print(f"результат проверки: {user_exists}")
        return JsonResponse({'exists': user_exists})


import traceback


def Send_Message_Control(request):
    if request.method == 'POST':
        print("Send_Message_Control working")
        data = request.POST
        print(f"data: {data}")
        second_user = data.get('second_username')
        sender = data.get('my_username')
        message = data.get('message_to_sec_user')

        # Получаем имя таблицы для диалога
        table_name = get_dialog_table_name(sender, second_user)
        print(f"table_name: {table_name}")

        try:
            cursor = connection.cursor()
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sender VARCHAR(255),
                    receiver VARCHAR(255),
                    message TEXT,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """

            print(f"Create table query: {create_table_query}")
            cursor.execute(create_table_query)

            encrypted_message = encrypt_message(message, key)

            # Вставляем сообщение в таблицу
            insert_query = f"""
                INSERT INTO {table_name} (sender, receiver, message)
                VALUES (%s, %s, %s)
            """
            print(f"Insert query: {insert_query}")
            cursor.execute(insert_query, (sender, second_user, encrypted_message))
            print("Insert query done!")
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            traceback.print_exc()  # Логируем трейсбек
            print(f"An error occurred while creating a database cursor: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        return JsonResponse({'status': 'error', 'message': 'Method POST not allowed'}, status=405)




def get_message_history(request):
    if request.method == 'POST':
        print("get_message_history working")
        sender = request.POST.get('sender')
        second_user = request.POST.get('secondUser')
        try:
            cursor = connection.cursor()

            # Выбираем сообщения из таблицы
            query = f"""
                SELECT sender, message, sent_at
                FROM {get_dialog_table_name(sender, second_user)}
                WHERE sender = %s OR receiver = %s
                ORDER BY sent_at ASC
            """
            cursor.execute(query, (sender, sender))

            messages_list = []
            for row in cursor.fetchall():
                sender, message, sent_at = row
                message_dict = {
                    'sender': sender,
                    'message': decrypt_message(message, key),
                    'sent_at': sent_at.strftime('%Y-%m-%d %H:%M:%S')  # Форматируем время отправки
                }
                messages_list.append(message_dict)

            return JsonResponse(messages_list, safe=False)
        except Exception as e:
            print(f"An error occurred while fetching message history: {e}")
            return JsonResponse({'error': 'Ошибка при получении истории сообщений'}, status=500)
    else:
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)





def submit_data_log(request):
    if request.method == 'POST':
        print("POST log HTTP TRUE")
        data = request.POST
        print("log data")
        print(f"data: {data}")
        username = data.get('username')
        password = data.get('password')
        if check_login_user_data(username,password): #функция которая сверяет данные с бд
            session_id = unique_session_id_generator()  # Здесь нужно сгенерировать уникальный идентификатор сессии
            request.session['session_id'] = session_id #отправка id session  на клиент
            print(f"session_id:{session_id}")
            session_auth = CheckSessionAuthentication(request)
            if session_auth.authenticate():
                # Если аутентификация прошла успешно, продолжаем выполнение
                print("Authentication successful")
                current_url = request.build_absolute_uri()
                # print("redirect:",redirect(f'/{username}/'))
                print("current_url", current_url)
                new_url = current_url.replace('/submit_data_log/', f'/{username}/')
                print("redirect:", new_url)
                return HttpResponse(status=302, headers={'Location': new_url})
            else:
                print("Authentication failed")
                return JsonResponse({'status': 'error', 'message': 'Authentication failed'}, status=401)


        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid username or password'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Method POST not allowed'}, status=405)



def check_login_user_data(username, password):
    try:
        # Пытаемся найти пользователя с указанным именем пользователя (username)
        user = User.objects.get(username=username)
        # Проверяем, соответствует ли введенный пароль хэшированному паролю пользователя
        if user.check_password(password):
            print("password is True for this user")
            return True  # Пароль верный
        else:
            print("password is False for this user")
            return False  # Пароль неверный
    except User.DoesNotExist:
        return False  # Пользователь с указанным именем пользователя не найден

def unique_session_id_generator():
    print("get unique session id..")
    return str(uuid.uuid4())

def CheckAvailableUsers_in_DB(username):
    return User.objects.filter(username=username).exists()


def get_dialog_table_name(user1, user2):
    print("формируется имя таблицы..")
    # Формируем имя таблицы, упорядочивая имена пользователей лексикографически
    return f"dialog_{sorted([user1, user2])[0]}_{sorted([user1, user2])[1]}"




# Шифрование
def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

# Дешифрование
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

