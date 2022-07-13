from tkinter import *

from PIL import ImageTk, Image


class Screen:

    def __init__(self, hero_attack, monster_pack_attack, game_state):
        self.hero_attack = hero_attack
        self.game_state = game_state
        self.monster_pack_attack = monster_pack_attack
        root = Tk()
        root.title("Diablo dnd edition")

        k_image = ImageTk.PhotoImage(Image.open("images/knight.png"))
        k_label = Label(image=k_image)
        k_label.grid(row=0, column=0, columnspan=1)

        s_image = ImageTk.PhotoImage(Image.open("images/skeleton.png"))
        s_label = Label(image=s_image)
        s_label.grid(row=0, column=1, columnspan=1)

        s_image_2 = ImageTk.PhotoImage(Image.open("images/skeleton.png"))
        s_label_2 = Label(image=s_image_2)
        s_label_2.grid(row=0, column=2, columnspan=1)

        self.hero_panel = Label(
            text=f"Class: Knight\nHealth: {game_state.get('hero_hp')}/{game_state.get('hero_max_hp')}")
        self.hero_panel.grid(row=1, column=0)

        self.monster_1_panel = Label(text=f"Health: {game_state['active_monster_pack'][0]}")
        self.monster_1_panel.grid(row=1, column=1)

        self.monster_2_panel = Label(text=f"Health: {game_state['active_monster_pack'][1]}")
        self.monster_2_panel.grid(row=1, column=2)

        log_panel = Label(text="Hero hit for 4 damage")
        log_panel.grid(row=2, column=0, columnspan=3)

        b_hero_attack = Button(text="Hero attack", command=self.on_hero_attack)
        b_hero_attack.grid(row=3, column=0, columnspan=1)

        root.mainloop()

    def on_hero_attack(self):
        self.hero_attack()  # calls action from the Game
        self.redraw_hero_and_monster_pack_panels()

    def redraw_hero_and_monster_pack_panels(self):
        self.hero_panel.forget()
        self.hero_panel = Label(
            text=f"Class: Knight\nHealth: {self.game_state.get('hero_hp')}/{self.game_state.get('hero_max_hp')}")
        self.hero_panel.grid(row=1, column=0)

        self.monster_1_panel.forget()
        self.monster_1_panel = Label(text=f"Health: {self.game_state['active_monster_pack'][0]}")
        self.monster_1_panel.grid(row=1, column=1)

        self.monster_2_panel.forget()
        self.monster_2_panel = Label(text=f"Health: {self.game_state['active_monster_pack'][1]}")
        self.monster_2_panel.grid(row=1, column=2)
