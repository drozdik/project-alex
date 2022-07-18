
from random import randint
from unicodedata import name
def calc_damage(min_damage, max_damage):
    damage = randint(min_damage, max_damage)
    return damage

m1 = {"min_damage": 2, "max_damage": 8, "name": "m1"}

m2 = {"min_damage": 5, "max_damage": 15, "name": "m2"}

m3 = {"min_damage": 50, "max_damage": 100, "name": "m3"}

m4 = {"min_damage": 150, "max_damage": 200, "name": "m4"}

m5 = {"min_damage": 250, "max_damage": 300, "name": "m5"}
damage1 = calc_damage(m1["min_damage"],m1["max_damage"])
damage2 = calc_damage(m2["min_damage"],m2["max_damage"])
damage3 = calc_damage(m3["min_damage"],m3["max_damage"])
damage4 = calc_damage(m4["min_damage"],m4["max_damage"])
damage5 = calc_damage(m5["min_damage"],m5["max_damage"])




def print_monster_damage(dict):
    damage = calc_damage(dict["min_damage"],dict["max_damage"])
    print(dict["name"],damage)
    

print_monster_damage(m1)
print_monster_damage(m2)
print_monster_damage(m3)






name1 = "alex"
name2 = "Vova"
name3 = "Kostja"
def hello(name):
    print("hello", name)
#hello(name1)
#hello(name2)
#hello(name3)

