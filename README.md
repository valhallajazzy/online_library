# Скачиваем книги из онлайн-библиотеки tululu.org
![Screenshot](https://github.com/valhallajazzy/online_library/blob/main/pic/miantu.png)

* Текст книг скачиваются в папку `books/` корневой директориии проекта  
* Обложки книг скачиваются в папку `pictures/` корневой директориии проекта

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
$ python3 tululu.py -s <start_id> -e <end_id>
```

PS `<start_id>`, `<end_id>` - срез id книг, которые нужно скачать. Аргументами по умолчанию являются `<start_id>` - 1,  
`<end_id>` - 10, то есть скрипт может запуститься и без аргументов.
