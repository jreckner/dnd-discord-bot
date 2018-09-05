import random

with open('./data/encounters.txt') as f:
    content = f.readlines()
content = [x.strip() for x in content] 

def get_random_encounter():
    return random.choice(content)
