/*document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Отправка запроса на сервер для проверки учетных данных
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Успешная авторизация, выполняем редирект на главную страницу
            window.location.href = '/';
        } else {
            // Неверные учетные данные, отображаем сообщение об ошибке
            document.getElementById('error-message').textContent = data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
*/

const input = document.getElementById('username');
const label = document.getElementById('login-label');

input.addEventListener('focus', () => {
    console.log(123);
    label.style.scale = 1.1;
    label.style.color = '#2F80ED';
});

input.addEventListener('blur', () => {
    label.style.scale = 1;
    label.style.color = '#999';
});

const input1 = document.getElementById('password');
const label1 = document.getElementById('password-label');

input1.addEventListener('focus', () => {
    console.log(123);
    label1.style.scale = 1.1;
    label1.style.color = '#2F80ED';
});

input1.addEventListener('blur', () => {
    label1.style.scale = 1;
    label1.style.color = '#999';
});