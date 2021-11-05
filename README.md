# Курсовой проект "Машинное обучение в бизнесе"

### Разработка приложения для прогнозирования цены на аренду квартиры в Москве с использованием Flask, Vue.js, Docker-compose. 

Пример задеплоиного приложения [по ссылке](http://rental-price-prediction.adinweb.ru/).

## Задача.

1. Обучить модель на данных cian.ru для прогнозирования стоимости аренды квартиры в Москве. 

2. Предварительно были спарсены данные сайта (~24000 объектов).

3. Сохранить обученную модель (в формате dill).

4. Настроить серверную часть на Flask для применения модели к новым данным - предсказываем стоимость для одного объекта по параметрам.

5. Разработать простую клиентскую часть на Vue для возможности обращения к серверу и получения в ответ предсказания модели для обекта недвижимости.

6. Упаковать все в докер (использовал docker-compose).

7. Задеплоить на реальном сервере ([готовый пример](http://rental-price-prediction.adinweb.ru/)).

## Установка через docker-compose.


```sh
$ git clone https://github.com/ZV8/Flask-vue-price-predict.git
$ cd Flask-vue-price-predict
```
### Далее, если запускаем **версию для разработки**:

```sh
$ docker-compose -f docker-compose-dev.yml up --build
```
После установки будет доступно по ссылке: [http://localhost:8080](http://localhost:8080) или [http://0.0.0.0:8080](http://localhost:8080)


### ... если запуск **в прод**, то:

```sh
$ docker-compose -f docker-compose-prod.yml up --build -d
```

### API (Flask)
доступно по адресу: [http://localhost:5000](http://localhost:5000)

GET - История предиктов на сервере: [http://localhost:5000/get-examples](http://localhost:5000/get-examples)

POST - выполнить предикт для объекта: [http://localhost:5000/predict](http://localhost:5000/predict)
