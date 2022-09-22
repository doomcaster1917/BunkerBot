## BunkerBot расположен по адресу https://vk.com/bunker_lm
Для установки введите по отдельности в командную строку сервера:
```
apt update; apt install git

git clone https://github.com/doomcaster1917/BunkerBot.git /home/BunkerBot

/home/BunkerBot/./script
```
Первая строка обновит сервер и скачает git. Вторая строка скачает с гита этот репозиторий с ботом. Третья строка запустит установку бота: спросит токен от группы и пароль привязанной к боту страницы(при желании, можно отказатся), далее разместит нужные медиа на серверах vk.com, а в конце создаст systemd юнит, который будет отвечать за бесперебойную работу бота.


# При успешной установке начинает работать в вашей группе и создаёт из сообщений пользователей вот такой текст:

![1](https://user-images.githubusercontent.com/113614995/191250872-d4a79f2d-eef5-4458-b2cc-3073596a43c0.jpg)![3](https://user-images.githubusercontent.com/113614995/191258617-9f5a0593-54b6-43dc-a102-0f35f0706da2.jpg)


# Или делает из их фотографий мемы:
![2](https://user-images.githubusercontent.com/113614995/191251196-fd99c42e-0bae-46e4-b041-2524e440bf7e.jpg)

Текст в мемах дробится на строки, а размер шрифта уменьшается, а зависимости от количества текста. По умолчанию, текст рисуется снизу, но его можно рисовать сверху и снизу, использую команды "ВЕРХ:текст сверху НИЗ:текст снизу".

Так же, при желании, во время установки вы можете настроить привязанную к боту страницу, которая будет присылать вам уведомления об ошибках сервера (да, они есть, ибо vk.com часто разрывает сосединение с ботами, и этого никак не избежать):

![Снимок экрана от 2022-09-20 15-32-31](https://user-images.githubusercontent.com/113614995/191258313-1bbaab1c-20fa-4381-817b-c5cb312ff887.png)

