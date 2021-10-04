# PokeProject

![Python](https://forthebadge.com/images/badges/made-with-python.svg)

A personal project to learn Python & Django.

Live demo : https://pokeproject-django.herokuapp.com/

## Configuration

- In the pokeproject folder : copy `.env.example` file to `.env` 
- Change your settings inside the `.env` file to match your MySQL Database configuration
- Generate a new secret key from the cmd with : `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' `
- Paste this key to the `.env` file as follows : `SECRET_KEY=your_key`

### Load pokemons

- Create a database named after what you wrote in the `.env` file, it could be `pokebase`
- Run the command : `py pokemons\getPokemons.py`
> It could take a few minutes to load all pokemons

### Start Django Server

- Run the command : `py manage.py runserver`
- Go to http://127.0.0.1:8000/pokemons/

### Author

Fabien Hannon

### License

Licensed under the GPL License
