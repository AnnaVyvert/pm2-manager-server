# pm2-manager-server
### components of the project
the server is fragmented into these three parts:
- client - examples of scripts that a user can use to send requests to the server (any request can be sent via CURL or python);
- server - the server, it does run the code, script execution and its configuration;
- sh - storage location for various isolated scripts to run. it includes both bash environment variables and utilities.

### server device
```
the server runs on the following system:
-> open port, waiting for a request
-> request acceptance
-> request processing
  - key verification
  - access key (private server access key)
  - project key (since the server manages several projects, it needs data with which project to interact)
-> running scripts
-> sending a response
```

### exception handling
  the server could potentially break down in two stages:
- request processing
- running scripts

accordingly, errors must be handled and a clear response sent to the user.
at the moment, only the "request processing" point is being processed.
the "run scripts" point has a minimal exception handling.

### about scripts
scripts can be any, the main thing is that they work correctly, are fault-tolerant, idempotent and the server runs them in the right place and with the right arguments.

at the moment, the system is able to:
- restart the project
- stop pm2 runtime
- update the project from the repository
- restart the project

since the data for the configuration of services are located inside the project inside the .env file, there is no need to configure the restart

### about the client part
there is a beginning of the development of a python script to send requests to the server.

in the closed contour, a static URL, private key and project keys are set, and in the open contour, the user selects a project to update and restart the project (in the future, the functionality can be expanded by introducing an additional key to the action of the management server)

---

# pm2-manager-server
### составляющие проекта
сервер разделён на три части:
- client - примеры скриптов, которые может использовать пользователь для отправки запросов на этот сервер (любой запрос можно отправить через CURL или питон);
- server - непосредственно сам сервер, его код для рантайма, запуск скриптов и его конфигурация;
- sh - место хранения различных изолированных скриптов для запуска. туда входят как переменные окружения bash, так и утилиты.

### устройство сервера
```
сервер работает по следующей системе: 
-> открытый порт, ожидание запроса 
-> приём запроса
-> обработка запроса
	- проверка ключей
	- ключ доступа (приватный ключ доступа к серверу)
	- ключ проекта (так как сервер управляет несколькими проектами ему нужны данные с каким проектом взаимодействовать)
-> запуск скриптов
-> отправка ответа
```

### обработка исключений
потенциально сервер может "лечь" на двух этапах: 
- обработка запросов
- запуск скриптов

соответственно, ошибки необходимо обрабатывать и отправлять понятный ответ пользователю.
на данный момент обрабатывается только пункт "обработка запроса".
пункт "запуск скриптов" имеет минимальную обработку исключений.

### про скрипты
скрипты могут быть любые, главное чтобы они корректно отрабатывали, были отказоустойчивыми, идемпотентными и сервер запускал их в правильном месте и с правильными аргументами.

на данный момент система умеет: 
- перезапускать проект
- останавливать pm2 runtime
- обновлять проект из репозитория
- перезапускать проект

так как данные для конфигурации сервисов находятся внутри проекта в .env файле, то конфигурировать перезапуск не нужно

### про клиентскую часть
есть начало разработки скрипта на питоне для отправки запросов на сервер. 

в закрытом контуре устанавливается статичный URL, приватный ключ и ключи проектов, а в открытом контуре пользователем выбирается проект для обновления и перезапуска проекта (в дальнейшем функциональность может быть расширена введением дополнительного ключа на действие управляющего сервера)
