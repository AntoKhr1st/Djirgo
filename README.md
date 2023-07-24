# Djirgo

*сервис разработан для управления задачами : создание, распределение и обновление задач.


API реализован на основе *django REST framework*.\
реализована регистрация и аутентификация пользователей.*


### Запуск :
> 
```python
docker compose up --build
```
### Эндпоинты 

1. [admin/](http://127.0.0.1:8000/admin/)
2. [api/tasks/](http://127.0.0.1:8000/api/tasks/)
3. [api/tasks/{id}/](https://127.0.0.1:8000/api/tasks/1/)
4. [api/users/](https://127.0.0.1:8000/api/users/)
5. [api/users/{id}/](https://127.0.0.1:8000/api/users/1/)
6. [api/auth/users/](https://127.0.0.1:8000/api/auth/users/)
7. [api/auth/jwt/create/](http://127.0.0.1:8000/api/auth/jwt/create/)

### Регистрация пользователя:
#### **POST:** **http://127.0.0.1:8000/api/auth/users/**

```json
{
    "username": "test_user",
    "password": "test_pass"
}
```

#### **POST:** **http://127.0.0.1:8000/api/auth/jwt/create/**

>аутентификации реализована с помощью JWT-token
```json
{
    "username": "test_user",
    "password": "test_pass"
}
```

*  response:

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 ....  ROUx3kl5CPHKzFiejKsaheLSx2IcJSY",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 .... 8TysltQY4bUqVVUH5BvbcwsziDo6vYgIfFUS8UHQ3dI"
}
```


### Новая задача:

#### **POST:** **http://127.0.0.1:8000/api/tasks/**


```json
{
    "text":" task_text"
}
```

 *  response:

```json
 {
    "id": 1,
    "task_status": "New",
    "owner": "test_user",
    "text": "task_text",
    "pub_date": "2023-07-24T12:14:24.025402Z",
    "performer": null,
    "perform_time": "00:00:00"
} 
```
>  *- При создании новой задачи, поле owner автоматически назначается в соответствии с пользователем, который создал задачу.*
> 

### Распределение задачи на исполнителя:

#### **PATCH:** **http://127.0.0.1:8000/api/tasks/{id}/**

```json
{
    "task_status": "In_Progress"
}
```



 *  response:

```json
{
    "id": 1,
    "task_status": "In_Progress",
    "owner": "test_user",
    "text": "task_text 1",
    "pub_date": "2023-07-24T12:01:35.198639Z",
    "performer": "test_user",
    "perform_time": "07:08:51"
}
```
>  *- при изменении статуса по задаче, которая находилась в статусе *New* автоматически выставляется исполнитель ( user отправивший запрос на обновление статуса).<br>Время затраченное на выполнение задачи фиксируется автоматически*


### В разработке
В проекте я использую **RabbitMQ** в качестве брокера сообщений. В настоящее время брокер принимает сообщения о поступивших задачах и помещает их в очередь. Чтобы получить эти сообщения, необходимо запустить скрипт **rabbitmq_consumer.py**

В дальнейшем планируется использовать **RabbitMQ** для создания устойчивого сервиса, способного эффективно обрабатывать высокую нагрузку запросов. Это будет достигнуто благодаря асинхронной обработке сообщений, которая позволит эффективно масштабировать и управлять обработкой задач.


Так же будет реализована периодическая задача по удалению старых сообщений 

