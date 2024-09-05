$(document).ready(function() {

    $('#login-form').on('click', '#log-btn', function() {
        console.log("log-btn activated");
        $('#login-form').hide();
        displayLoginForm();
    });

    $('#login-form').on('click', '#reg-btn', function() {
        console.log("register-btn activated");
        $('#login-form').hide();
        displayRegistrationForm();
    });

    $('#login-form').on('click', '#sumbit-reg-btn', function() {
        console.log("sumbit-reg-btn activated");
        send_register_data_to_server();
    });

    $('#login-form').on('click', '#sumbit-log-btn', function() {
        console.log("sumbit-log-btnac activated");
        send_login_data_to_server();
    });

});

function send_register_data_to_server(){
    var username = $('#username-register').val();
    var password = $('#password-register').val();

    var data = {
        username: username,
        password: password
    };

    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/submit_data_reg/',
        type: 'POST',
        data: data,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(response) {
            console.log('Данные успешно отправлены на сервер:', response);
            location.reload();
            alert("Регистрация успешна!");
        },
        error: function(xhr, status, error) {
            console.error('Произошла ошибка при отправке данных на сервер:', error);
            // Добавьте здесь код для обработки ошибки отправки данных на сервер, если это необходимо
        }
    });
}






function send_login_data_to_server(){
    var username = $('#username-log').val();
    var password = $('#password-log').val();

    var data = {
        username: username,
        password: password
    };

    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/submit_data_log/',
        type: 'POST',
        data: data,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(response) {
            console.log('Данные успешно отправлены на сервер:', response);
            // Сохраняем идентификатор сессии в куки
            window.location.href = '/' + username + '/';

        },
        error: function(xhr, status, error) {
            console.error('Произошла ошибка при отправке данных на сервер:', error);
            // Добавьте здесь код для обработки ошибки отправки данных на сервер, если это необходимо
        }
    });
}



function displayRegistrationForm(){
console.log("in displayLoginForm func");
    $('#login-form').html('');
    $('#login-form').append(`
       <div id= "register-form" >
           <div class = "text-header">
                <h2>Регистрация</h2>
            </div>
            <div id = "username" class="username">
                <label for="username">Username:</label>
                <div class="sec-2-username" id="sec-2-username">
                    <input id= "username-register" type="text" name="username" placeholder="Username..">
                </div>
            </div>
            <div id="password" class ="password">
                <label for="password">Password:</label>
                <div class="sec-2-password" id="sec-2-password">
                    <input id ="password-register" class="pas" type="password" name="password" placeholder="············">
                </div>
            </div>
            <div class = "login-bnt-div">
                <button id="sumbit-reg-btn" class="login">Login</button>
            </div>
            <div class="footer">
                <span id = "log-btn">Login</span>
                <span>Forgot Password?</span>
            </div>
        </div>
     `);
      $('#login-form').show();
}

function displayLoginForm(){
console.log("in displayLRegForm func");
    $('#login-form').html('');
    $('#login-form').append(`
        <div class = "text-header">
             <h2>Авторизация</h2>
        </div>
        <div id = "username" class="username">
            <label for="username">Username:</label>
            <div class="sec-2-username" id="sec-2-username">

                <input id = "username-log" type="text" name="username" placeholder="Username..">
            </div>
        </div>
        <div id="password" class ="password">
            <label for="password">Password:</label>
            <div class="sec-2-password" id="sec-2-password">
                <input id ="password-log" class="pas" type="password" name="password" placeholder="············">
            </div>
        </div>
        <div class = "login-bnt-div">
            <button  id="sumbit-log-btn" class="login">Login</button>
        </div>
        <div class="footer">
            <span id = "reg-btn">Register</span>
            <span>Forgot Password?</span>
        </div>
    `);
     $('#login-form').show();
}



