from django.urls import path
from django.core.management import call_command
from django.http import HttpResponse

from . import views

def run_script(request):
    call_command('populate_db')
    return HttpResponse("Script executed")

urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.listing, name='list'),
    path('details/<int:pokemon_id>/', views.details, name='details'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('addPokemon',views.addPokemon, name='addPokemon'),
    path('updatePokemon', views.updatePokemon, name='updatePokemon'),
    path('searchPokemon', views.searchPokemon, name='searchPokemon'),
    path('run-script/', run_script)
]