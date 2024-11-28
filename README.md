# Покрытие тестами кода сайта новостной ленты и сайта ведения заметок (логика, роутеры, контент)
## Структура проекта
```
Dev
 └── django_testing
     ├── ya_news
     │   ├── news
     │   │   ├── fixtures/
     │   │   ├── migrations/
     │   │   ├── pytest_tests/   <- Директория с pytest для проекта ya_news
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanews/
     │   ├── manage.py
     │   └── pytest.ini
     ├── ya_note
     │   ├── notes
     │   │   ├── migrations/
     │   │   ├── tests/          <- Директория с unittest для проекта ya_note
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanote/
     │   ├── manage.py
     │   └── pytest.ini
     ├── .gitignore
     ├── README.md
     ├── requirements.txt
     └── structure_test.py
```

## Запуск проекта
Клонируйте репозиторий локально: 
```
git clone git@github.com:Alexshifter/django_testing.git
```
Находясь в директории проекта разверните виртуальное окружение
```
python -m venv venv
```
Запустите виртуальное окружение
```
source venv/scripts/activate
```
Обновите pip
```
python -m pip install --upgrade pip
```
Установите зависимости
```
pip install -r requirements.txt
```
Для проверки запуска тестов используйте команды библиотеки ```pytest``` для проекта ```ya_news`` и команды библиотеки ```unittest``` для проекта ya_note.
## Автор проекта
[Alexey Pakaev](https://github.com/Alexshifter)
