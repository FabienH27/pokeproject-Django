# PokeProject

A personal project to learn Python & Django.

## Configuration

- In the pokeproject folder : copy `.env.example` file to `.env` 
- Change your settings inside the `.env` file to match your MySQL Database configuration

### Load pokemons

- Create a database named after what you wrote in the `.env` file, it could be `pokebase`
- Run the command : `py pokemons\getPokemons.py`
> It could take a few minutes to load all pokemons

### Start Django Server

- Run the command : `py manage.py runserver`
- Go to http://127.0.0.1:8000/pokemons/