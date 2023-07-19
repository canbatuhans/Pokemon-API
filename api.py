from flask import Flask, jsonify, request

app = Flask(__name__)

pokemons = [
    {
        "name": "Bulbasaur",
        "price": "£63.00",
        "description": "Bulbasaur can be seen napping in bright sunlight. There is a seed on its back. By soaking up the sun’s rays, the seed grows progressively larger.",
        "stock": "45 in stock"
    },
    {
        "name": "Ivysaur",
        "price": "£87.00",
        "description": "There is a bud on this Pokémon’s back. To support its weight, Ivysaur’s legs and trunk grow thick and strong. If it starts spending more time lying in the sunlight, it’s a sign that the bud will bloom into a large flower soon.",
        "stock": "142 in stock"
    },
       {
        "name": "Venusaur",
        "price": "£105.00",
        "description": "There is a large flower on Venusaur’s back. The flower is said to take on vivid colors if it gets plenty of nutrition and sunlight. The flower’s aroma soothes the emotions of people.",
        "stock": "30 in stock"
    },
       {
        "name": "Charmander",
        "price": "£48.00",
        "description": "The flame that burns at the tip of its tail is an indication of its emotions. The flame wavers when Charmander is enjoying itself. If the Pokémon becomes enraged, the flame burns fiercely..",
        "stock": "206 in stock"
    },
       {
        "name": "Charmeleon",
        "price": "£165.00",
        "description": "Charmeleon mercilessly destroys its foes using its sharp claws. If it encounters a strong foe, it turns aggressive. In this excited state, the flame at the tip of its tail flares with a bluish white color.",
        "stock": "284 in stock"
    },
       {
        "name": "Charizard",
        "price": "£156.00",
        "description": "Charizard flies around the sky in search of powerful opponents. It breathes fire of such great heat that it melts anything. However, it never turns its fiery breath on any opponent weaker than itself.",
        "stock": "31 in stock"
    },
]

# Ürün servisi
class ProductAPI:
    def get_all_products(self):
        return pokemons

    def get_products_exclude(self, excluded_fields):
        excluded_fields = excluded_fields.split(',')
        result = [{key: pokemon[key] for key in pokemon if key not in excluded_fields} for pokemon in pokemons]
        return result

    def get_products_include(self, included_fields):
        included_fields = included_fields.split(',')
        result = [{key: pokemon[key] for key in pokemon if key in included_fields} for pokemon in pokemons]
        return result

# API kontrolcüsü
class APIController:
    def __init__(self, product_api):
        self.product_api = product_api

    # localhost/pokemons endpoint'i
    def get_all_pokemons(self):
        products = self.product_api.get_all_products()
        return jsonify(products)

    # localhost/pokemons/ex=name,stock endpoint'i
    def get_pokemons_exclude(self, excluded_fields):
        products = self.product_api.get_products_exclude(excluded_fields)
        return jsonify(products)

    # localhost/pokemons/in=description,name endpoint'i
    def get_pokemons_include(self, included_fields):
        products = self.product_api.get_products_include(included_fields)
        return jsonify(products)

# Flask ve endpoint yönlendirme
@app.route('/pokemons', methods=['GET'])
def get_all_pokemons():
    return api_controller.get_all_pokemons()

@app.route('/pokemons/ex=<excluded_fields>', methods=['GET'])
def get_pokemons_exclude(excluded_fields):
    return api_controller.get_pokemons_exclude(excluded_fields)

@app.route('/pokemons/in=<included_fields>', methods=['GET'])
def get_pokemons_include(included_fields):
    return api_controller.get_pokemons_include(included_fields)

# Uygulama başlatma
if __name__ == '__main__':
    product_api = ProductAPI()
    api_controller = APIController(product_api)
    app.run()
