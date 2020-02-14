from django.conf.urls import url
from .views import index, get_pokemon_details, get_pokemons_by_type

urlpatterns = [
    url(r'^$', index, name = "pokemon_index"),
    url(r'^(?P<id>\d+)/$', get_pokemon_details, name = "pokemon_details"),
    url(r'^type/(?P<id>\d+)/$', get_pokemons_by_type, name = "pokemons_by_type"),
]
