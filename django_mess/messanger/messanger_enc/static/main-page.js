

    function showUsername() {
        var url = window.location.href;
        var pathSegments = url.split('/');
        var lastSegment = pathSegments[pathSegments.length - 2];
        console.log("showusername func val is ",lastSegment);
        document.getElementById("userName").textContent = lastSegment;
    }

    function CreateLocalStorage(sec_user){
        console.log("creating local storage..")
        localStorage.clear();
        localStorage.setItem('username_second', sec_user);
        var currentUrl = window.location.href;
        var parts = currentUrl.split("/");

        var lastPart = parts[parts.length - 2];
        console.log("check username sender:",lastPart);
        localStorage.setItem('sender', lastPart);
    }


    function SendMessageController() {
        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
        console.log("send message func working...")
        var data = {
            second_username: $('#userProfileName').text(),
            my_username: $('#userName').text(),
            message_to_sec_user: $('#messageForUser').val()
        };
        console.log("data:", data);
        $.ajax({
            url: '/Send_Message_Control/',
            type: 'POST',
            data: data,
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (response) {
                console.log("Server response:", response);
                $('#messageForUser').val('');
                loadMessageHistory();


            },
            error: function (xhr, status, error) {
                console.error('Произошла ошибка при проверке и поиска пользователя:', error);
            }
        });
    }

function Exit() {
     console.error('Выход из мессенджера..');
     document.cookie = "session_id=";
     window.location.href = '/' + 'login' + '/';
}

function loadMessageHistory() {
    console.log("loadMessageHistory controller..")
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    var sender = localStorage.getItem('sender');
    var secondUser = localStorage.getItem('username_second');

    $.ajax({
        url: '/get_message_history/',  // Замените на URL вашего представления на сервере
        type: 'POST',
        data: {
            'sender': sender,
            'secondUser': secondUser
        },
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (response) {
            var messageList = $('#messageList');
            messageList.empty();  // Очищаем список сообщений перед добавлением новых

            response.forEach(function (message) {
                var formattedTime = new Date(message.sent_at).toLocaleString(); // Форматируем время отправки сообщения
                var listItem = $('<li>').text(message.sender + ': ' + message.message + ' (' + formattedTime + ')');
                messageList.append(listItem);
            });
        },
        error: function (xhr, status, error) {
            console.error('Произошла ошибка при получении истории сообщений:', error);
        }
    });
}




    function userFind() {
        console.log("Имя пользователя отобразилось");
        var div = document.getElementById("userProfile");
        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
        var userInput = $('#userSearch').val();

        CreateLocalStorage(userInput);
        console.log('Введенное значение поля для поиска пользователей:', userInput);

        if (userInput == localStorage.getItem('sender')){
            alert("Ошибка! Вы ввели самого же себя, попробуйте еще раз");

        }else{
            //console.log("div = " ,div);
            var data = {
                username: userInput
            };
            console.log(data.username);
            $.ajax({
                url: '/check_user/',
                type: 'POST',
                data: data,
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                success: function (response) {
                    if (response.exists) {
                        div.style.display = "block"
                        $("#userProfileName").text(data.username);
                        loadMessageHistory();
                        var pollingInterval = 1500;
                        startPollingForNewMessages(pollingInterval);
                    } else {
                        div.style.display === "none"
                        alert('Пользователь не найден в базе данных.');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Произошла ошибка при проверке и поиска пользователя:', error);
                }
            });

        }
    }



    function startPollingForNewMessages(interval) {
        console.log("updating view chat starting..");
        setInterval(loadMessageHistory, interval);  // Вызываем loadMessageHistory каждые interval миллисекунд
    }



