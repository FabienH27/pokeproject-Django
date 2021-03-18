from typing import Type
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=255)
    height = models.IntegerField()
    weight = models.IntegerField()
    default_front_sprite_url = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now,editable=False)
    modified = models.DateTimeField(default=timezone.now)
    pokedex_number = models.IntegerField()
    default_back_sprite_url = models.CharField(max_length=255, blank=True, null=True)
    front_shiny_sprite_url = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'pokemons'
    def __str__(self):
        return self.name

class Stat(models.Model):
    name = models.CharField(max_length=255)
    pokemons = models.ManyToManyField(Pokemon,through='PokemonStat', related_name="stat")
    created = models.DateTimeField(default=timezone.now,editable=False)
    modified = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'stat'
        ordering = ['name']
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=255)
    pokemons = models.ManyToManyField(Pokemon, through='PokemonType',related_name="type")
    created = models.DateTimeField(default=timezone.now,editable=False)
    modified = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'types'
    def __str__(self):
        return self.name

class PokemonStat(models.Model):
    pokemon = models.ForeignKey(Pokemon,on_delete=models.CASCADE)
    stat = models.ForeignKey(Stat,on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        db_table = 'pokemon_stats'

class PokemonType(models.Model):
    pokemon = models.ForeignKey(Pokemon,on_delete=models.CASCADE)
    types = models.ForeignKey(Type,on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now,editable=False)
    modified = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'pokemon_types'
    def __str__(self):
        return self.types.name

class UserPokemon(models.Model):
    pokemon = models.ForeignKey(Pokemon,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table = 'user_pokemons'
    def __str__(self):
        return self.pokemon.name

class PokemonEvolution(models.Model):
    pokemon = models.ForeignKey(Pokemon,on_delete=models.CASCADE,related_name='pokemon')
    pokemonEvolution1 = models.ForeignKey(Pokemon,on_delete=models.CASCADE,blank = True,null = True,related_name='evolution1')
    pokemonEvolution2 = models.ForeignKey(Pokemon,on_delete=models.CASCADE,blank = True,null = True,related_name='evolution2')
    class Meta:
        db_table = 'pokemon_evolutions'
    def __str__(self):
        return self.pokemon.name