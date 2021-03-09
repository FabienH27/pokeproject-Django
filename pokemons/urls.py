from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.list, name='list'),
    path('details/<int:pokemon_id>/', views.details, name='details'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('addPokemon',views.addPokemon, name='addPokemon'),
    path('updatePokemon', views.updatePokemon, name='updatePokemon'),
]