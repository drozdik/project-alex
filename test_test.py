from random import randint


class MyMonster:
    
    hp = 10
    def alive():
        if MyMonster.damage >= MyMonster.hp:
            return False
        else:
            return True
    def dead():
        if MyMonster.damage >= MyMonster.hp:
            return True
        else:
            return False

damage = randint(5,15)
m1 = MyMonster()
m1.hp = m1.hp - damage
print("damage:",damage,"Alive:",MyMonster.alive(),"Dead:",MyMonster.dead())
