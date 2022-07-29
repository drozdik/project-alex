class Monster:
    max_hp = 30
    armor = 3
    hp = 30
    name = "Skeleton"
    clazz = "Skeleton"
    min_damage = 3
    max_damage = 15
    def alive(self):
        return self.hp > 0

    def dead(self):
        return not self.alive()

class Skeleton(Monster):
    max_hp = 30
    armor = 3
    hp = 30
    name = "Skeleton"
    clazz = "Skeleton"
    min_damage = 3
    max_damage = 15
    

class SkeletonMage(Monster):
    max_hp = 10
    hp = 10
    armor = 2
    name = "Skeleton-mage"
    clazz = "Skeleton-mage"
    min_damage = 10
    max_damage = 14
    

class SkeletonLich(Monster):
    max_hp = 60
    hp = 60
    armor = 18
    name =  "Skeleton-Lich"
    clazz ="Skeleton-Lich"
    min_damage = 10
    max_damage = 20
    