import sys
from typing import Type
sys.path.append('D:/Django/pokeproject')

import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'pokeproject.settings'

django.setup()

from pokemons import models
from pokemons.models import *
import requests, json


#Récupération des données depuis l'API
def loadGeneration(xMin, xMax):
    url = 'http://pokeapi.co/api/v2/pokemon/'
    for i in range(xMin, xMax):
        pokemon = url + str(i)
        response = requests.get(pokemon)
        if(response.status_code == 200):        
            pokemondata = json.loads(response.text)
            pokemon = updatePokemon(pokemondata)
            updateType(pokemondata['types'],pokemon)
            updateStats(pokemondata['stats'], pokemon)

#Fonction utilisée pour insérer les données dans la base de données
def updatePokemon(pokemondata):
    p,created = Pokemon.objects.update_or_create(
        name = pokemondata['name'],
        height = pokemondata['height'],
        weight = pokemondata['weight'],
        default_front_sprite_url= pokemondata['sprites']['front_default'],
        front_shiny_sprite_url = pokemondata['sprites']['front_shiny'],
        default_back_sprite_url = pokemondata['sprites']['back_default'],
        pokedex_number = pokemondata['id']
    )
    #p.save()
    return p

def updateType(typedata, pokemonData):
    types = Type.objects.first()

    for i in range(len(typedata)):
        type, created = Type.objects.update_or_create(
            name = typedata[i]['type']['name']
        )
        type.save()
        type.pokemons.add(pokemonData)

def updateStats(statdata, pokemonData):
    for i in range(len(statdata)):
        stat,created = Stat.objects.update_or_create(
            name= statdata[i]['stat']['name'], 
        )
        stat = Stat.objects.get(pk=i+1)
        stat.pokemons.add(pokemonData,through_defaults={'value':statdata[i]['base_stat']})
    stat.save()

print('-----------Génération 1-------------')
loadGeneration(1,151)
print('-----------Génération 2-------------')
loadGeneration(152, 251)
print('-----------Génération 3-------------')
loadGeneration(252, 386)
print('-----------Génération 4-------------')
loadGeneration(389,449)
print('-----------Génération 5-------------')
loadGeneration(494, 649)
print('-----------Génération 6-------------')
loadGeneration(650, 721)
print('-----------Génération 7-------------')
loadGeneration(722, 809)
print('-----------Génération 8-------------')
loadGeneration(810, 899)