# Курсовой проект "Машинное обучение в бизнесе"

### Разработка приложения для прогнозирования цены на аренду квартиры в Москве с использованием Flask, Vue.js, Docker-compose. 

Пример задеплоиного приложения [по ссылке](http://rental-price-prediction.adinweb.ru/).

## Установка через docker-compose.

1. Запуск версии для разработки

    ```sh
   docker-compose -f docker-compose-dev.yml up --build
    ```
   После установки доступно по ссылке: [http://localhost:8080](http://localhost:8080) или [http://0.0.0.0:8080](http://localhost:8080)


2. Запуск в продакшн

    ```sh
   docker-compose -f docker-compose-prod.yml up --build -d
    ```
