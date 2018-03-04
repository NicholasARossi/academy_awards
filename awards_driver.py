import tmdbsimple as tmdb
import pandas as pd
import numpy as np
import json
tmdb.API_KEY = ### your key here

import collections

def get_unique_actors(all_names):
    print ([item for item, count in collections.Counter(all_names).items() if count > 1])

if __name__== "__main__":
    movies = [399055, 359940, 398818, 399404, 446354, 419430, 400617, 374720, 391713]

    allnames = []
    castnodes = []
    castedges = []
    crewdb = pd.DataFrame()
    idx = 0
    movie_idx = 0
    movie_idxs = []
    titles = []
    all_names = []
    ### You need to run get unique actors on a compendium of all the names to get this list
    repeat_actors = ['Nick Searcy', 'Lucas Hedges', 'Charley Palmer Rothwell', 'Caleb Landry Jones', 'Bradley Whitford',
                     'Tracy Letts', 'Timothée Chalamet', 'Kathryn Newton', 'Michael Stuhlbarg']

    repeate_source = []
    repeate_target = []
    for j, movie in enumerate(movies):
        identity = tmdb.Movies(movie)
        dictionary = identity.credits()
        cast = [person['name'] for person in dictionary['cast'][:]]
        crew = [person['name'] for person in dictionary['crew'][:]]
        title = identity.info()['original_title']
        titles.append(title)
        movie_idx = idx
        movie_idxs.append(movie_idx)
        castnodes.append({"group": j, "name": title})
        idx += 1
        for castm in cast:
            if castm not in repeat_actors:
                castnodes.append({"group": j, "name": castm})
                all_names.append(castm)
                castedges.append({"source": movie_idx, "target": idx, "value": 1})
                idx += 1
            else:
                repeate_source.append(movie_idx)
                repeate_target.append(castm)

    for actor in sorted(repeat_actors):
        castnodes.append({"group": 9, "name": actor})
        indices = [i for i, x in enumerate(repeate_target) if x == actor]
        for indice in indices:
            castedges.append({"source": repeate_source[indice], "target": idx, "value": 1})

        idx += 1

    final={'nodes':castnodes, 'links':castedges}



    with open('other_sets.json', 'w') as fp:
        json.dump(final, fp)