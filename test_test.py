

from unicodedata import name


a = {
    "min_damage" : 2,
    "max_damage" : 4
}
name = "alex"
name2 = "Vova"
names = f"{name} and {name2}"
text = f'lalala,{names}'
text2 = f"monster damage:{a['min_damage']} - {a['max_damage']}"
print(text)
