# test_task_backend

### Блок авторизации

1. /login?phone=<телефон> GET запрос с номером телефона, возвращает 6-значный код
2.  /login POST запрос вида *`{"phone": "[+71111111111](tel:+71111111111)", "code": "QWDCR4"}`* - в ответ приходит `{"status": "OK"}` если код верный и `{"status": "Fail"}` если код не верный. 

### Блок работы с ссылками

1.  /structure GET запрос, В ответ прийдёт словарь с количеством каждого типа HTML-тэгов (например *`{"html": 1, "head": 1, "body": 1, "p": 10, "img": 2}`*) для сайта [freestylo.ru] является ответом по умолчанию.
- запрос поддерживает query string поэтому при добавлении ?link=<ссылка> возвращается словарь для выбранного сайта, а для ?tags=<тэги> вернётся только словарь тэгов указанные в запросе(можно перечислить через запятую, например html,img). Соответсвенно    /structure?link=example.com&tags=html,im или /structure?tags=html,im&link=example.com допустимые запросы, отсальные query string выдают ответ по умолчанию. 
 
2. /check_structure POST запрос вида  `{"link": "freestylo.ru", "structure": {"html": 1, "head": 1, "body": 1, "p": 10, "img": 2}}` 
Который для данный ссылки проверяет структуру html тэгов. В ответ должно приходить `{"is_correct": True}` если все верно и `{"is_correct": False, "difference": {"p": 2, "img": 1}}`  если есть ошибки, где difference - это разница структур. 
Например, если верная структура - `{"html": 1, "head": 1, "body": 1, "p": 4}` а передавалась структура `{"html": 1, "head": 1, "body": 1, "p": 2, "img": 1}` то разница будет `{"p": 2, "img": 1}`
    
### Для запуска проекта необходимо в терминале в корне проекта прописать следующие команды:
      docker-compose build
      docker-compose run 
Запущенное приложение будет доступно по http://0.0.0.0:8080 

