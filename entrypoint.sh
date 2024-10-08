#!/bin/sh

exec python manage.py migrate

exec python pokeapp/getPokemons.py
