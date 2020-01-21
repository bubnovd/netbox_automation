## WebHook Listener for NetBox
[webhook-listener.py](https://majornetwork.net/2019/10/even-better-webhook-listener/) Принимает вебхуки от NetBox. Код немного переделан из оригинального:
- Добавлен костыль для исправления юникода
- Исключен модуль проверки сигнатуры (токена для авторизации)

Скрипт создает файл webhook-listener.log, в котором отражаются действия, настроенные в webhooks NetBox'a.

### Docker
Запускать лучше в Docker. Dockerfile биндит порт 5000 как входящий для вебхуков. Лог файл маунтить отдельным volume'ом.
Сборка образа:
`docker build -t webhook-listener --build-arg HTTP_PROXY="http://prx.domain.com" --build-arg HTTPS_PROXY="http://prx.domain.com" .`

Запуск контейнера:
`docker run -d --name=webhook -p 5000:5000 -v /path/to/log:/webhook/ webhook-listener`

Время внутри контейнера UTC. Рекомендуется оставить таким, а часовые пояса устанавливать на внешних обработчиках