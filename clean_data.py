import json
import os
import pandas as pd
from urllib.request import urlopen


dir_data = 'data'
download = False   # Flag to download data or not

# Download data
if download:
    url = 'https://raw.githubusercontent.com/HeroesToolChest/heroes-data/master/heroesdata/2.54.2.85576/data/herodata_85576_localized.json'
    response = urlopen(url)
    data_json = json.loads(response.read())

    # write out data
    with open(os.path.join(dir_data, 'herodata.json'), 'w') as outfile:
        json.dump(data_json, outfile)

# read data in from local file
else:
    f = open (os.path.join(dir_data, 'herodata.json'), "r")
    data_json = json.loads(f.read())


heroes = sorted(list(data_json.keys()))

data = {'hero': heroes,
        'role': list(),
        'speed': list(),
        'sight': list(),
        'rating_damage': list(),
        'rating_survivability': list(),
        'rating_utility': list(),
        'life_amount': list(),
        'life_scale': list(),
        'life_regenRate': list(),
        'life_regenScale': list(),
        'weapon_damage': list(),
        'weapon_damageScale': list(),
        'weapon_period': list(),
        'weapon_range': list()
        }


tanks = ['Anubarak', 'Arthas', 
        'Firebat', 'Crusader',
        'Cho', 'Diablo', 'Garrosh',
        'L90ETC',
        'MalGanis', 
        'MeiOW',
        'Muradin', 'Stitches', 'Tyrael']
bruisers = ['Artanis', 'Chen', 'Deathwing', 'Dehaka', 'DVa', 'Tinker',
             'Hogger', 'Imperius', 'Leoric', 'Malthael', 'Ragnaros', 
             'Rexxar', 'Barbarian', 'Thrall', 'Varian', 'Necromancer', 'Yrel']
meleesAssasins = ['Alarak', 'Butcher', 'Illidan', 'Kerrigan', 'Maiev',
                 'Murky', 'NexusHunter', 'Samuro',  'Valeera', 'Zeratul']
support = ['Abathur', 'Medivh', 'LostVikings', 'Zarya']


for h in heroes:

    # determine role
    try:
        if h in bruisers:
            r = 'Bruiser'
        elif h in tanks:
            r = 'Tank'
        elif h in meleesAssasins:
            r = 'Melee Assasin'
        elif h in support:
            r = 'Support'
        elif 'AllyHealer' in data_json[h]['descriptors']:
            r = 'Healer'
        else:
            r = 'Ranged Assasin'
    except:
        print(h, 'hero has no descriptors')
        if h == 'Hogger':
            r = 'Bruiser'
        elif h == 'Maiev':
            r = 'Melee Assasin'
        elif h == 'LostVikings':
            r = 'Support'
        else:
            r = None
    data['role'].append(r)


    # other attributes
    data['speed'].append(data_json[h]['speed'])

    # TODO: Generalize into a function
    try:
        data['sight'].append(data_json[h]['sight'])
    except KeyError:
        data['sight'].append(None)

    # ratings 
    ratings = ['damage', 'survivability', 'utility']
    try:
        ratings_data = data_json[h]['ratings']
        for r in ratings:
            data['rating_' + r].append(ratings_data[r])
    except KeyError:
        for r in ratings:
            data['rating_' + r].append(None)

    life = ['amount', 'scale', 'regenRate', 'regenScale']
    try:
        life_data = data_json[h]['life']
        for r in life:
            data['life_' + r].append(life_data[r])
    except KeyError:
        for r in life:
            data['life_' + r].append(None)

    weapon = ['damage', 'damageScale', 'period', 'range']
    try:
        weapon_data = data_json[h]['weapons'][0]
        for r in weapon:
            data['weapon_' + r].append(weapon_data[r])
    except KeyError:
        for r in weapon:
            data['weapon_' + r].append(None)

# correct spelling of hero names
heroNames = {'hero': {
                     # Bruisers
                    'DVa': 'D.Va',              
                    'Barbarian': 'Sonya',
                    'Necromancer': 'Xul',
                    'Tinker': 'Gazlowe',

                    # Healers
                    'FaerieDragon': 'Brightwing', 
                    'LiLi': 'Li Li',
                    'Monk': 'Kharazim',
                    'Medic': 'Lt. Morales',

                    # Melee Assassin
                    'NexusHunter': 'Qhira',

                    # Ranged Assassins
                    'Amazon': 'Cassia',
                    'DemonHunter': 'Valla',
                    'Dryad': 'Lunara',
                    'Guldan': "Gul'dan",
                    'Kaelthas': "Kael'thas",
                    'KelThuzad': "Kel'Thuzad",
                    'SgtHammer': 'Sgt. Hammer',
                    'Wizard': 'Li-Ming',
                    'WitchDoctor': 'Nazeebo',
                    'Zuljin': "Zul'jin",
                
                    # Support
                    'LostVikings': 'Lost Vikings',

                    # Tank
                    'Anubarak': "Anub'arak",
                    'Crusader': 'Johanna',
                    'Firebat': 'Blaze',
                    'L90ETC': 'E.T.C.',
                    'MalGanis': "Mal'Ganis",
                    'MeiOW': 'Mei'
                }
        }

df = (pd.DataFrame(data)
        .replace(heroNames, regex=False)
        .dropna(how='any')
        )


# df = pd.DataFrame(data

# export data
df.to_csv(os.path.join(dir_data, 'herodata.csv'), index=False)
