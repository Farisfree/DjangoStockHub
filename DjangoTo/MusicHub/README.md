# Music Management System

This project is a software search engine that allows users to search for the appropriate song in this application based
on the keyword of the song title or the keyword of the song author.

## Import DataBase

Import the three tables from  `MusicHub/data` folder into the MySQL database

## Connect to MySQL

In `MusicHub/MusicHub/settings.py`, modify the DATABASES variable by fulfilling your own MySQL information,
including `NAME`, `USER`, `PASSWORD`

In `MusicHub/MusicHub/service.py`,modify the Connection variable conn by fulfilling your own MySQL information,
including `host`, `user`, `password`

## Install requirements

Run the following command to install requirements

```shell
pip install matplotlib
pip install pandas
pip install django
pip install pylab
pip install pymysql
```

## Setup Server

Run the following command to start a development server.

```shell
python manage.py runserver
```

then visit `http://127.0.0.1:8000/login` (by default) to preview the website.
The admin account is "admin" and the password is "admin".
