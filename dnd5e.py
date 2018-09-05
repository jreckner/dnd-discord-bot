import requests
import json

phb_index_json = requests.get('https://raw.githubusercontent.com/copperdogma/dnd-phb-5e-index/master/PHB%20Index%20Improved.json').json()
dmg_index_json = requests.get('https://raw.githubusercontent.com/copperdogma/dnd-phb-5e-index/master/DMG%20Index%20Improved.json').json()

results = {}

def lookup_term(term):
    results.clear()
    find_in_PHB(term)
    find_in_DMG(term)
    lines = ''
    for item in results:
        lines += item + ' see page(s) ' + results[item] + '\n'
    return lines

def find_in_PHB(term):
    for node in phb_index_json:
       search_node(term, 'PHB', node)

def find_in_DMG(term):
    for node in dmg_index_json:
       search_node(term, 'DMG', node)

def search_node(term, book, node):
    if term.lower() in node['name'].lower():
       if 'pages' in node:
           results[book + ': ' +  node['name']] = str(node['pages'])
    if "children" in node:
       for child_node in node['children']:
           search_node(term, book, child_node)

#print(lookup_term('rage'))
