from django.db import models
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Pokemon, PokemonStat, UserPokemon, PokemonEvolution

from .forms import RegisterForm

def index(request):
    user = request.user
    return render(request,'pokemons/index.html/', {'user': user})

def listing(request):
    pokemons = Pokemon.objects.all().order_by('id')
    paginator = Paginator(pokemons,30)

    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    
    return render(request,'pokemons/list.html',{'page_object':page_object})

def details(request,pokemon_id):
    pokemonData = Pokemon.objects.get(pk=pokemon_id)
    dataStats = PokemonStat.objects.filter(pokemon=pokemon_id)

    pokemonEvolution1List = []
    pokemonEvolution2List = []
    pokemonBase = None

    if(PokemonEvolution.objects.filter(pokemon=pokemon_id)):
        base = PokemonEvolution.objects.filter(pokemon=pokemon_id)
        for i in range(base.count()):
            evolution1 = list(Pokemon.objects.filter(pk=base[i].pokemonEvolution1.pk).values_list('name','default_front_sprite_url','id'))
            pokemonEvolution1List.append(evolution1[0])
            if(base[i].pokemonEvolution2 is not None):
                evolution2 = list(Pokemon.objects.filter(pk=base[i].pokemonEvolution2.pk).values_list('name','default_front_sprite_url','id'))
                pokemonEvolution2List.append(evolution2[0])
        pokemonEvolution1List = list(dict.fromkeys(pokemonEvolution1List))
        pokemonEvolution2List = list(dict.fromkeys(pokemonEvolution2List))

    elif(PokemonEvolution.objects.filter(pokemonEvolution1=pokemon_id)):
        evolution1 = PokemonEvolution.objects.filter(pokemonEvolution1=pokemon_id)
        pokemonBase = list(Pokemon.objects.filter(pk=evolution1[0].pokemon.pk).values_list('name','default_front_sprite_url','id'))
        evolution2 = evolution1.values('pokemonEvolution2')
        for i in range(evolution1.count()):
            if(evolution1[i].pokemonEvolution2 is not None):
                pokemonEvolution2 = list(Pokemon.objects.filter(pk=evolution1[i].pokemonEvolution2.pk).values_list('name','default_front_sprite_url','id'))
                pokemonEvolution2List.append(pokemonEvolution2[0])
        pokemonBase = list(dict.fromkeys(pokemonBase))
        pokemonEvolution2List = list(dict.fromkeys(pokemonEvolution2List))

    elif(PokemonEvolution.objects.filter(pokemonEvolution2=pokemon_id)):
        evolution2 = PokemonEvolution.objects.filter(pokemonEvolution2=pokemon_id)
        pokemonBase = list(Pokemon.objects.filter(pk=evolution2[0].pokemon.pk).values_list('name','default_front_sprite_url','id'))
        evolution1 = evolution2.values('pokemonEvolution1')
        for i in range(evolution2.count()):
            pokemonEvolution1 = list(Pokemon.objects.filter(pk=evolution2[i].pokemonEvolution1.pk).values_list('name','default_front_sprite_url','id'))
            pokemonEvolution1List.append(pokemonEvolution1[0])
        pokemonEvolution1List = list(dict.fromkeys(pokemonEvolution1List))
        pokemonEvolution2List = list(dict.fromkeys(pokemonEvolution2List))

    return render(request,'pokemons/details.html',{'pokemon':pokemonData, 'stats':dataStats,'pokemonBase':pokemonBase,'pokemonEvolution1':pokemonEvolution1List,'pokemonEvolution2':pokemonEvolution2List})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/pokemons')
    else:
        form = RegisterForm()
    return render(request, 'pokemons/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':  
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/pokemons')
    else:
        form = AuthenticationForm()
    return render(request,'pokemons/login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('/pokemons')

@login_required(login_url='/pokemons/login')
def dashboard(request):
    userPokemons = UserPokemon.objects.filter(user=request.user)
    print(userPokemons)
    return render(request, 'pokemons/dashboard.html', {'user_pokemons':userPokemons})

def addPokemon(request):
    if request.method == 'GET':
        pokemon_id = request.GET.get('pokemon_id')
        user_id = request.GET.get('user_id')
        pokemon = Pokemon.objects.get(id=pokemon_id)
        user = User.objects.get(id=user_id)

        data = {
            'exists': UserPokemon.objects.filter(user=user,pokemon=pokemon).exists()
        }
        if not data['exists']:
            m,created = UserPokemon.objects.update_or_create(user=user, pokemon=pokemon)
            m.save()
    return JsonResponse(data)
    
def updatePokemon(request):
    pokemon_id = request.GET.get('pokemon_id')
    user_id = request.GET.get('user_id')
    pokemon = Pokemon.objects.get(id=pokemon_id)
    user = User.objects.get(id=user_id)
    userPokemons =UserPokemon.objects.filter(user=user, pokemon=pokemon).delete()
    pokemonList = UserPokemon.objects.filter(user=user)
    return render(request, 'pokemons/dashboard_table.html', {'user_pokemons':pokemonList})

def searchPokemon(request):
    data = list(Pokemon.objects.filter(name__istartswith=request.GET.get('term')).values('id','name','default_front_sprite_url'))
    return JsonResponse(data,safe=False)





    #pokemonEvolution1Length = PokemonEvolution.objects.filter(pokemon=pokemonData).count()
    #pokemonPrevious = None
    #pokemonEvolutionPrevious = None
    #pokemonNext = None
    #pokemonBase = None
    #if(pokemonEvolution1Length == 0):
    #    pokemonEvolution = PokemonEvolution.objects.filter(pokemonEvolution1=pokemonData)
    #    if(Pokemon.objects.filter(pk=pokemonEvolution[0].pokemon.pk).count() > 0 ):
    #        pokemonPrevious = Pokemon.objects.filter(pk=pokemonEvolution[0].pokemon.pk).values_list('name','default_front_sprite_url','id')
    #    pokemonNext = Pokemon.objects.filter(pk=pokemonEvolution[0].pokemonEvolution2.pk).values_list('name','default_front_sprite_url','id')
    #
    #pokemonEvolution1 = PokemonEvolution.objects.filter(pokemon=pokemonData)
    #pokemonEvolution1List = []
    #for i in range(pokemonEvolution1Length):
    #    evolution1 = list(Pokemon.objects.filter(pk=pokemonEvolution1[i].pokemonEvolution1.pk).values_list('name','default_front_sprite_url','id'))
    #    pokemonEvolution1List.append(evolution1[0])
    #pokemonEvolution1List = list(dict.fromkeys(pokemonEvolution1List))
    #pokemonEvolution2Length = PokemonEvolution.objects.filter(pokemon=pokemonData).count()
    #pokemonEvolution2 = PokemonEvolution.objects.filter(pokemon=pokemonData)
    #pokemonEvolution2List = []
    #for i in range(pokemonEvolution2Length):
    #    if pokemonEvolution2[i].pokemonEvolution2 is not None:
    #        evolution2 = list(Pokemon.objects.filter(pk=pokemonEvolution2[i].pokemonEvolution2.pk).values_list('name','default_front_sprite_url','id'))
    #        pokemonEvolution2List.append(evolution2[0])
    #pokemonEvolution2List = list(dict.fromkeys(pokemonEvolution2List))
    #if(PokemonEvolution.objects.filter(pokemon=pokemon_id).exists()):
    #    pokemonBase = PokemonEvolution.objects.filter(pokemon=pokemon_id)
    #    evolution1Count = pokemonBase.values('pokemonEvolution1').count() 
    #    pokemonEvolution1List = []
    #    if(evolution1Count > 0):
    #        for i in range(pokemonEvolution1Length):
    #            evolution1 = list(Pokemon.objects.filter(pk=pokemonBase[i].pokemonEvolution1.pk).values_list('name','default_front_sprite_url','id'))
    #            pokemonEvolution1List.append(evolution1[0])
    #        print(pokemonEvolution1List)
    #        pokemonEvolution1List = list(dict.fromkeys(pokemonEvolution1List)) 
    #        
    #        evolution2Count = pokemonBase.values('pokemonEvolution2').count() 
    #        if(evolution2Count)
    #        pokemonEvolution2List = []
    #        for i in range(pokemonEvolution1Length):
    #            evolution2 = list(Pokemon.objects.filter(pk=pokemonBase[i].pokemonEvolution2.pk).values_list('name','default_front_sprite_url','id'))
    #            pokemonEvolution2List.append(evolution2[0])
    #        print(pokemonEvolution2List)

    #elif(PokemonEvolution.objects.filter(pokemonEvolution1=pokemon_id)):
    #    print("evolution 1")
    #elif(PokemonEvolution.objects.filter(pokemonEvolution2=pokemon_id)):
    #    print("evolution2")