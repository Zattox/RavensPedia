<!--Установка-->
## Установка
1. Клонирование репозитория

```git clone https://github.com/Zattox/RavensPedia.git```

2. Установка poetry
 
Процесс установки описан [здесь](https://www.jetbrains.com/help/pycharm/poetry.html#install-poetry)

3. Установка зависимостей
 
Перейдите в папку проекта, затем пропишите в терминале ```poetry install```

4. Создание переменных окружения

Создайте файл ```.env``` в корневой папке проекта и введите ваши значения переменных окружения: ```FACEIT_BASE_URL``` и ```FACEIT_API_KEY```

5. Получение FACEIT_BASE_URL
   
Есть разные версии API, в коде описано взаимодействие с 4-ой версией ```https://open.faceit.com/data/v4/matches```, подробнее [тут](https://docs.faceit.com/docs/data-api/data/#tag/Matches/operation/getMatchStats)

6. Получение FACEIT_API_KEY
   
Получение API_KEY описано [здесь](https://developers.faceit.com/docs/auth/api-keys)
