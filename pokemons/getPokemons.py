import sys
from typing import Type
sys.path.append('D:/Django/pokeproject-Django')

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
    p.save()
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

def loadEvolutions(xMin, xMax):
    url = "https://pokeapi.co/api/v2/evolution-chain/"
    evolution1 = None
    evolution2 = None
    for i in range(xMin, xMax):
        print("loading evolution chain n°" + str(i))
        chain = url + str(i)
        response = requests.get(chain)
        if(response.status_code == 200):
            data = json.loads(response.text)
            try:
                pokemonBase = Pokemon.objects.get(name=data['chain']['species']['name'])
            except Pokemon.DoesNotExist:
                pokemonBase = None
            print(pokemonBase)
            if(pokemonBase is not None):
                for i in range(len(data['chain']['evolves_to'])):
                    try:
                        evolution1 = Pokemon.objects.get(name=data['chain']['evolves_to'][i]['species']['name'])
                    except Pokemon.DoesNotExist:
                        evolution1 = None
                    print(evolution1)
                    if(evolution1 is not None):
                        for j in range(len(data['chain']['evolves_to'][i]['evolves_to'])):
                            try:
                                evolution2 =  Pokemon.objects.get(name=data['chain']['evolves_to'][i]['evolves_to'][j]['species']['name'])
                            except Pokemon.DoesNotExist:
                                evolution2 = None
                            print(evolution2)
                            if(evolution2 is not None):
                                chain,created = PokemonEvolution.objects.update_or_create(
                                    pokemon=pokemonBase,
                                    pokemonEvolution1=evolution1,
                                    pokemonEvolution2=evolution2
                                )
                                chain.save()
            
#Name = evolutionData['chain']['species']['name']
#evolution1 = evolutionData['chain']['evolves_to'][0]['species']['name']
#evolution2 = evolutionData['chain']['evolves_to'][0]['evolves_to'][0]['species']['name']

#print('-----------Evolutions-------------')
#loadEvolutions(1,476)

#print('-----------Génération 1-------------')
#loadGeneration(1,152)
#print('-----------Génération 2-------------')
#loadGeneration(152, 252)
#print('-----------Génération 3-------------')
#loadGeneration(252, 389)
#print('-----------Génération 4-------------')
#loadGeneration(389,494)
#print('-----------Génération 5-------------')
#loadGeneration(494, 650)
#print('-----------Génération 6-------------')
#loadGeneration(650, 722)
#print('-----------Génération 7-------------')
#loadGeneration(722, 810)
#print('-----------Génération 8-------------')
#loadGeneration(810, 899)