# Сборка документации
1. Должен быть установлен python3
2. Установить пакет mkdocs: pip install mkdocs
3. Установить пакет с темой material: pip install mkdocs-material
4. Проверка отображения страниц командой mkdocs serve (должен хостить на локальной машине по адресу: http://127.0.0.1:8000)
5. Сборка в директорию site командой mkdocs build
6. Хостинг простым http-сервером. Перейти в каталог tutorial/site и набрать: python -m http.server (должен хостить на локальной машине по адресу: http://127.0.0.1:8000)

## Синтаксис
Классический markdown, с использованием расширения Admonition, которое позволяет выделять красивым блоком заметки и код. 

Ссылки:
- [mkdocs](https://www.mkdocs.org) 
- [Material](https://github.com/squidfunk/mkdocs-material)
- [Python](https://www.python.org/)
- [Admonition](https://squidfunk.github.io/mkdocs-material/extensions/admonition)



