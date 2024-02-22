# Скачиваем книги из онлайн-библиотеки tululu.org
![Screenshot](https://github.com/valhallajazzy/online_library/blob/main/pic/maintulu.png)

Текст книг скачиваются в папку `books/` корневой директориии проекта
Обложки книг скачиваются в папку `pictures/` корневой директориии проекта

![Screenshot](https://github.com/valhallajazzy/online_library/blob/main/pic/pathtulu.png)

## Подготовка и запуск скрипта

* В терминале, в корневой папке проекта создаем виртуальное окружение и устанавливаем зависимости:

```console
$ poetry install
```
* Активируем виртуальное окружение:

```console
$ poetry shell
```

* Из корневой директории проекта запускаем скрипт командой:

```console
$ python3 tululu.py <start_id> <end_id>
```

PS Нужны обязательные аргументы `<start_id>`, `<end_id>` для указания диапазона скачиваемых книг с сайта,  
без них скачивание не начнется.
