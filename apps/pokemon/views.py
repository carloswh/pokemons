import json
import requests

from django.shortcuts import render

# Create your views here.


def index(request):
    response = {
        'pokemons' : get_pokemons()
    }

    return render(request, 'pokemon/pokemon.html', response)

def pokemon_api(endpoint = 'pokemon'):
    result      = None
    api_url     = 'https://pokeapi.co/api/v2/{}'.format(endpoint)
    
    response    = requests.get(api_url)

    if response.status_code == 200:
        payload = response.json()
        result  = payload.get('results', []) if 'results' in payload else payload

    return result

def get_pokemons():
    pokemons = pokemon_api()

    for pokemon in pokemons:
        pokemon['id'] = pokemon['url'].split('/')[-2]

    return pokemons

def get_pokemon_details(request, id):
    pokemon     = None
    endpoint    = 'pokemon/{}'.format(id)

    response    = pokemon_api(endpoint)

    if response:
        moves       = ""
        habilities  = ""
        types       = []

        #_types = reduce(lambda str, value : "{} ,{}".format(str, value['type']['name']), response['types'])

        for hability in response['abilities']:
            habilities = hability['ability']['name'] if habilities == "" else "{}, {}".format(hability['ability']['name'], habilities)

        for move in response['moves']:
            moves = move['move']['name'] if moves == "" else "{}, {}".format(move['move']['name'], moves)

        for ptype in response['types']:
            ptype['id'] = ptype['type']['url'].split('/')[-2]
    
        pokemon = {
            'id'            : response['id'],
            'name'          : response['name'],
            'height'        : response['height'],
            'weight'        : response['weight'],
            'types'         : response['types'],
            'habilities'    : habilities,
            'moves'         : moves,
        }

    return render(request, 'pokemon/details.html', { 'pokemon' : pokemon })

def get_pokemons_by_type(request, id):
    pokemons = []
    endpoint = 'type/{}'.format(id)

    response = pokemon_api(endpoint)

    if response['pokemon']:
        for pokemon in response['pokemon']:
            
            pokemon_obj = {
                'id'    : pokemon['pokemon']['url'].split('/')[-2],
                'name'  : pokemon['pokemon']['name'],
            } 

            pokemons.append(pokemon_obj)

    return render(request, 'pokemon/pokemon.html', { 'pokemons' : pokemons })

