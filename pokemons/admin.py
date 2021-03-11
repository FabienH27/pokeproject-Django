from django.contrib import admin

from .models import Pokemon, Stat,Type

# Register your models here.
admin.site.register(Pokemon)
admin.site.register(Stat)
admin.site.register(Type)