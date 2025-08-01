
# Barterfy - Django приложение для обмена вещами
Веб-приложение на Django, в котором пользователи могут:
публиковать объявления о вещах (категории, описание, состояние),
просматривать объявления других пользователей,
предлагать обмен вещами,
принимать или отклонять предложения на обмен.

🚀 Возможности

🔐 Регистрация и авторизация

📤 Размещение объявлений

🖋 Редактирование и удаление своих объявлений

🔍 Поиск, фильтрация по категории и состоянию

🔁 Создание предложений на обмен

✅ Принятие и отклонение предложений







## Установка
1. Клонировать репозиторий
git clone https://github.com/Andrei-Rybachenko/Barterfy.git \
cd Barterfy 

2. Создать и активировать виртуальное окружение
python -m venv venv \
source venv/bin/activate  # Windows: venv\Scripts\activate

3. Установить зависимости
pip install -r requirements.txt

4. Выполнить миграции
python manage.py migrate

5. Создать суперпользователя (по желанию) 
python manage.py createsuperuser

6. Запустить сервер
python manage.py runserver




## Тестирование

Для запуска встроенных Django тестов:\
python manage.py test




## Структура проекта

ads/\
├ models.py       
├ views.py         
├ forms.py         
├ urls.py          
├ templates/      
├ tests.py         
