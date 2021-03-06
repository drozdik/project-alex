from random import randint


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
    
    def take_damage(self,damage):
        effective_damage = damage - self.armor
        if effective_damage > 0:
            self.hp = self.hp - effective_damage
        return(damage, effective_damage)
    
    def deal_damage(self,calc_damage,game_state):
        damage = calc_damage(self.min_damage, self.max_damage)
        effective_damage = damage - game_state["hero_armor"]
        if effective_damage > 0:
            game_state["hero_hp"] = game_state["hero_hp"] - effective_damage
            self.special(game_state)
        return(damage, effective_damage)
    
    def special(self,game_state):
        pass


class Skeleton(Monster):
    max_hp = 30
    armor = 3
    hp = 30
    name = "Skeleton"
    clazz = "Skeleton"
    min_damage = 3
    max_damage = 15
    
    def special(self, game_state):
        print("Skeleton special")
        game_state["hero_armor"]= game_state["hero_armor"] - 2
    

class SkeletonMage(Monster):
    max_hp = 10
    hp = 10
    armor = 2
    name = "Skeleton-mage"
    clazz = "Skeleton-mage"
    min_damage = 10
    max_damage = 14

    def special(self, game_state):
        print("SkeletonMAge special")
        game_state["hero_max_damage"] = game_state["hero_max_damage"] - 5
        if game_state["hero_max_damage"] <= game_state["hero_min_damage"]:
            game_state["hero_max_damage"] = game_state["hero_min_damage"]
        
    

class SkeletonLich(Monster):
    max_hp = 60
    hp = 60
    armor = 18
    name =  "Skeleton-Lich"
    clazz ="Skeleton-Lich"
    min_damage = 10
    max_damage = 20

    def hero_is_stunned(self,game_state):
        return game_state["hero_stuned_rounds"] > 0

    def lich_stun(self,game_state):
        if not self.hero_is_stunned(game_state):
            game_state["hero_armor"] = game_state["hero_armor"] / 2
            game_state["hero_max_damage"] = int(game_state["hero_max_damage"] / 2)
        game_state["hero_stuned_rounds"] = game_state["hero_stuned_rounds"] + 3

    def special(self,game_state):
        print("SkeletonLich special")
        lich_will_stun = randint(1,10) <= 2   
        if lich_will_stun:    
            self.lich_stun(game_state)
    