from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import re, json
import sys

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
###                                                                                             ###
###    Work in progress, it works but I have to implement function instead of a simple script   ###
###          credits:                                                                           ###
###              https://github.com/sindresorhus/pokemon                                        ###
###              https://pokemondb.net/                                                         ###
###              https://dex.pokemonshowdown.com/                                               ###
###                                                                                             ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


sys.stdout.reconfigure(encoding='utf-8')

def get_ability():
    url = 'https://pokemondb.net/ability'
    service = Service()
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    soup = bs(driver.page_source, 'html.parser')
    driver.implicitly_wait(5)
    driver.quit()

    ability_dict = {}
    for row in soup.find('table', class_='data-table sticky-header block-wide').find_all('tr')[1:]:
        ability_dict[row.find_all('td')[0].text] = row.find_all('td')[2].text

    return ability_dict

def xstr(s):
    return '' if s is None else str(s)

ability_list = get_ability()
listOjb = []
with open('names_json.json', 'r', encoding="utf8") as f:
    # JSON file of all pokemon names (english, french, dutsch, japanese and korean)
    data = json.loads(f.read())


#   Get all names (english, french, japanese, deutsch) from JSON file
names_id = []
for country in ('english', 'french', 'deutsch', 'japanese', 'korean'):
    iterations = [name for name in data[country]]
    names_id.append(iterations)

for pokemon in range(1, 4):  # Number of pokemon added in my JSON file
    #   Connect to pokemonshowdown website to get data
    url = f'https://dex.pokemonshowdown.com/pokemon/{names_id[0][pokemon - 1]}'
    service = Service()
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    soup = bs(driver.page_source, 'html.parser')
    driver.implicitly_wait(5)
    driver.quit()

    #   Base stats / Minimum stats / Maximum stats
    base_stat = []
    for tr in soup.find('table', class_='stats').find_all('tr'):
        # print(*tr.find('td').contents)
        stat = tr.find('td', class_='stat')
        if stat != None:
            base_stat.append(stat.string)
    #   Get base stats value of choosen pokemon 
    #   To get desired value use:
    #   data[0] - for hp base stat
    #   ...
    #   data[5] - for speed base stat

    #   Type 1 and Type 2 (Type/Slot/Name)
    len_type = len(soup.findAll('dd')[0].findAll('a'))
    type1 = soup.findAll('dd')[0].findAll('a')[0].string
    type2 = xstr(soup.findAll('dd')[0].findAll('a')[1].string if len_type > 1 else None)
    #   In case lenght of type < 2 add None to type 2

    #   Abilities 1 and Abilities 2 (Passiv/Slot/Name)
    len_abilities = len(soup.findAll('dd')[2].findAll('a'))
    ability1 = soup.findAll('dd')[2].findAll('a')[0].string
    ability2 = xstr(soup.findAll('dd')[2].findAll('a')[1].string if len_abilities > 1 else None)
    #   In case lenght of abilities < 2 add None to type 2

    #   Moves by level-up / by TM
    moves_lvl = []
    moves_tm = []
    moves_db = []
    for e, i in enumerate(soup.find('ul', class_='utilichart nokbd').findAll('li')[1:]):
        if i.text == 'TM/HM':
            len_li = e
            break
    types = ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']
    for i, move in enumerate(soup.find('ul', class_='utilichart nokbd').findAll('li')[1:]):
        if i < e:
            #   Get data from lvl up table
            for n in move.find_all('img', alt=True):
                if n['alt'] in types:
                    move_type = n.get('alt') 
                    move_lvl = move.find('span').text.encode("ascii", "ignore").strip().decode('utf-8')[1:]
                    move_name = move.find(class_='col shortmovenamecol').string
                    move_power = ''.join(re.findall(r'\d+', move.findAll('span')[3].text.encode("ascii", "ignore").strip().decode('utf-8')[1:]))
                    move_accuracy = ''.join(re.findall(r'\d+', move.findAll('span')[4].text.encode("ascii", "ignore").strip().decode('utf-8')))
                    move_pp = ''.join(re.findall(r'\d+', move.findAll('span')[5].text.encode("ascii", "ignore").strip().decode('utf-8')))
                    move_detail = move.findAll('span')[6].text
                    moves_lvl.append((move_lvl, move_name, move_type, xstr(move_power), xstr(move_accuracy), xstr(move_pp), xstr(move_detail)))
        elif move.string == 'Tutor':
            break
        else:
            #   Get data from TM table
            for n in move.find_all('img', alt=True):
                if n['alt'] in types:
                    move_type = n.get('alt') 
                    move_lvl = move.find('span').text.encode("ascii", "ignore").strip().decode('utf-8')[1:]
                    move_name = move.find(class_='col shortmovenamecol').string
                    move_power = ''.join(re.findall(r'\d+', move.findAll('span')[3].text.encode("ascii", "ignore").strip().decode('utf-8')[1:]))
                    move_accuracy = ''.join(re.findall(r'\d+', move.findAll('span')[4].text.encode("ascii", "ignore").strip().decode('utf-8')))
                    move_pp = ''.join(re.findall(r'\d+', move.findAll('span')[5].text.encode("ascii", "ignore").strip().decode('utf-8')))
                    move_detail = move.find(class_='col movedesccol').text
                    moves_tm.append((move_lvl, move_name, move_type, xstr(move_power), xstr(move_accuracy), xstr(move_pp), xstr(move_detail)))

    #   Create a new entry for each loop and append data to listObj
    new_entry = {
  "id": pokemon,
  "name": {
    "english": names_id[0][pokemon - 1],
    "french": names_id[1][pokemon - 1],
    "deutsch": names_id[2][pokemon - 1],
    "japanese": names_id[3][pokemon - 1],
    "korean": names_id[4][pokemon - 1]
  },
  "type": [
    type1,
    type2
  ],
  "base": {
    "HP": base_stat[0],
    "Attack": base_stat[1],
    "Defense": base_stat[2],
    "Sp. Attack": base_stat[3],
    "Sp. Defense": base_stat[4],
    "Speed": base_stat[5]
  },
  "passive": {
    "slot1": [
      {
        "name": ability1,
        "effect": ability_list[ability1]
      }
    ],
    "slot2": [
      {
        "name": ability2,
        "effect": ability_list[ability2]
      }
    ],
    "abilities": {
      "learned_by_level": [
        [i for i in moves_lvl]
      ],
      "learned_by_tm": [
        [i for i in moves_tm]
      ]
    },
    "images": {
      "mini": "",
      "normal": f'img/{pokemon}.png',
      "normal_shiny": f'img/shiny/{pokemon}.png',
      "gif": ""
    }
  }
}
    listOjb.append(new_entry)
    print('Data added for:', names_id[0][pokemon - 1]) # Print success
    
with open('pokemon_db.json', 'a') as db: # JSON file database
    db.write(json.dumps(listOjb, indent=4, separators=(',', ': '))) # Write data, using indent
    db.close()
        