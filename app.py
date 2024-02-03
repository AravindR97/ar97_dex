from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import requests

app = Flask(__name__)

client = MongoClient("mongodb+srv://'username':'password'@sparta0.o9aiqfb.mongodb.net/?retryWrites=true&w=majority")
db = client.dbhomework

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pkmn', methods=["POST"])
def save_pkmn():
    pkmn_name = request.form['pkmn_give'].lower()
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pkmn_name}")

    if r.status_code == 200:
        data = r.json()

        type_list = []
        for i in data['types']:
            type_list.append(i['type']['name'])

        image = data['sprites']['front_default']

        ability_list = []
        for i in data['abilities']:
            ability_list.append(i['ability']['name'])


        doc = {'pkmn': pkmn_name,
            'type': type_list,
            'img': image,
            'ability':ability_list}
        
        db.pokedex.insert_one(doc)
        return jsonify({"msg": "Pokemon Captured!"})
    else:
        return jsonify({"msg":"Enter a valid name!!"})

@app.route('/pkmn', methods= ["GET"])
def get_pkmn():
    pkmn_list = list(db.pokedex.find({},{'_id':False}))
    return jsonify({'pkmns':pkmn_list})

@app.route('/delete', methods= ["POST"])
def delete_pkmn():
    name_receive = request.form['name_give']
    db.pokedex.delete_one({'pkmn': name_receive})
    return jsonify({'msg': f"Goodbye {name_receive}!"})


if __name__=="__main__":
    app.run(debug=True)
