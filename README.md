# School Backend

## Description

A school backend rest api application based on python django rest framework.

## Features

1. List | Create | Detail | Update | Delete `School`
2. List | Create | Detail | Update | Delete `Classroom`
3. List | Create | Detail | Update | Delete `Teacher`
4. List | Create | Detail | Update | Delete `Student`

## Planing Features

- :white_check_mark: Unit Test
- :black_square_button: Env file
- :black_square_button: Authentication
- ...

## Requirements

1. python 3.10+

## Project setup

1. Clone this project and install python packages in your virutal environment

    ```bash
    # Using pipenv
    $ pyenv install
    ```

2. Migrate sqlite3 database
   
   ```bash
   $ pyenv shell
   $ python manage.py migrate
   ```
   or Use db.sqlite3.example


## Run the project

```bash
# development
$ pyenv shell
$ python manage.py runserver
```

The application should be serving on port `8000`. (Default)

## Run Test

```bash
$ pyenv shell
$ pytest
```

## API

For API, Visit `API.md`