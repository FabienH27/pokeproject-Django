from django.core.management.base import BaseCommand
import sys
from typing import Type
sys.path.append('/code')

import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'pokeproject.settings'

django.setup()

from pokeapp import models
from pokeapp.models import *
import requests, json


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
    pokemonEvolution1 = None
    pokemonEvolution2 = None    
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
            if(pokemonBase is not None):
                for i in range(len(data['chain']['evolves_to'])):
                    try:
                        pokemonEvolution1 = Pokemon.objects.get(name=data['chain']['evolves_to'][i]['species']['name'])
                    except Pokemon.DoesNotExist:
                        pokemonEvolution1 = None
                    if pokemonEvolution1 is not None:
                        if len(data['chain']['evolves_to'][i]['evolves_to']) > 0:
                            #si le pokemon a une évolution de niveau 2
                            if len(data['chain']['evolves_to'][i]['evolves_to']) > 1:
                                for j in range(len(data['chain']['evolves_to'][i]['evolves_to'])):
                                    try:
                                        pokemonEvolution2 = Pokemon.objects.get(name=data['chain']['evolves_to'][i]['evolves_to'][j]['species']['name'])
                                    except Pokemon.DoesNotExist:
                                        pokemonEvolution2 = None
                                    chain,created = PokemonEvolution.objects.update_or_create(
                                        pokemon=pokemonBase,
                                        pokemonEvolution1=pokemonEvolution1,
                                        pokemonEvolution2=pokemonEvolution2
                                    )
                                    chain.save()  
                            else:
                                try:
                                    pokemonEvolution2 = Pokemon.objects.get(name=data['chain']['evolves_to'][i]['evolves_to'][0]['species']['name'])
                                except Pokemon.DoesNotExist:
                                    pokemonEvolution2 = None
                                chain,created = PokemonEvolution.objects.update_or_create(
                                    pokemon=pokemonBase,
                                    pokemonEvolution1=pokemonEvolution1,
                                    pokemonEvolution2=pokemonEvolution2
                                )
                                chain.save()  
                        else:
                            #Si le pokemon n'a pas d'évolution de niveau 2
                            chain,created = PokemonEvolution.objects.update_or_create(
                                pokemon=pokemonBase,
                                pokemonEvolution1=pokemonEvolution1
                            )
                            chain.save()   

class Command(BaseCommand):
    help = 'Populate SQLite database with default data'

    def handle(self, *args, **kwargs):
        print('-----------Génération 1-------------')
        loadGeneration(1,152)
        print('-----------Génération 2-------------')
        loadGeneration(152, 252)