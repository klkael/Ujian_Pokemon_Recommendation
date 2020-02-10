from flask import Flask, render_template, request, send_from_directory
import pandas as pd 
import numpy as np 
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('namapokemon.html')

@app.route('/hasil', methods=['GET', 'POST'])
def hasil():
    namapoke = request.form
    namapokemon = request.form['Poke']
    listpoke = df['Name'].tolist()
    if namapokemon not in listpoke:
        return render_template('error.html')
    else:
        return render_template('pokemon.html',df=df,namapokemon=namapokemon,pokemon_lain=pokemon_lain)


if __name__ == '__main__':
    df = pd.read_csv('Pokemon.csv')

    col = ['Name','Type 1','Generation','Legendary']
    df = df[col]
    df['compare'] = df.apply(
        lambda i: f"{i['Type 1']},{(i['Generation'])},{(i['Legendary'])}",axis = 1)

    model = CountVectorizer(tokenizer= lambda x:x.split(','))
    rekomen = model.fit_transform(df['compare'])

    cos_score = cosine_similarity(rekomen)
    pokee = input('nama pokemon')
    index = df[df['Name']==pokee.capitalize()].index.values[0]
    # harus input nama pokemon sesuai di df buat buka server "Raichu", "Pikachu","Magnemite"
    #bingung error dimana
    
    rekomenpokelain = sorted(list(enumerate(cos_score[index])),key=lambda x:x[1],reverse=True)
    
    pokemon_lain = []

    for i in rekomenpokelain:
        pokeee = {}
        if i[0] == index:
            continue
        else:
            name = df.iloc[i[0]]['Name']
            tipe = df.iloc[i[0]]['Type 1']
            gen = df.iloc[i[0]]['Generation']
            legend = df.iloc[i[0]]['Legendary']
            pokeee['name'] = name
            pokeee['tipe'] = tipe
            pokeee['gen'] = gen
            pokeee['legend'] = legend
            
        pokemon_lain.append(pokeee)
        if len(pokemon_lain) == 6:
            break
    
    app.run(debug=True,port=5000)