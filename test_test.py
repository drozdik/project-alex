from random import *
import time


class PokerPlayer:
    clothes = []

    def __init__(self, name, clothes) -> None:
        self.name = name
        self.clothes = clothes

    def on_lose(self):
        remained = len(self.clothes)
        removed = self.clothes.pop(randrange(remained))
        if len(self.clothes) == 0:
            print(f"{self.name} проиграл(а) скинув {removed} последним")
            quit()
        print(f"{self.name} скидывает {removed}")
        return removed


goth_girl = PokerPlayer("Готка", ["Цепи", "Черная юбка", "Армейские ботинки", "Кожаный топ с кнопками"])
school_girl = PokerPlayer("Наташа", ["Клетчатая короткая юбка", "Чюлки", "Белая блузка", "Боты на платформе"])
boobs_girl = PokerPlayer("Анфиса", ["Лифчки D+", "Стринги", "Красные туфли на шпильках", "Подвязка"])
alex = PokerPlayer("Саня", ["Кожанка", "Кроссы", "Трусы красные в белый горошек"])

players = [goth_girl, school_girl, boobs_girl, alex]

while True:
    players[randrange(4)].on_lose()
    time.sleep(1.3)
