from django.db import models
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Pokemon, PokemonStat, UserPokemon
from .forms import RegisterForm

def index(request):
    user = request.user
    return render(request,'pokemons/index.html/', {'user': user})

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