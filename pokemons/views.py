from django.db import models
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Pokemon, PokemonStat

def index(request):
    return render(request,'pokemons/index.html/')

def list(request):
    pokemons = Pokemon.objects.all()
    paginator = Paginator(pokemons,30)

    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    
    return render(request,'pokemons/list.html',{'page_object':page_object})

def details(request,pokemon_id):
    pokemon = Pokemon.objects.get(pk=pokemon_id)
    dataStats = PokemonStat.objects.filter(pokemon=pokemon_id)
    return render(request,'pokemons/details.html',{'pokemon':pokemon, 'stats':dataStats})